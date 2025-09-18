"""
Script principal simplificado para geração de vídeo
"""

import argparse
import os
import sys
import logging
from typing import List, Optional
from pathlib import Path

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

def create_demo_video(args):
    """Cria um vídeo de demonstração com imagens sintéticas"""
    logger.info("Criando vídeo de demonstração...")
    
    try:
        from video_creator import VideoCreator
        from PIL import Image
        import numpy as np
        
        # Criar frames sintéticos para demonstração
        frames = []
        for i in range(args.frames):
            # Criar imagem com gradiente que muda ao longo do tempo
            img_array = np.zeros((args.height, args.width, 3), dtype=np.uint8)
            
            # Gradiente baseado no frame atual
            for y in range(args.height):
                for x in range(args.width):
                    # Gradiente que muda com o tempo
                    r = int(255 * (x / args.width) * (1 + 0.5 * np.sin(i * 0.2)))
                    g = int(255 * (y / args.height) * (1 + 0.5 * np.cos(i * 0.3)))
                    b = int(255 * ((x + y) / (args.width + args.height)) * (1 + 0.5 * np.sin(i * 0.1)))
                    
                    # Limitar valores
                    r = min(255, max(0, r))
                    g = min(255, max(0, g))
                    b = min(255, max(0, b))
                    
                    img_array[y, x] = [r, g, b]
            
            # Adicionar texto com o número do frame
            img = Image.fromarray(img_array)
            frames.append(img)
            
            if (i + 1) % 5 == 0:
                logger.info(f"Frame {i + 1}/{args.frames} criado")
        
        # Criar vídeo
        video_creator = VideoCreator(fps=args.fps, quality=args.quality)
        
        success = video_creator.create_video(
            frames=frames,
            output_path=args.output,
            method=args.method
        )
        
        if success:
            logger.info(f"Vídeo de demonstração criado: {args.output}")
            
            # Mostrar informações do arquivo
            if os.path.exists(args.output):
                file_size = os.path.getsize(args.output) / (1024 * 1024)  # MB
                logger.info(f"Tamanho do arquivo: {file_size:.2f} MB")
        else:
            logger.error("Falha ao criar vídeo de demonstração")
            return False
        
        # Salvar frames individuais se solicitado
        if args.save_frames:
            success = video_creator.save_frames_as_images(
                frames=frames,
                output_dir=args.frames_dir,
                prefix="demo_frame"
            )
            
            if success:
                logger.info(f"Frames salvos em: {args.frames_dir}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao criar vídeo de demonstração: {e}")
        return False

def main():
    """Função principal"""
    args = parse_arguments()
    
    logger.info("Iniciando geração de vídeo de demonstração")
    logger.info(f"Prompt: {args.prompt}")
    logger.info(f"Frames: {args.frames}")
    logger.info(f"Saída: {args.output}")
    
    try:
        # Criar vídeo de demonstração
        success = create_demo_video(args)
        
        if success:
            logger.info("Vídeo de demonstração criado com sucesso!")
            logger.info("\n📝 NOTA: Este é um vídeo de demonstração com imagens sintéticas.")
            logger.info("Para usar o Stable Diffusion real, instale as dependências corretamente.")
        else:
            logger.error("Falha ao criar vídeo de demonstração")
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
