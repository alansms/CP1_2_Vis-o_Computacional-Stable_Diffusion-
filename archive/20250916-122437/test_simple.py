"""
Teste simples do sistema sem OpenVINO
"""

import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_basic_imports():
    """Testa imports básicos"""
    logger.info("Testando imports básicos...")
    
    try:
        import torch
        logger.info(f"✅ PyTorch {torch.__version__}")
    except ImportError as e:
        logger.error(f"❌ PyTorch: {e}")
        return False
    
    try:
        import diffusers
        logger.info(f"✅ Diffusers {diffusers.__version__}")
    except ImportError as e:
        logger.error(f"❌ Diffusers: {e}")
        return False
    
    try:
        import cv2
        logger.info(f"✅ OpenCV {cv2.__version__}")
    except ImportError as e:
        logger.error(f"❌ OpenCV: {e}")
        return False
    
    try:
        import imageio
        logger.info(f"✅ ImageIO {imageio.__version__}")
    except ImportError as e:
        logger.error(f"❌ ImageIO: {e}")
        return False
    
    try:
        from PIL import Image
        logger.info("✅ Pillow")
    except ImportError as e:
        logger.error(f"❌ Pillow: {e}")
        return False
    
    return True

def test_project_modules():
    """Testa módulos do projeto"""
    logger.info("Testando módulos do projeto...")
    
    try:
        from stable_diffusion_pipeline import StableDiffusionVideoGenerator
        logger.info("✅ StableDiffusionVideoGenerator")
    except ImportError as e:
        logger.error(f"❌ StableDiffusionVideoGenerator: {e}")
        return False
    
    try:
        from video_creator import VideoCreator
        logger.info("✅ VideoCreator")
    except ImportError as e:
        logger.error(f"❌ VideoCreator: {e}")
        return False
    
    try:
        from config import Config
        logger.info("✅ Config")
    except ImportError as e:
        logger.error(f"❌ Config: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Testa funcionalidade básica"""
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
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na funcionalidade básica: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🧪 Teste simples do sistema...")
    logger.info("="*50)
    
    tests = [
        ("Imports Básicos", test_basic_imports),
        ("Módulos do Projeto", test_project_modules),
        ("Funcionalidade Básica", test_basic_functionality)
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
        logger.info("🎉 Sistema básico funcionando!")
        return True
    else:
        logger.warning(f"⚠️  {total - passed} teste(s) falharam.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
