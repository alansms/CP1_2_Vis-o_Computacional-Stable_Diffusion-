"""
Script de teste rápido para verificar se o sistema está funcionando
"""

import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Testa se todos os imports estão funcionando"""
    logger.info("Testando imports...")
    
    try:
        import torch
        logger.info(f"✅ PyTorch {torch.__version__}")
    except ImportError as e:
        logger.error(f"❌ PyTorch não encontrado: {e}")
        return False
    
    try:
        import diffusers
        logger.info(f"✅ Diffusers {diffusers.__version__}")
    except ImportError as e:
        logger.error(f"❌ Diffusers não encontrado: {e}")
        return False
    
    try:
        import cv2
        logger.info(f"✅ OpenCV {cv2.__version__}")
    except ImportError as e:
        logger.error(f"❌ OpenCV não encontrado: {e}")
        return False
    
    try:
        import imageio
        logger.info(f"✅ ImageIO {imageio.__version__}")
    except ImportError as e:
        logger.error(f"❌ ImageIO não encontrado: {e}")
        return False
    
    try:
        from PIL import Image
        logger.info("✅ Pillow")
    except ImportError as e:
        logger.error(f"❌ Pillow não encontrado: {e}")
        return False
    
    try:
        import numpy as np
        logger.info(f"✅ NumPy {np.__version__}")
    except ImportError as e:
        logger.error(f"❌ NumPy não encontrado: {e}")
        return False
    
    # Testar imports do projeto
    try:
        from stable_diffusion_pipeline import StableDiffusionVideoGenerator
        logger.info("✅ StableDiffusionVideoGenerator")
    except ImportError as e:
        logger.error(f"❌ StableDiffusionVideoGenerator não encontrado: {e}")
        return False
    
    try:
        from video_creator import VideoCreator
        logger.info("✅ VideoCreator")
    except ImportError as e:
        logger.error(f"❌ VideoCreator não encontrado: {e}")
        return False
    
    try:
        from config import Config
        logger.info("✅ Config")
    except ImportError as e:
        logger.error(f"❌ Config não encontrado: {e}")
        return False
    
    return True

def test_gpu():
    """Testa disponibilidade de GPU"""
    logger.info("Testando GPU...")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"✅ {gpu_count} GPU(s) CUDA disponível(is): {gpu_name}")
            return True
        else:
            logger.info("⚠️  GPU CUDA não disponível - usando CPU")
            return True
    except Exception as e:
        logger.error(f"❌ Erro ao verificar GPU: {e}")
        return False

def test_openvino():
    """Testa se OpenVINO está disponível"""
    logger.info("Testando OpenVINO...")
    
    try:
        from optimum.intel import OVStableDiffusionPipeline
        logger.info("✅ OpenVINO disponível")
        return True
    except ImportError:
        logger.warning("⚠️  OpenVINO não disponível - usando PyTorch padrão")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao verificar OpenVINO: {e}")
        return False

def test_ffmpeg():
    """Testa se FFmpeg está disponível"""
    logger.info("Testando FFmpeg...")
    
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            logger.info(f"✅ FFmpeg disponível: {version_line}")
            return True
        else:
            logger.warning("⚠️  FFmpeg não encontrado")
            return False
    except FileNotFoundError:
        logger.warning("⚠️  FFmpeg não encontrado")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao verificar FFmpeg: {e}")
        return False

def test_basic_functionality():
    """Testa funcionalidade básica sem carregar modelo"""
    logger.info("Testando funcionalidade básica...")
    
    try:
        from video_creator import VideoCreator
        from PIL import Image
        import numpy as np
        
        # Criar imagem de teste
        test_image = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
        
        # Testar VideoCreator
        video_creator = VideoCreator(fps=24, quality=8)
        logger.info("✅ VideoCreator inicializado")
        
        # Testar salvamento de frames
        test_frames = [test_image, test_image, test_image]
        success = video_creator.save_frames_as_images(
            frames=test_frames,
            output_dir="test_frames",
            prefix="test"
        )
        
        if success:
            logger.info("✅ Salvamento de frames funcionando")
        else:
            logger.error("❌ Erro no salvamento de frames")
            return False
        
        # Limpar arquivos de teste
        import shutil
        if Path("test_frames").exists():
            shutil.rmtree("test_frames")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na funcionalidade básica: {e}")
        return False

def test_config_system():
    """Testa sistema de configuração"""
    logger.info("Testando sistema de configuração...")
    
    try:
        from config import Config, get_preset_config
        
        # Testar configuração padrão
        default_config = Config.get_default_config()
        logger.info("✅ Configuração padrão carregada")
        
        # Testar presets
        presets = ["fast", "balanced", "high_quality", "style_transition", "animation"]
        for preset in presets:
            config = get_preset_config(preset)
            logger.info(f"✅ Preset '{preset}' carregado")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no sistema de configuração: {e}")
        return False

def main():
    """Função principal de teste"""
    logger.info("🧪 Iniciando testes do sistema...")
    logger.info("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("GPU", test_gpu),
        ("OpenVINO", test_openvino),
        ("FFmpeg", test_ffmpeg),
        ("Funcionalidade Básica", test_basic_functionality),
        ("Sistema de Configuração", test_config_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name}: PASSOU")
            else:
                logger.error(f"❌ {test_name}: FALHOU")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERRO - {e}")
    
    logger.info("\n" + "="*50)
    logger.info(f"📊 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        logger.info("🎉 Todos os testes passaram! Sistema pronto para uso.")
        return True
    else:
        logger.warning(f"⚠️  {total - passed} teste(s) falharam. Verifique as dependências.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
