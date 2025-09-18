"""
Teste final do sistema usando versão simplificada
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

def test_simple_modules():
    """Testa módulos simplificados"""
    logger.info("Testando módulos simplificados...")
    
    try:
        from stable_diffusion_simple import StableDiffusionVideoGenerator
        logger.info("✅ StableDiffusionVideoGenerator (simples)")
    except ImportError as e:
        logger.error(f"❌ StableDiffusionVideoGenerator (simples): {e}")
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
        from pathlib import Path
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
    """Função principal"""
    logger.info("🧪 Teste final do sistema...")
    logger.info("="*50)
    
    tests = [
        ("Imports Básicos", test_basic_imports),
        ("Módulos Simplificados", test_simple_modules),
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
        logger.info("🎉 Sistema funcionando perfeitamente!")
        logger.info("\n📖 PRÓXIMOS PASSOS:")
        logger.info("1. Execute: python main_simple.py --prompt 'A beautiful sunset' --frames 5")
        logger.info("2. Ou execute: python example_simple.py")
        return True
    else:
        logger.warning(f"⚠️  {total - passed} teste(s) falharam.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
