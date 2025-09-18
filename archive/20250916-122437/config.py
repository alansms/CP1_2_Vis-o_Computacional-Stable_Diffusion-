"""
Arquivo de configuração para o gerador de vídeo Stable Diffusion
"""

import os
from typing import Dict, Any

class Config:
    """Classe de configuração para o gerador de vídeo"""
    
    # Configurações padrão do modelo
    DEFAULT_MODEL = "runwayml/stable-diffusion-v1-5"
    USE_OPENVINO = True
    
    # Configurações de geração
    DEFAULT_WIDTH = 512
    DEFAULT_HEIGHT = 512
    DEFAULT_STEPS = 20
    DEFAULT_GUIDANCE = 7.5
    DEFAULT_STRENGTH = 0.7
    
    # Configurações de vídeo
    DEFAULT_FPS = 24
    DEFAULT_QUALITY = 8
    DEFAULT_METHOD = "imageio"
    
    # Configurações de diretórios
    FRAMES_DIR = "frames"
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """Retorna configuração padrão"""
        return {
            "model_id": cls.DEFAULT_MODEL,
            "use_openvino": cls.USE_OPENVINO,
            "width": cls.DEFAULT_WIDTH,
            "height": cls.DEFAULT_HEIGHT,
            "steps": cls.DEFAULT_STEPS,
            "guidance": cls.DEFAULT_GUIDANCE,
            "strength": cls.DEFAULT_STRENGTH,
            "fps": cls.DEFAULT_FPS,
            "quality": cls.DEFAULT_QUALITY,
            "method": cls.DEFAULT_METHOD,
            "frames_dir": cls.FRAMES_DIR,
            "output_dir": cls.OUTPUT_DIR,
            "temp_dir": cls.TEMP_DIR,
            "log_level": cls.LOG_LEVEL,
            "log_format": cls.LOG_FORMAT
        }
    
    @classmethod
    def load_from_file(cls, config_path: str) -> Dict[str, Any]:
        """Carrega configuração de arquivo"""
        import json
        
        if not os.path.exists(config_path):
            return cls.get_default_config()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Mesclar com configuração padrão
            default_config = cls.get_default_config()
            default_config.update(config)
            
            return default_config
            
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return cls.get_default_config()
    
    @classmethod
    def save_to_file(cls, config: Dict[str, Any], config_path: str):
        """Salva configuração em arquivo"""
        import json
        
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")

# Configurações pré-definidas para diferentes tipos de vídeo
PRESET_CONFIGS = {
    "fast": {
        "steps": 10,
        "strength": 0.5,
        "fps": 30,
        "quality": 6
    },
    
    "balanced": {
        "steps": 20,
        "strength": 0.7,
        "fps": 24,
        "quality": 8
    },
    
    "high_quality": {
        "steps": 30,
        "strength": 0.6,
        "fps": 24,
        "quality": 10,
        "method": "ffmpeg"
    },
    
    "style_transition": {
        "steps": 25,
        "strength": 0.8,
        "fps": 8,
        "quality": 9
    },
    
    "animation": {
        "steps": 15,
        "strength": 0.6,
        "fps": 12,
        "quality": 8
    }
}

def get_preset_config(preset_name: str) -> Dict[str, Any]:
    """Retorna configuração de preset"""
    if preset_name not in PRESET_CONFIGS:
        raise ValueError(f"Preset '{preset_name}' não encontrado. Disponíveis: {list(PRESET_CONFIGS.keys())}")
    
    # Mesclar com configuração padrão
    default_config = Config.get_default_config()
    default_config.update(PRESET_CONFIGS[preset_name])
    
    return default_config
