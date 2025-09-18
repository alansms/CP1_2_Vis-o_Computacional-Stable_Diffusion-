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

    // DEMO MODE: Return a sample video URL instead of processing
    // This is because Stable Diffusion requires significant resources
    // that are not available in Netlify Functions
    
    console.log('Demo mode: Returning sample video');
    console.log('Parameters:', { version, frames, fps, quality });

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Return a sample video URL (you can replace this with your own)
    const sampleVideoUrl = 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4';

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        videoUrl: sampleVideoUrl,
        demo: true,
        message: 'Demo mode: Sample video returned. For full functionality, use the Jupyter notebooks locally.'
      })
    };

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
