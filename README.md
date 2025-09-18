# 🎬 Stable Diffusion Video Generator

Interface web moderna para geração de vídeos com movimento real usando Stable Diffusion e retroalimentação de frames.

## ✨ Funcionalidades

### 🎯 **Geração de Vídeo com IA**
- **Retroalimentação Real**: Cada frame gera o próximo usando Img2Img
- **Duas Versões Otimizadas**:
  - **Versão 1**: Continuidade + Movimento Progressivo
  - **Versão 2**: Interpolação Avançada
- **Movimento Natural**: Homer Simpson com poses e expressões reais
- **Qualidade Configurável**: Rápida, Balanceada, Alta

### 🖥️ **Interface Web Moderna**
- **Drag & Drop**: Upload intuitivo de imagens
- **Design Responsivo**: Mobile-first, gradiente moderno
- **Configurações Flexíveis**: Frames (4-12), FPS (8-24), Qualidade
- **Preview em Tempo Real**: Visualização da imagem selecionada
- **Progress Bar**: Acompanhamento da geração

### 🚀 **Deploy Automático**
- **Netlify Ready**: Configuração completa para deploy
- **GitHub Actions**: CI/CD automático
- **Funções Serverless**: Backend com Netlify Functions
- **Demo Mode**: Teste local sem backend

## 🏗️ Arquitetura do Projeto

```
stable_diffusion_video_generator/
├── 📁 web_app/                    # Interface web
│   ├── index.html                 # Página principal
│   ├── demo.html                  # Versão demo
│   ├── styles.css                 # CSS moderno
│   ├── script.js                  # JavaScript completo
│   ├── netlify.toml               # Configuração Netlify
│   ├── package.json               # Dependências
│   └── netlify/functions/         # Backend functions
├── 📁 colab_sd_video_*.ipynb      # Notebooks Jupyter
├── 📁 output/                     # Vídeos gerados
├── 📁 frames/                     # Frames intermediários
└── 📁 temp/                       # Arquivos temporários
```

## 🎯 Versões do Stable Diffusion

### **Versão 1: Continuidade + Movimento Progressivo**
```python
# Strength progressivo: 0.6 → 0.8 → 0.65
# Sequência suave entre poses
# Mantém identidade do personagem
progressive_sequence = [
    "arms slightly lowered, same expression",
    "arms down, relaxed pose, gentle movement", 
    "right arm pointing forward, left arm down",
    "both arms raised to shoulder height, excited",
    "both arms raised high, very excited, jumping",
    "hands on hips, confident pose",
    "arms crossed, thinking pose",
    "original pose, arms raised, returning"
]
```

### **Versão 2: Interpolação Avançada**
```python
# Strength variável: 0.5 → 0.8 → 0.5
# 10 frames com poses-chave
# Interpolação entre extremos
key_poses = [
    "original pose, arms raised",
    "arms slightly lowered, transition",
    "arms down, relaxed, gentle movement",
    "right arm pointing, left arm down",
    "both arms to shoulders, excited",
    "both arms raised high, very excited",
    "hands on hips, confident",
    "arms crossed, thinking",
    "returning to original, arms up",
    "original pose, arms raised"
]
```

## 🚀 Como Usar

### **Desenvolvimento Local**

```bash
# Clone o repositório
git clone https://github.com/alansms/CP1_2_Vis-o_Computacional-Stable_Diffusion-.git
cd stable_diffusion_video_generator

# Navegar para interface web
cd web_app

# Executar servidor local
python -m http.server 8000
# Acesse: http://localhost:8000
```

### **Deploy no Netlify**

