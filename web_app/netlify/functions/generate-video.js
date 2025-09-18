const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { promisify } = require('util');

const execAsync = promisify(exec);

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Parse form data
    const formData = JSON.parse(event.body);
    const { image, version, frames, fps, quality } = formData;

    if (!image) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'No image provided' })
      };
    }

    // Create temporary directory
    const tempDir = `/tmp/sd_video_${Date.now()}`;
    await execAsync(`mkdir -p ${tempDir}`);

    // Save uploaded image
    const imagePath = `${tempDir}/input.png`;
    const imageBuffer = Buffer.from(image.split(',')[1], 'base64');
    fs.writeFileSync(imagePath, imageBuffer);

    // Determine quality settings
    let width, height, steps;
    switch (quality) {
      case 'fast':
        width = height = 256;
        steps = 10;
        break;
      case 'balanced':
        width = height = 512;
        steps = 20;
        break;
      case 'high':
        width = height = 768;
        steps = 25;
        break;
      default:
        width = height = 512;
        steps = 20;
    }

    // Generate video using Python script
    const pythonScript = `
import sys
sys.path.append('/opt/python')
import os
import numpy as np
from PIL import Image
import torch
import imageio
from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler

# Configuration
model_id = "runwayml/stable-diffusion-v1-5"
width, height = ${width}, ${height}
width = (width // 8) * 8
height = (height // 8) * 8
steps, guidance, frames, fps = ${steps}, 7.5, ${frames}, ${fps}

# Load image
init_img = Image.open("${imagePath}").convert("RGB").resize((width, height), Image.LANCZOS)

# Pipeline
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device=="cuda" else torch.float32,
    safety_checker=None,
    requires_safety_checker=False,
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to(device)

if device == "cuda":
    pipe.enable_attention_slicing()

# Generate frames
${version === 'version1' ? getVersion1Sequence() : getVersion2Sequence()}

# Export video
output_path = "${tempDir}/output.mp4"
with imageio.get_writer(output_path, fps=fps, quality=8) as w:
    for im in frames_list:
        w.append_data(np.array(im.convert("RGB")))

print("Video generated successfully")
`;

    // Write Python script
    const scriptPath = `${tempDir}/generate_video.py`;
    fs.writeFileSync(scriptPath, pythonScript);

    // Execute Python script
    await execAsync(`cd ${tempDir} && python generate_video.py`);

    // Read generated video
    const videoPath = `${tempDir}/output.mp4`;
    const videoBuffer = fs.readFileSync(videoPath);
    const videoBase64 = videoBuffer.toString('base64');

    // Cleanup
    await execAsync(`rm -rf ${tempDir}`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        videoUrl: `data:video/mp4;base64,${videoBase64}`
      })
    };

  } catch (error) {
    console.error('Error generating video:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Failed to generate video',
        details: error.message 
      })
    };
  }
};

function getVersion1Sequence() {
  return `
# Version 1: Continuidade + Movimento Progressivo
progressive_sequence = [
    ("Homer Simpson, yellow skin, cartoon character, arms slightly lowered, same expression", 0.6),
    ("Homer Simpson, yellow skin, cartoon character, arms down, relaxed pose, gentle movement", 0.65),
    ("Homer Simpson, yellow skin, cartoon character, right arm pointing forward, left arm down", 0.7),
    ("Homer Simpson, yellow skin, cartoon character, both arms raised to shoulder height, excited", 0.75),
    ("Homer Simpson, yellow skin, cartoon character, both arms raised high, very excited, jumping", 0.8),
    ("Homer Simpson, yellow skin, cartoon character, hands on hips, confident pose", 0.75),
    ("Homer Simpson, yellow skin, cartoon character, arms crossed, thinking pose", 0.7),
    ("Homer Simpson, yellow skin, cartoon character, original pose, arms raised, returning", 0.65)
]

frames_list = [init_img]
current = init_img

for i in range(1, frames):
    prompt, strength = progressive_sequence[i-1]
    out = pipe(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted, deformed, ugly, disfigured, mutated, extra limbs, missing limbs, bad anatomy, bad proportions, malformed, different character, not Homer Simpson",
        image=current,
        strength=strength,
        num_inference_steps=steps,
        guidance_scale=guidance,
    )
    img = out.images[0]
    frames_list.append(img)
    current = img
`;
}

function getVersion2Sequence() {
  return `
# Version 2: Interpolação Avançada
key_poses = [
    ("Homer Simpson, yellow skin, cartoon character, original pose, arms raised", 0.5),
    ("Homer Simpson, yellow skin, cartoon character, arms slightly lowered, transition", 0.6),
    ("Homer Simpson, yellow skin, cartoon character, arms down, relaxed, gentle movement", 0.7),
    ("Homer Simpson, yellow skin, cartoon character, right arm pointing, left arm down", 0.75),
    ("Homer Simpson, yellow skin, cartoon character, both arms to shoulders, excited", 0.8),
    ("Homer Simpson, yellow skin, cartoon character, both arms raised high, very excited", 0.8),
    ("Homer Simpson, yellow skin, cartoon character, hands on hips, confident", 0.75),
    ("Homer Simpson, yellow skin, cartoon character, arms crossed, thinking", 0.7),
    ("Homer Simpson, yellow skin, cartoon character, returning to original, arms up", 0.6),
    ("Homer Simpson, yellow skin, cartoon character, original pose, arms raised", 0.5)
]

frames_list = [init_img]
current = init_img

for i in range(1, frames):
    prompt, strength = key_poses[i-1]
    out = pipe(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted, deformed, ugly, disfigured, mutated, extra limbs, missing limbs, bad anatomy, bad proportions, malformed, different character, not Homer Simpson",
        image=current,
        strength=strength,
        num_inference_steps=steps,
        guidance_scale=guidance,
    )
    img = out.images[0]
    frames_list.append(img)
    current = img
`;
}
