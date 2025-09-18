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

    // DEMO MODE: Create a simple video based on the uploaded image
    // This simulates the Stable Diffusion process without the heavy computation
    
    console.log('Demo mode: Creating video from uploaded image');
    console.log('Parameters:', { version, frames, fps, quality });

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Create a simple video by duplicating the uploaded image
    // This approach works without external dependencies
    const tempDir = `/tmp/sd_video_${Date.now()}`;
    await execAsync(`mkdir -p ${tempDir}`);

    // Save uploaded image
    const imagePath = `${tempDir}/input.png`;
    const imageBuffer = Buffer.from(image.split(',')[1], 'base64');
    fs.writeFileSync(imagePath, imageBuffer);

    // Create multiple copies of the image to simulate frames
    const numFrames = parseInt(frames) || 8;
    const frames = [];
    
    for (let i = 0; i < numFrames; i++) {
      const framePath = `${tempDir}/frame_${i.toString().padStart(3, '0')}.png`;
      fs.copyFileSync(imagePath, framePath);
      frames.push(framePath);
    }

    // Try to create video with FFmpeg (if available)
    const outputPath = `${tempDir}/output.mp4`;
    
    try {
      const ffmpegCommand = `ffmpeg -framerate ${fps || 12} -i "${tempDir}/frame_%03d.png" -c:v libx264 -pix_fmt yuv420p "${outputPath}" -y`;
      await execAsync(ffmpegCommand);
      
      // Read the generated video
      const videoBuffer = fs.readFileSync(outputPath);
      const videoBase64 = videoBuffer.toString('base64');
      
      // Cleanup
      await execAsync(`rm -rf ${tempDir}`);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          videoUrl: `data:video/mp4;base64,${videoBase64}`,
          demo: true,
          message: 'Demo mode: Video created from your uploaded image. For full Stable Diffusion processing, use the Jupyter notebooks locally.'
        })
      };
    } catch (ffmpegError) {
      console.error('FFmpeg error:', ffmpegError);
      
      // Fallback: Return the original image as a "video"
      // This ensures the user sees their uploaded image
      const imageBase64 = imageBuffer.toString('base64');
      
      await execAsync(`rm -rf ${tempDir}`);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          videoUrl: `data:image/png;base64,${imageBase64}`,
          demo: true,
          message: 'Demo mode: Your uploaded image returned. For full Stable Diffusion processing, use the Jupyter notebooks locally.'
        })
      };
    }

  } catch (error) {
    console.error('Error in demo mode:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Demo mode error',
        details: error.message 
      })
    };
  }
};

// Demo mode function - no complex processing needed
