"""
Exemplo de uso do gerador de vídeo Stable Diffusion
"""

import os
import logging
from stable_diffusion_pipeline import StableDiffusionVideoGenerator
from video_creator import VideoCreator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_basic_video():
    """Exemplo básico de geração de vídeo"""
    logger.info("=== Exemplo Básico de Geração de Vídeo ===")
    
    # Inicializar gerador
    generator = StableDiffusionVideoGenerator(
        model_id="runwayml/stable-diffusion-v1-5",
        use_openvino=True  # Usar OpenVINO para melhor performance
    )
    
    # Gerar frames
    frames = generator.generate_video_frames(
        initial_prompt="A beautiful sunset over mountains, cinematic lighting",
        frame_prompts=[],  # Usar o prompt inicial para todos os frames
        num_frames=20,
        negative_prompt="blurry, low quality, distorted",
        width=512,
        height=512,
        strength=0.6,  # Menor força para transições mais suaves
        num_inference_steps=15,  # Menos passos para velocidade
        guidance_scale=7.5,
        seed=42
    )
    
    # Criar vídeo
    video_creator = VideoCreator(fps=24, quality=8)
    success = video_creator.create_video(
        frames=frames,
        output_path="example_basic_video.mp4",
        method="imageio"
    )
    
    if success:
        logger.info("Vídeo básico criado com sucesso!")
    
    # Limpar recursos
    generator.cleanup()

def example_animated_prompts():
    """Exemplo com prompts animados"""
    logger.info("=== Exemplo com Prompts Animados ===")
    
    # Prompts que criam uma animação
    frame_prompts = [
        "A cat sitting peacefully in a garden",
        "A cat stretching its paws in a garden",
        "A cat standing up in a garden",
        "A cat walking through the garden",
        "A cat running through the garden",
        "A cat jumping over flowers in the garden",
        "A cat playing with butterflies in the garden",
        "A cat resting under a tree in the garden",
        "A cat looking at birds in the garden",
        "A cat sleeping peacefully in the garden"
    ]
    
    generator = StableDiffusionVideoGenerator(
        model_id="runwayml/stable-diffusion-v1-5",
        use_openvino=True
    )
    
    frames = generator.generate_video_frames(
        initial_prompt=frame_prompts[0],
        frame_prompts=frame_prompts,
        num_frames=len(frame_prompts),
        negative_prompt="blurry, low quality, distorted, multiple cats",
        width=512,
        height=512,
        strength=0.7,
        num_inference_steps=20,
        guidance_scale=7.5,
        seed=123
    )
    
    video_creator = VideoCreator(fps=12, quality=9)  # FPS menor para animação mais lenta
    success = video_creator.create_video(
        frames=frames,
        output_path="example_animated_cat.mp4",
        method="imageio"
    )
    
    if success:
        logger.info("Vídeo animado criado com sucesso!")
    
    generator.cleanup()

def example_style_transition():
    """Exemplo de transição de estilo"""
    logger.info("=== Exemplo de Transição de Estilo ===")
    
    # Prompts que fazem transição de estilo
    style_prompts = [
        "A realistic portrait of a woman, photorealistic",
        "A woman in impressionist painting style",
        "A woman in cubist art style",
        "A woman in abstract art style",
        "A woman in pop art style",
        "A woman in watercolor painting style",
        "A woman in oil painting style",
        "A woman in digital art style",
        "A woman in anime art style",
        "A woman in pixel art style"
    ]
    
    generator = StableDiffusionVideoGenerator(
        model_id="runwayml/stable-diffusion-v1-5",
        use_openvino=True
    )
    
    frames = generator.generate_video_frames(
        initial_prompt=style_prompts[0],
        frame_prompts=style_prompts,
        num_frames=len(style_prompts),
        negative_prompt="blurry, low quality, distorted, multiple people",
        width=512,
        height=512,
        strength=0.8,  # Maior força para mudanças mais dramáticas
        num_inference_steps=25,  # Mais passos para melhor qualidade
        guidance_scale=8.0,
        seed=456
    )
    
    video_creator = VideoCreator(fps=8, quality=10)  # FPS baixo para apreciar as transições
    success = video_creator.create_video(
        frames=frames,
        output_path="example_style_transition.mp4",
        method="imageio"
    )
    
    if success:
        logger.info("Vídeo de transição de estilo criado com sucesso!")
    
    generator.cleanup()

def example_save_frames():
    """Exemplo salvando frames individuais"""
    logger.info("=== Exemplo Salvando Frames Individuais ===")
    
    generator = StableDiffusionVideoGenerator(
        model_id="runwayml/stable-diffusion-v1-5",
        use_openvino=True
    )
    
    frames = generator.generate_video_frames(
        initial_prompt="A magical forest with glowing mushrooms, fantasy art",
        frame_prompts=[],
        num_frames=10,
        negative_prompt="blurry, low quality, distorted",
        width=512,
        height=512,
        strength=0.5,
        num_inference_steps=15,
        guidance_scale=7.5,
        seed=789
    )
    
    # Salvar frames individuais
    video_creator = VideoCreator()
    success = video_creator.save_frames_as_images(
        frames=frames,
        output_dir="magical_forest_frames",
        prefix="forest_frame"
    )
    
    if success:
        logger.info("Frames salvos individualmente com sucesso!")
    
    # Também criar vídeo
    video_success = video_creator.create_video(
        frames=frames,
        output_path="example_magical_forest.mp4",
        method="imageio"
    )
    
    if video_success:
        logger.info("Vídeo também criado com sucesso!")
    
    generator.cleanup()

if __name__ == "__main__":
    print("Exemplos de uso do Gerador de Vídeo Stable Diffusion")
    print("=" * 60)
    
    try:
        # Executar exemplos
        example_basic_video()
        print()
        
        example_animated_prompts()
        print()
        
        example_style_transition()
        print()
        
        example_save_frames()
        print()
        
        print("Todos os exemplos executados com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante execução dos exemplos: {e}")
        print(f"Erro: {e}")
