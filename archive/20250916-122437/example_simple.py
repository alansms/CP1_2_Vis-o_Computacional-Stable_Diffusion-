"""
Exemplo de uso do gerador de vídeo (versão simplificada)
"""

import os
import logging
from video_creator import VideoCreator
from PIL import Image
import numpy as np

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_gradient_frames(num_frames, width=512, height=512):
    """Cria frames com gradientes animados"""
    frames = []
    
    for i in range(num_frames):
        # Criar imagem com gradiente que muda ao longo do tempo
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Gradiente baseado no frame atual
        for y in range(height):
            for x in range(width):
                # Gradiente que muda com o tempo
                r = int(255 * (x / width) * (1 + 0.5 * np.sin(i * 0.2)))
                g = int(255 * (y / height) * (1 + 0.5 * np.cos(i * 0.3)))
                b = int(255 * ((x + y) / (width + height)) * (1 + 0.5 * np.sin(i * 0.1)))
                
                # Limitar valores
                r = min(255, max(0, r))
                g = min(255, max(0, g))
                b = min(255, max(0, b))
                
                img_array[y, x] = [r, g, b]
        
        frames.append(Image.fromarray(img_array))
    
    return frames

def create_circle_animation(num_frames, width=512, height=512):
    """Cria animação de círculo se movendo"""
    frames = []
    
    for i in range(num_frames):
        # Criar fundo preto
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calcular posição do círculo
        center_x = width // 2 + int(100 * np.sin(i * 0.3))
        center_y = height // 2 + int(50 * np.cos(i * 0.2))
        radius = 30
        
        # Desenhar círculo
        for y in range(height):
            for x in range(width):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= radius:
                    # Círculo branco
                    img_array[y, x] = [255, 255, 255]
                elif distance <= radius + 5:
                    # Borda cinza
                    img_array[y, x] = [128, 128, 128]
        
        frames.append(Image.fromarray(img_array))
    
    return frames

def create_wave_animation(num_frames, width=512, height=512):
    """Cria animação de ondas"""
    frames = []
    
    for i in range(num_frames):
        # Criar fundo azul
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        img_array[:, :] = [0, 0, 100]  # Azul escuro
        
        # Desenhar ondas
        for x in range(width):
            for wave_offset in [0, 50, 100]:
                y = int(height // 2 + 30 * np.sin((x + i * 2) * 0.02) + wave_offset)
                if 0 <= y < height:
                    # Onda branca
                    img_array[y, x] = [255, 255, 255]
                    if y + 1 < height:
                        img_array[y + 1, x] = [200, 200, 255]
        
        frames.append(Image.fromarray(img_array))
    
    return frames

def example_gradient_video():
    """Exemplo de vídeo com gradientes animados"""
    logger.info("=== Exemplo: Vídeo com Gradientes Animados ===")
    
    # Criar frames
    frames = create_gradient_frames(30, 512, 512)
    
    # Criar vídeo
    video_creator = VideoCreator(fps=24, quality=8)
    success = video_creator.create_video(
        frames=frames,
        output_path="example_gradient_video.mp4",
        method="imageio"
    )
    
    if success:
        logger.info("Vídeo de gradientes criado com sucesso!")
    else:
        logger.error("Erro ao criar vídeo de gradientes")

def example_circle_animation():
    """Exemplo de animação de círculo"""
    logger.info("=== Exemplo: Animação de Círculo ===")
    
    # Criar frames
    frames = create_circle_animation(40, 512, 512)
    
    # Criar vídeo
    video_creator = VideoCreator(fps=20, quality=9)
    success = video_creator.create_video(
        frames=frames,
        output_path="example_circle_animation.mp4",
        method="imageio"
    )
    
    if success:
        logger.info("Animação de círculo criada com sucesso!")
    else:
        logger.error("Erro ao criar animação de círculo")

def example_wave_animation():
    """Exemplo de animação de ondas"""
    logger.info("=== Exemplo: Animação de Ondas ===")
    
    # Criar frames
    frames = create_wave_animation(50, 512, 512)
    
    # Criar vídeo
    video_creator = VideoCreator(fps=15, quality=8)
    success = video_creator.create_video(
        frames=frames,
        output_path="example_wave_animation.mp4",
        method="imageio"
    )
    
    if success:
        logger.info("Animação de ondas criada com sucesso!")
    else:
        logger.error("Erro ao criar animação de ondas")

def example_save_frames():
    """Exemplo salvando frames individuais"""
    logger.info("=== Exemplo: Salvando Frames Individuais ===")
    
    # Criar frames
    frames = create_gradient_frames(10, 256, 256)
    
    # Salvar frames
    video_creator = VideoCreator()
    success = video_creator.save_frames_as_images(
        frames=frames,
        output_dir="example_frames",
        prefix="gradient_frame"
    )
    
    if success:
        logger.info("Frames salvos individualmente com sucesso!")
    else:
        logger.error("Erro ao salvar frames")

def main():
    """Função principal"""
    print("🎬 Exemplos de Geração de Vídeo")
    print("=" * 50)
    
    try:
        # Executar exemplos
        example_gradient_video()
        print()
        
        example_circle_animation()
        print()
        
        example_wave_animation()
        print()
        
        example_save_frames()
        print()
        
        print("🎉 Todos os exemplos executados com sucesso!")
        print("\n📁 Arquivos criados:")
        
        # Listar arquivos criados
        video_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
        for video_file in video_files:
            size = os.path.getsize(video_file) / 1024  # KB
            print(f"   📹 {video_file} ({size:.1f} KB)")
        
        if os.path.exists("example_frames"):
            frame_count = len([f for f in os.listdir("example_frames") if f.endswith('.png')])
            print(f"   🖼️  example_frames/ ({frame_count} imagens)")
        
    except Exception as e:
        logger.error(f"Erro durante execução dos exemplos: {e}")
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
