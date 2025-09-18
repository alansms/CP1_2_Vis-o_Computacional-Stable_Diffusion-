// Global Variables
let selectedVersion = 'version1';
let selectedFile = null;
let isGenerating = false;

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const removeImage = document.getElementById('removeImage');
const generateBtn = document.getElementById('generateBtn');
const progress = document.getElementById('progress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const results = document.getElementById('results');
const generatedVideo = document.getElementById('generatedVideo');
const downloadBtn = document.getElementById('downloadBtn');

// Version Buttons
const version1Btn = document.getElementById('version1');
const version2Btn = document.getElementById('version2');

// Settings
const framesSlider = document.getElementById('frames');
const fpsSlider = document.getElementById('fps');
const qualitySelect = document.getElementById('quality');
const framesValue = document.getElementById('framesValue');
const fpsValue = document.getElementById('fpsValue');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Version selection
    version1Btn.addEventListener('click', () => selectVersion('version1'));
    version2Btn.addEventListener('click', () => selectVersion('version2'));
    
    // File handling
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);
    removeImage.addEventListener('click', removeSelectedImage);
    
    // Generate button
    generateBtn.addEventListener('click', generateVideo);
    
    // Settings
    framesSlider.addEventListener('input', updateFramesValue);
    fpsSlider.addEventListener('input', updateFpsValue);
    
    // Download button
    downloadBtn.addEventListener('click', downloadVideo);
    
    updateGenerateButton();
    
    // Show demo notification if running locally
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    if (isLocal) {
        showNotification('🎬 Modo Demo: Interface funcionando localmente. Para funcionalidade completa, faça deploy no Netlify.', 'info');
        // Update button text for demo mode
        generateBtn.innerHTML = '<i class="fas fa-video"></i> Gerar Vídeo (Demo)';
    }
}

// Version Selection
function selectVersion(version) {
    selectedVersion = version;
    
    // Update button states
    version1Btn.classList.toggle('active', version === 'version1');
    version2Btn.classList.toggle('active', version === 'version2');
    
    console.log(`Versão selecionada: ${version}`);
}

// File Handling
function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Por favor, selecione apenas arquivos de imagem.');
        return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('O arquivo é muito grande. Máximo 10MB.');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImage.src = e.target.result;
        preview.style.display = 'block';
        dropZone.style.display = 'none';
    };
    reader.readAsDataURL(file);
    
    updateGenerateButton();
}

function removeSelectedImage() {
    selectedFile = null;
    preview.style.display = 'none';
    dropZone.style.display = 'block';
    fileInput.value = '';
    updateGenerateButton();
}

// Settings
function updateFramesValue() {
    framesValue.textContent = framesSlider.value;
}

function updateFpsValue() {
    fpsValue.textContent = fpsSlider.value;
}

// Generate Button
function updateGenerateButton() {
    generateBtn.disabled = !selectedFile || isGenerating;
}

// Video Generation
async function generateVideo() {
    if (!selectedFile || isGenerating) return;
    
    isGenerating = true;
    updateGenerateButton();
    
    // Show progress
    progress.style.display = 'block';
    results.style.display = 'none';
    
    try {
        // Simulate progress
        await simulateProgress();
        
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('version', selectedVersion);
        formData.append('frames', framesSlider.value);
        formData.append('fps', fpsSlider.value);
        formData.append('quality', qualitySelect.value);
        
        // Call API (replace with your actual endpoint)
        const response = await callGenerationAPI(formData);
        
        if (response.success) {
            showResults(response.videoUrl);
        } else {
            throw new Error(response.error || 'Erro na geração do vídeo');
        }
        
    } catch (error) {
        console.error('Erro na geração:', error);
        alert('Erro na geração do vídeo: ' + error.message);
    } finally {
        isGenerating = false;
        updateGenerateButton();
        progress.style.display = 'none';
    }
}

async function simulateProgress() {
    const steps = [
        { progress: 20, text: 'Carregando imagem...' },
        { progress: 40, text: 'Inicializando Stable Diffusion...' },
        { progress: 60, text: 'Gerando frames...' },
        { progress: 80, text: 'Processando vídeo...' },
        { progress: 100, text: 'Finalizando...' }
    ];
    
    for (const step of steps) {
        progressFill.style.width = step.progress + '%';
        progressText.textContent = step.text;
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

async function callGenerationAPI(formData) {
    try {
        // Check if we're running locally (no Netlify functions)
        const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        
        if (isLocal) {
            // Local demo mode - simulate API call
            console.log('Running in local demo mode');
            await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate processing
            
            return {
                success: true,
                videoUrl: 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4' // Demo video
            };
        }
        
        // Production mode - call Netlify function
        const imageBase64 = await fileToBase64(selectedFile);
        
        const requestData = {
            image: imageBase64,
            version: selectedVersion,
            frames: parseInt(framesSlider.value),
            fps: parseInt(fpsSlider.value),
            quality: qualitySelect.value
        };
        
        const response = await fetch('/.netlify/functions/generate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Erro na geração do vídeo');
        }
        
        return result;
        
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

function showResults(videoUrl) {
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    
    if (isLocal) {
        // Demo mode - show demo content
        results.innerHTML = `
            <h3>Vídeo Gerado (Demo):</h3>
            <div style="background: #f0f0f0; padding: 40px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <i class="fas fa-video" style="font-size: 3rem; color: #667eea; margin-bottom: 20px;"></i>
                <h4>Vídeo Demo</h4>
                <p>Em produção, aqui apareceria o vídeo gerado pelo Stable Diffusion.</p>
                <p><strong>Configurações usadas:</strong></p>
                <ul style="list-style: none; padding: 0;">
                    <li>Versão: ${selectedVersion === 'version1' ? '1' : '2'}</li>
                    <li>Frames: ${framesSlider.value}</li>
                    <li>FPS: ${fpsSlider.value}</li>
                    <li>Qualidade: ${qualitySelect.options[qualitySelect.selectedIndex].text}</li>
                </ul>
            </div>
            <div class="download-section">
                <button id="downloadBtn" class="download-btn">
                    <i class="fas fa-download"></i>
                    Baixar Vídeo (Demo)
                </button>
            </div>
        `;
        
        // Re-attach download button event
        document.getElementById('downloadBtn').addEventListener('click', downloadVideo);
    } else {
        // Production mode - show actual video
        generatedVideo.src = videoUrl;
    }
    
    results.style.display = 'block';
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth' });
}

function downloadVideo() {
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    
    if (isLocal) {
        showNotification('🎬 Modo Demo: Em produção, aqui seria baixado o vídeo gerado pelo Stable Diffusion!', 'info');
        return;
    }
    
    const link = document.createElement('a');
    link.href = generatedVideo.src;
    link.download = `stable_diffusion_video_${Date.now()}.mp4`;
    link.click();
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'error' ? '#ff4757' : '#2ed573'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add CSS for notification animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Error Handling
window.addEventListener('error', function(e) {
    console.error('Error:', e.error);
    showNotification('Ocorreu um erro inesperado. Tente novamente.', 'error');
});

// Prevent default drag behaviors
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => e.preventDefault());
