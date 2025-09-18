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

    // DEMO MODE: Return the uploaded image directly
    // This is the simplest approach that always works
    
    console.log('Demo mode: Returning uploaded image directly');
    console.log('Parameters:', { version, frames, fps, quality });

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Return the uploaded image directly as a "video"
    // This ensures the user always sees their uploaded image
    const imageBase64 = image.split(',')[1]; // Remove data:image/png;base64, prefix
    
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
