"""
Script principal para geração de vídeo usando Stable Diffusion com retroalimentação
"""

import argparse
import os
import sys
import logging
from typing import List, Optional
from pathlib import Path

from stable_diffusion_pipeline import StableDiffusionVideoGenerator
from video_creator import VideoCreator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse dos argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="Gerador de vídeo usando Stable Diffusion com retroalimentação"
    )
    
    # Parâmetros básicos
    parser.add_argument(
        "--prompt", 
        type=str, 
        required=True,
        help="Prompt inicial para geração do vídeo"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="generated_video.mp4",
        help="Caminho do arquivo de vídeo de saída"
    )
    
    parser.add_argument(
        "--frames", 
        type=int, 
        default=30,
        help="Número de frames a gerar"
    )
    
    # Parâmetros do modelo
    parser.add_argument(
        "--model", 
        type=str, 
        default="runwayml/stable-diffusion-v1-5",
        help="ID do modelo Stable Diffusion"
    )
    
    parser.add_argument(
        "--no-openvino", 
        action="store_true",
        help="Desabilitar otimização OpenVINO"
    )
    
    # Parâmetros de geração
    parser.add_argument(
        "--width", 
        type=int, 
        default=512,
        help="Largura das imagens"
    )
    
    parser.add_argument(
        "--height", 
        type=int, 
        default=512,
        help="Altura das imagens"
    )
    
    parser.add_argument(
        "--steps", 
        type=int, 
        default=20,
        help="Número de passos de inferência"
    )
    
    parser.add_argument(
        "--guidance", 
        type=float, 
        default=7.5,
        help="Escala de orientação"
    )
    
    parser.add_argument(
        "--strength", 
        type=float, 
        default=0.7,
        help="Força da transformação entre frames"
    )
    
    parser.add_argument(
        "--seed", 
        type=int, 
        default=None,
        help="Semente para reprodutibilidade"
    )
    
    # Parâmetros do vídeo
    parser.add_argument(
        "--fps", 
        type=int, 
        default=24,
        help="Frames por segundo do vídeo"
    )
    
    parser.add_argument(
        "--quality", 
        type=int, 
        default=8,
        help="Qualidade do vídeo (1-10)"
    )
    
    parser.add_argument(
        "--method", 
        type=str, 
        choices=['opencv', 'imageio', 'ffmpeg'],
        default='imageio',
        help="Método para criação do vídeo"
    )
    
    # Parâmetros adicionais
    parser.add_argument(
        "--negative-prompt", 
        type=str, 
        default="",
        help="Prompt negativo"
    )
    
    parser.add_argument(
        "--save-frames", 
        action="store_true",
        help="Salvar frames individuais como imagens"
    )
    
    parser.add_argument(
        "--frames-dir", 
        type=str, 
        default="frames",
        help="Diretório para salvar frames individuais"
    )
    
    parser.add_argument(
        "--frame-prompts", 
        type=str, 
        nargs='*',
        help="Prompts específicos para cada frame"
    )
    
    return parser.parse_args()

def load_frame_prompts(file_path: str) -> List[str]:
    """Carrega prompts de frames de um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f.readlines() if line.strip()]
        return prompts
    except Exception as e:
        logger.error(f"Erro ao carregar prompts de frames: {e}")
        return []

def main():
    """Função principal"""
    args = parse_arguments()
    
    logger.info("Iniciando geração de vídeo com Stable Diffusion")
    logger.info(f"Prompt: {args.prompt}")
    logger.info(f"Frames: {args.frames}")
    logger.info(f"Modelo: {args.model}")
    logger.info(f"OpenVINO: {not args.no_openvino}")
    
    try:
        # Inicializar gerador de vídeo
        video_generator = StableDiffusionVideoGenerator(
            model_id=args.model,
            use_openvino=not args.no_openvino
        )
        
        # Preparar prompts de frames
        frame_prompts = []
        if args.frame_prompts:
            frame_prompts = args.frame_prompts
        elif os.path.exists("frame_prompts.txt"):
            frame_prompts = load_frame_prompts("frame_prompts.txt")
        
        # Gerar frames
        logger.info("Iniciando geração de frames...")
        frames = video_generator.generate_video_frames(
            initial_prompt=args.prompt,
            frame_prompts=frame_prompts,
            num_frames=args.frames,
            negative_prompt=args.negative_prompt,
            width=args.width,
            height=args.height,
            strength=args.strength,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            seed=args.seed
        )
        
        logger.info(f"Gerados {len(frames)} frames com sucesso")
        
        # Salvar frames individuais se solicitado
        if args.save_frames:
            video_creator = VideoCreator(fps=args.fps, quality=args.quality)
            video_creator.save_frames_as_images(frames, args.frames_dir)
        
        # Criar vídeo
        logger.info("Criando vídeo...")
        video_creator = VideoCreator(fps=args.fps, quality=args.quality)
        
        success = video_creator.create_video(
            frames=frames,
            output_path=args.output,
            method=args.method
        )
        
        if success:
            logger.info(f"Vídeo criado com sucesso: {args.output}")
            
            # Mostrar informações do arquivo
            if os.path.exists(args.output):
                file_size = os.path.getsize(args.output) / (1024 * 1024)  # MB
                logger.info(f"Tamanho do arquivo: {file_size:.2f} MB")
        else:
            logger.error("Falha ao criar vídeo")
            sys.exit(1)
        
        # Limpar recursos
        video_generator.cleanup()
        
    except KeyboardInterrupt:
        logger.info("Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
