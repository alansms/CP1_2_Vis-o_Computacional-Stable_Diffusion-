"""
Módulo para criação de vídeo a partir de frames gerados pelo Stable Diffusion
"""

import cv2
import numpy as np
from PIL import Image
import imageio
import os
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class VideoCreator:
    """
    Classe para criar vídeos a partir de frames de imagens
    """
    
    def __init__(self, fps: int = 24, quality: int = 8):
        """
        Inicializa o criador de vídeo
        
        Args:
            fps: Frames por segundo do vídeo
            quality: Qualidade do vídeo (1-10, onde 10 é melhor qualidade)
        """
        self.fps = fps
        self.quality = quality
    
    def frames_to_video_opencv(self, 
                              frames: List[Image.Image], 
                              output_path: str,
                              codec: str = 'mp4v') -> bool:
        """
        Cria vídeo usando OpenCV
        
        Args:
            frames: Lista de imagens PIL
            output_path: Caminho do arquivo de saída
            codec: Codec de vídeo
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            if not frames:
                logger.error("Lista de frames vazia")
                return False
            
            # Obter dimensões da primeira imagem
            width, height = frames[0].size
            
            # Configurar codec e writer
            fourcc = cv2.VideoWriter_fourcc(*codec)
            out = cv2.VideoWriter(output_path, fourcc, self.fps, (width, height))
            
            logger.info(f"Criando vídeo com {len(frames)} frames, {self.fps} FPS")
            
            for i, frame in enumerate(frames):
                # Converter PIL para OpenCV
                frame_cv = self._pil_to_opencv(frame)
                out.write(frame_cv)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Processado {i + 1}/{len(frames)} frames")
            
            out.release()
            logger.info(f"Vídeo salvo em: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar vídeo com OpenCV: {e}")
            return False
    
    def frames_to_video_imageio(self, 
                               frames: List[Image.Image], 
                               output_path: str,
                               format: str = 'mp4') -> bool:
        """
        Cria vídeo usando imageio
        
        Args:
            frames: Lista de imagens PIL
            output_path: Caminho do arquivo de saída
            format: Formato do vídeo
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            if not frames:
                logger.error("Lista de frames vazia")
                return False
            
            logger.info(f"Criando vídeo com imageio: {len(frames)} frames")
            
            # Converter frames PIL para numpy arrays
            frame_arrays = []
            for i, frame in enumerate(frames):
                # Converter para RGB se necessário
                if frame.mode != 'RGB':
                    frame = frame.convert('RGB')
                
                # Converter para numpy array
                frame_array = np.array(frame)
                frame_arrays.append(frame_array)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Convertido {i + 1}/{len(frames)} frames")
            
            # Criar vídeo
            with imageio.get_writer(output_path, fps=self.fps, quality=self.quality) as writer:
                for frame_array in frame_arrays:
                    writer.append_data(frame_array)
            
            logger.info(f"Vídeo salvo em: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar vídeo com imageio: {e}")
            return False
    
    def frames_to_video_ffmpeg(self, 
                              frames: List[Image.Image], 
                              output_path: str,
                              temp_dir: str = "temp_frames") -> bool:
        """
        Cria vídeo usando FFmpeg (salva frames temporários)
        
        Args:
            frames: Lista de imagens PIL
            output_path: Caminho do arquivo de saída
            temp_dir: Diretório temporário para frames
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            if not frames:
                logger.error("Lista de frames vazia")
                return False
            
            # Criar diretório temporário
            os.makedirs(temp_dir, exist_ok=True)
            
            logger.info(f"Salvando {len(frames)} frames temporários")
            
            # Salvar frames como imagens temporárias
            for i, frame in enumerate(frames):
                frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
                frame.save(frame_path)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Salvo {i + 1}/{len(frames)} frames")
            
            # Usar FFmpeg para criar vídeo
            import subprocess
            
            # Comando FFmpeg
            cmd = [
                'ffmpeg',
                '-y',  # Sobrescrever arquivo existente
                '-framerate', str(self.fps),
                '-i', os.path.join(temp_dir, 'frame_%04d.png'),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-crf', str(23 - self.quality),  # CRF inversamente proporcional à qualidade
                output_path
            ]
            
            logger.info("Executando FFmpeg...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Vídeo criado com sucesso: {output_path}")
                
                # Limpar arquivos temporários
                self._cleanup_temp_files(temp_dir)
                return True
            else:
                logger.error(f"Erro no FFmpeg: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao criar vídeo com FFmpeg: {e}")
            return False
    
    def _pil_to_opencv(self, pil_image: Image.Image) -> np.ndarray:
        """Converte imagem PIL para formato OpenCV"""
        # Converter para RGB se necessário
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Converter para numpy array
        opencv_image = np.array(pil_image)
        
        # OpenCV usa BGR, PIL usa RGB
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
        
        return opencv_image
    
    def _cleanup_temp_files(self, temp_dir: str):
        """Remove arquivos temporários"""
        try:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"Arquivos temporários removidos: {temp_dir}")
        except Exception as e:
            logger.warning(f"Erro ao limpar arquivos temporários: {e}")
    
    def create_video(self, 
                    frames: List[Image.Image], 
                    output_path: str,
                    method: str = 'imageio') -> bool:
        """
        Cria vídeo usando o método especificado
        
        Args:
            frames: Lista de imagens PIL
            output_path: Caminho do arquivo de saída
            method: Método a usar ('opencv', 'imageio', 'ffmpeg')
            
        Returns:
            True se sucesso, False caso contrário
        """
        logger.info(f"Criando vídeo usando método: {method}")
        
        if method == 'opencv':
            return self.frames_to_video_opencv(frames, output_path)
        elif method == 'imageio':
            return self.frames_to_video_imageio(frames, output_path)
        elif method == 'ffmpeg':
            return self.frames_to_video_ffmpeg(frames, output_path)
        else:
            logger.error(f"Método não suportado: {method}")
            return False
    
    def save_frames_as_images(self, 
                            frames: List[Image.Image], 
                            output_dir: str,
                            prefix: str = "frame") -> bool:
        """
        Salva frames como imagens individuais
        
        Args:
            frames: Lista de imagens PIL
            output_dir: Diretório de saída
            prefix: Prefixo dos nomes dos arquivos
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            logger.info(f"Salvando {len(frames)} frames em: {output_dir}")
            
            for i, frame in enumerate(frames):
                filename = f"{prefix}_{i:04d}.png"
                filepath = os.path.join(output_dir, filename)
                frame.save(filepath)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Salvo {i + 1}/{len(frames)} frames")
            
            logger.info("Frames salvos com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar frames: {e}")
            return False