#### **Método 1: Dashboard Netlify**
1. Acesse [Netlify Dashboard](https://app.netlify.com)
2. "New site from Git"
3. Conecte o repositório GitHub
4. Configure:
   - **Build command**: `echo 'Static site - no build needed'`
   - **Publish directory**: `web_app`
5. Deploy automático!

#### **Método 2: Netlify CLI**
```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Login no Netlify
netlify login

# Deploy
cd web_app
netlify deploy --prod
```

### **Uso da Interface**

1. **Upload de Imagem**:
   - Arraste uma imagem para a área central
   - Ou clique para selecionar arquivo
   - Formatos suportados: PNG, JPG, JPEG

2. **Seleção de Versão**:
   - **Versão 1**: Movimento progressivo e suave
   - **Versão 2**: Interpolação avançada

3. **Configurações**:
   - **Frames**: 4-12 (padrão: 8)
   - **FPS**: 8-24 (padrão: 12)
   - **Qualidade**: Rápida (256x256), Balanceada (512x512), Alta (768x768)

4. **Geração**:
   - Clique em "Gerar Vídeo"
   - Acompanhe o progresso
   - Baixe o resultado

## 🧪 Notebooks Jupyter

### **Notebooks Disponíveis**

1. **`colab_sd_video_continuidade.ipynb`**
   - Versão corrigida sem distorção
   - Continuidade + movimento progressivo
   - Strength: 0.35-0.6

2. **`colab_sd_video_movimento_real.ipynb`**
   - Movimento dramático
   - Strength alto (0.75)
   - Poses extremas

3. **`colab_sd_video_fast.ipynb`**
   - Versão otimizada para velocidade
   - 2-4 minutos total
   - Dimensões menores

### **Executar Notebooks**

```bash
# Jupyter Notebook
jupyter notebook

# Google Colab
# Upload para https://colab.research.google.com
```

## ⚙️ Configurações Técnicas

### **Stable Diffusion**
- **Modelo**: `runwayml/stable-diffusion-v1-5`
- **Pipeline**: `StableDiffusionImg2ImgPipeline`
- **Scheduler**: `DPMSolverMultistepScheduler`
- **Device**: CUDA (se disponível) ou CPU

### **Otimizações**
- **Attention Slicing**: Reduz VRAM
- **Memory Efficient Attention**: Otimização de memória
- **Float16**: Precisão otimizada para GPU
- **Batch Processing**: Processamento eficiente

### **Parâmetros Otimizados**
```python
# Configuração balanceada
width, height = 512, 512
steps = 20
guidance_scale = 7.5
strength = 0.6  # Versão 1
strength = 0.8  # Versão 2 (movimento dramático)
```

## 📊 Performance

### **Tempos de Geração**

| Configuração | Tempo Total | Qualidade | Uso |
|-------------|-------------|-----------|-----|
| **Rápida** | 2-4 min | Boa | Testes |
| **Balanceada** | 4-6 min | Muito boa | Uso regular |
| **Alta** | 8-12 min | Excelente | Produção |

### **Requisitos de Sistema**

- **GPU**: NVIDIA RTX 3060+ (recomendado)
- **RAM**: 8GB+ (16GB+ recomendado)
- **VRAM**: 6GB+ para GPU
- **CPU**: 4+ cores (fallback)

## 🔧 Troubleshooting

### **Problemas Comuns**

1. **Out of Memory**:
   ```python
   # Reduzir dimensões
   width, height = 256, 256
   # Ou usar CPU
   device = "cpu"
   ```

2. **Frames Distorcidos**:
   ```python
   # Reduzir strength
   strength = 0.3-0.4
   # Melhorar negative prompts
   negative_prompt = "blurry, low quality, distorted, deformed"
   ```

3. **Falta de Movimento**:
   ```python
   # Aumentar strength
   strength = 0.7-0.8
   # Usar prompts específicos
   prompt = "Homer Simpson, both arms raised high, excited"
   ```

### **Logs e Debug**

```python
# Habilitar logs detalhados
import logging
logging.basicConfig(level=logging.INFO)

# Verificar device
print(f"Device: {device}")
print(f"CUDA available: {torch.cuda.is_available()}")
```

## 📈 Resultados Esperados

### **Versão 1: Continuidade**
- ✅ Movimento suave e natural
- ✅ Mantém identidade do personagem
- ✅ Transições fluidas
- ✅ Sem distorções

### **Versão 2: Interpolação**
- ✅ Movimento dramático
- ✅ Poses extremas
- ✅ Expressões variadas
- ✅ Sequência completa

## 🤝 Contribuição

### **Como Contribuir**

1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra** um Pull Request

### **Áreas de Melhoria**

- [ ] Novos modelos de Stable Diffusion
- [ ] Otimizações de performance
- [ ] Interface mobile melhorada
- [ ] Novos tipos de movimento
- [ ] Integração com outros modelos

## 📄 Licença

MIT License - Use livremente para projetos pessoais e comerciais.

## 🔗 Links Úteis

- [Stable Diffusion](https://huggingface.co/runwayml/stable-diffusion-v1-5)
- [Diffusers Library](https://github.com/huggingface/diffusers)
- [Netlify](https://netlify.com)
- [Google Colab](https://colab.research.google.com)

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/alansms/CP1_2_Vis-o_Computacional-Stable_Diffusion-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/alansms/CP1_2_Vis-o_Computacional-Stable_Diffusion-/discussions)

---

**🎉 Desenvolvido com ❤️ usando Stable Diffusion e IA Generativa**

*Interface web moderna + Notebooks Jupyter + Deploy automático no Netlify*
