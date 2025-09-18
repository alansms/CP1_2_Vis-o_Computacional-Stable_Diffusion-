"""
Script de instalação e configuração do gerador de vídeo Stable Diffusion
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_gpu():
    """Verifica disponibilidade de GPU"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU CUDA disponível: {gpu_name}")
            return True
        else:
            print("⚠️  GPU CUDA não disponível - usando CPU")
            return False
    except ImportError:
        print("⚠️  PyTorch não instalado - não é possível verificar GPU")
        return False

def install_requirements():
    """Instala dependências do requirements.txt"""
    print("\n📦 Instalando dependências...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_ffmpeg():
    """Verifica se FFmpeg está instalado"""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, check=True)
        print("✅ FFmpeg encontrado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg não encontrado")
        print_ffmpeg_install_instructions()
        return False

def print_ffmpeg_install_instructions():
    """Imprime instruções de instalação do FFmpeg"""
    system = platform.system().lower()
    
    print("\n📋 Para instalar FFmpeg:")
    
    if system == "darwin":  # macOS
        print("   brew install ffmpeg")
    elif system == "linux":
        print("   sudo apt update && sudo apt install ffmpeg")
    elif system == "windows":
        print("   Baixe de: https://ffmpeg.org/download.html")
    else:
        print("   Consulte: https://ffmpeg.org/download.html")

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ["output", "frames", "temp", "configs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def create_sample_config():
    """Cria arquivo de configuração de exemplo"""
    print("\n⚙️  Criando configuração de exemplo...")
    
    config_content = """{
  "model_id": "runwayml/stable-diffusion-v1-5",
  "use_openvino": true,
  "width": 512,
  "height": 512,
  "steps": 20,
  "guidance": 7.5,
  "strength": 0.7,
  "fps": 24,
  "quality": 8,
  "method": "imageio",
  "frames_dir": "frames",
  "output_dir": "output",
  "temp_dir": "temp"
}"""
    
    try:
        with open("configs/default.json", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("   ✅ configs/default.json")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar configuração: {e}")
        return False

def create_sample_frame_prompts():
    """Cria arquivo de exemplo com prompts de frames"""
    print("\n📝 Criando exemplo de prompts de frames...")
    
    prompts_content = """# Exemplo de prompts para animação
# Cada linha representa um prompt para um frame

A cat sitting peacefully in a garden
A cat stretching its paws in a garden
A cat standing up in a garden
A cat walking through the garden
A cat running through the garden
A cat jumping over flowers in the garden
A cat playing with butterflies in the garden
A cat resting under a tree in the garden
A cat looking at birds in the garden
A cat sleeping peacefully in the garden
"""
    
    try:
        with open("frame_prompts_example.txt", "w", encoding="utf-8") as f:
            f.write(prompts_content)
        print("   ✅ frame_prompts_example.txt")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar exemplo de prompts: {e}")
        return False

def test_installation():
    """Testa se a instalação foi bem-sucedida"""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testar imports principais
        from stable_diffusion_pipeline import StableDiffusionVideoGenerator
        from video_creator import VideoCreator
        from config import Config
        
        print("   ✅ Imports principais - OK")
        
        # Testar configuração
        config = Config.get_default_config()
        print("   ✅ Sistema de configuração - OK")
        
        print("✅ Instalação testada com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def print_usage_instructions():
    """Imprime instruções de uso"""
    print("\n" + "="*60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    
    print("\n📖 COMO USAR:")
    print("\n1. Exemplo básico:")
    print("   python main.py --prompt 'A beautiful sunset' --frames 20")
    
    print("\n2. Com prompts animados:")
    print("   python main.py --prompt 'A cat in a garden' \\")
    print("     --frame-prompts 'A cat stretching' 'A cat walking' \\")
    print("     --frames 10 --output cat_animation.mp4")
    
    print("\n3. Usando arquivo de prompts:")
    print("   python main.py --prompt 'A magical forest' \\")
    print("     --frame-prompts $(cat frame_prompts_example.txt) \\")
    print("     --frames 10")
    
    print("\n4. Executar exemplos:")
    print("   python example_usage.py")
    
    print("\n📚 Para mais informações, consulte o README.md")
    print("\n🚀 Divirta-se criando vídeos com IA!")

def main():
    """Função principal de instalação"""
    print("🚀 Instalador do Gerador de Vídeo Stable Diffusion")
    print("="*60)
    
    # Verificações iniciais
    if not check_python_version():
        sys.exit(1)
    
    check_gpu()
    
    # Instalação
    if not install_requirements():
        sys.exit(1)
    
    # Verificações pós-instalação
    check_ffmpeg()
    
    # Configuração
    create_directories()
    create_sample_config()
    create_sample_frame_prompts()
    
    # Teste final
    if test_installation():
        print_usage_instructions()
    else:
        print("\n❌ Instalação falhou. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()
