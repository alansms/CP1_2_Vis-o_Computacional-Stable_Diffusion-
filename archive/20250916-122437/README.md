# Gerador de Vídeo com Stable Diffusion

Este projeto implementa um sistema para gerar vídeos a partir de imagens do Stable Diffusion, onde cada frame é gerado usando o frame anterior como entrada (retroalimentação). O sistema é otimizado com OpenVINO para melhor performance.

## Características

- ✅ Geração de vídeo com retroalimentação de frames
- ✅ Otimização com OpenVINO para melhor performance
- ✅ Suporte a múltiplos métodos de criação de vídeo (OpenCV, ImageIO, FFmpeg)
- ✅ Prompts animados para transições suaves
- ✅ Configuração flexível de parâmetros
- ✅ Salvamento de frames individuais
- ✅ Interface de linha de comando e programática

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Instalar FFmpeg (opcional, para melhor qualidade de vídeo)

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Baixe do site oficial: https://ffmpeg.org/download.html

## Uso

### Linha de Comando

#### Exemplo básico:
```bash
python main.py --prompt "A beautiful sunset over mountains" --frames 30 --output sunset_video.mp4
```

#### Exemplo com prompts animados:
```bash
python main.py \
  --prompt "A cat sitting in a garden" \
  --frame-prompts "A cat stretching" "A cat walking" "A cat running" "A cat jumping" \
  --frames 20 \
  --output cat_animation.mp4 \
  --fps 12
```

#### Exemplo com configurações avançadas:
```bash
python main.py \
  --prompt "A magical forest with glowing mushrooms" \
  --frames 25 \
  --width 768 \
  --height 768 \
  --steps 30 \
  --guidance 8.0 \
  --strength 0.6 \
  --fps 24 \
  --quality 9 \
  --method ffmpeg \
  --save-frames \
  --output magical_forest.mp4
```

### Uso Programático

```python
from stable_diffusion_pipeline import StableDiffusionVideoGenerator
from video_creator import VideoCreator

# Inicializar gerador
generator = StableDiffusionVideoGenerator(
    model_id="runwayml/stable-diffusion-v1-5",
    use_openvino=True
)

# Gerar frames
frames = generator.generate_video_frames(
    initial_prompt="A beautiful landscape",
    frame_prompts=[],
    num_frames=20,
    strength=0.7,
    seed=42
)

# Criar vídeo
video_creator = VideoCreator(fps=24, quality=8)
video_creator.create_video(frames, "output.mp4", method="imageio")

# Limpar recursos
generator.cleanup()
```

## Parâmetros

### Parâmetros Básicos
- `--prompt`: Prompt inicial para geração
- `--output`: Caminho do arquivo de vídeo de saída
- `--frames`: Número de frames a gerar
- `--model`: ID do modelo Stable Diffusion

### Parâmetros de Geração
- `--width/--height`: Dimensões das imagens (padrão: 512x512)
- `--steps`: Número de passos de inferência (padrão: 20)
- `--guidance`: Escala de orientação (padrão: 7.5)
- `--strength`: Força da transformação entre frames (0.0-1.0, padrão: 0.7)
- `--seed`: Semente para reprodutibilidade

### Parâmetros do Vídeo
- `--fps`: Frames por segundo (padrão: 24)
- `--quality`: Qualidade do vídeo 1-10 (padrão: 8)
- `--method`: Método de criação ('opencv', 'imageio', 'ffmpeg')

### Parâmetros Adicionais
- `--negative-prompt`: Prompt negativo
- `--save-frames`: Salvar frames individuais
- `--frames-dir`: Diretório para frames individuais
- `--frame-prompts`: Prompts específicos para cada frame

## Exemplos

Execute o arquivo de exemplos para ver diferentes casos de uso:

```bash
python example_usage.py
```

Os exemplos incluem:
1. **Vídeo básico**: Geração simples com um prompt
2. **Prompts animados**: Animação de um gato com prompts específicos
3. **Transição de estilo**: Mudança gradual entre estilos artísticos
4. **Salvamento de frames**: Salvamento de frames individuais

## Modelos Suportados

O sistema funciona com qualquer modelo Stable Diffusion compatível com Diffusers:

- `runwayml/stable-diffusion-v1-5` (padrão)
- `stabilityai/stable-diffusion-2-1`
- `stabilityai/stable-diffusion-xl-base-1.0`
- Modelos customizados locais

## Otimização OpenVINO

O OpenVINO é usado por padrão para otimizar a performance. Para desabilitar:

```bash
python main.py --no-openvino --prompt "your prompt here"
```

## Dicas para Melhores Resultados

### 1. Configuração de Strength
- **0.3-0.5**: Transições muito suaves, pouca mudança
- **0.6-0.7**: Transições equilibradas (recomendado)
- **0.8-0.9**: Mudanças mais dramáticas

### 2. Prompts Animados
Use prompts que descrevem sequências lógicas:
```python
frame_prompts = [
    "A person standing still",
    "A person starting to walk",
    "A person walking normally",
    "A person walking faster",
    "A person running"
]
```

### 3. Configuração de FPS
- **8-12 FPS**: Para transições de estilo
- **12-24 FPS**: Para animações suaves
- **24+ FPS**: Para movimento rápido

### 4. Qualidade vs Velocidade
- **Passos baixos (10-15)**: Mais rápido, qualidade menor
- **Passos médios (20-25)**: Equilíbrio
- **Passos altos (30+)**: Melhor qualidade, mais lento

## Solução de Problemas

### Erro de Memória
- Reduza as dimensões (`--width 256 --height 256`)
- Use menos passos (`--steps 10`)
- Desabilite OpenVINO se necessário

### Qualidade Baixa
- Aumente os passos (`--steps 30`)
- Ajuste a força (`--strength 0.6`)
- Use prompts mais específicos

### Vídeo com Artefatos
- Use método FFmpeg (`--method ffmpeg`)
- Aumente a qualidade (`--quality 10`)
- Verifique se FFmpeg está instalado

## Estrutura do Projeto

```
stable_diffusion_video_generator/
├── main.py                    # Script principal
├── stable_diffusion_pipeline.py  # Pipeline do Stable Diffusion
├── video_creator.py           # Criação de vídeo
├── example_usage.py          # Exemplos de uso
├── requirements.txt          # Dependências
└── README.md                # Este arquivo
```

## Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Agradecimentos

- HuggingFace pela biblioteca Diffusers
- Intel pelo OpenVINO
- Comunidade Stable Diffusion pelos modelos
