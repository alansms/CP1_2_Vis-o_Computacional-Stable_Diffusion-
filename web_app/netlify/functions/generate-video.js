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

    // Create a simple video using the uploaded image
    const tempDir = `/tmp/sd_video_${Date.now()}`;
    await execAsync(`mkdir -p ${tempDir}`);

    // Save uploaded image
    const imagePath = `${tempDir}/input.png`;
    const imageBuffer = Buffer.from(image.split(',')[1], 'base64');
    fs.writeFileSync(imagePath, imageBuffer);

    // Create a simple video by duplicating the image
    const outputPath = `${tempDir}/output.mp4`;
    
    // Use ffmpeg to create a video from the image with some animation
    const duration = 3; // 3 seconds
    const ffmpegCommand = `ffmpeg -loop 1 -i "${imagePath}" -c:v libx264 -t ${duration} -pix_fmt yuv420p -vf "scale=512:512,zoompan=z='min(zoom+0.0015,1.5)':d=${duration*25}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=25" "${outputPath}" -y`;
    
    try {
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
          message: 'Demo mode: Video created from your uploaded image with zoom effect. For full Stable Diffusion processing, use the Jupyter notebooks locally.'
        })
      };
    } catch (ffmpegError) {
      console.error('FFmpeg zoom error:', ffmpegError);
      
      // Try simpler version without zoom
      try {
        const simpleCommand = `ffmpeg -loop 1 -i "${imagePath}" -c:v libx264 -t 3 -pix_fmt yuv420p -vf "scale=512:512" "${outputPath}" -y`;
        await execAsync(simpleCommand);
        
        const videoBuffer = fs.readFileSync(outputPath);
        const videoBase64 = videoBuffer.toString('base64');
        
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
      } catch (simpleError) {
        console.error('FFmpeg simple error:', simpleError);
      
      // Fallback to sample video if ffmpeg fails
      const demoVideoPath = path.join(__dirname, '../../demo_video.mp4');
      
      if (fs.existsSync(demoVideoPath)) {
        const videoBuffer = fs.readFileSync(demoVideoPath);
        const videoBase64 = videoBuffer.toString('base64');
        
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            videoUrl: `data:video/mp4;base64,${videoBase64}`,
            demo: true,
            message: 'Demo mode: Fallback video returned. For full functionality, use the Jupyter notebooks locally.'
          })
        };
      } else {
        // Final fallback to external URL
        const sampleVideoUrl = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';
        
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            videoUrl: sampleVideoUrl,
            demo: true,
            message: 'Demo mode: External video returned. For full functionality, use the Jupyter notebooks locally.'
          })
        };
      }
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
