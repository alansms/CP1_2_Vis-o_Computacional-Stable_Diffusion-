# 🎬 Stable Diffusion Video Generator

Interface web moderna para geração de vídeos com movimento real usando Stable Diffusion.

## ✨ Funcionalidades

- **Drag & Drop**: Interface intuitiva para upload de imagens
- **Duas Versões**: 
  - Versão 1: Continuidade + Movimento Progressivo
  - Versão 2: Interpolação Avançada
- **Configurações Flexíveis**: Frames, FPS, Qualidade
- **Interface Moderna**: Design responsivo e limpo
- **Deploy no Netlify**: Pronto para produção

## 🚀 Como Usar

### Desenvolvimento Local

```bash
# Navegar para o diretório
cd web_app

# Instalar dependências
npm install

# Executar servidor local
npm run dev
```

### Deploy no Netlify

1. **Conectar repositório GitHub**:
   - Acesse [Netlify](https://netlify.com)
   - Conecte seu repositório GitHub
   - Configure o build settings:
     - Build command: `echo 'Static site - no build needed'`
     - Publish directory: `web_app`

2. **Deploy manual**:
   ```bash
   # Instalar Netlify CLI
   npm install -g netlify-cli
   
   # Login no Netlify
   netlify login
   
   # Deploy
   npm run deploy
   ```

## 🏗️ Estrutura do Projeto

```
web_app/
├── index.html          # Página principal
├── styles.css          # Estilos CSS
├── script.js           # JavaScript
├── netlify.toml        # Configuração Netlify
├── package.json        # Dependências
└── README.md          # Documentação
```

## 🎯 Funcionalidades da Interface

### Upload de Imagens
- **Drag & Drop**: Arraste imagens diretamente
- **Click to Upload**: Clique para selecionar arquivo
- **Preview**: Visualização da imagem selecionada
- **Validação**: Tipos de arquivo e tamanho

### Versões Disponíveis
- **Versão 1**: Continuidade + Movimento Progressivo
  - Strength progressivo (0.6 → 0.8 → 0.65)
  - Transições suaves entre poses
  - Mantém identidade do personagem

- **Versão 2**: Interpolação Avançada
  - 10 frames com poses-chave
  - Strength variável (0.5 → 0.8 → 0.5)
  - Interpolação entre extremos

### Configurações
- **Frames**: 4-12 frames (padrão: 8)
- **FPS**: 8-24 FPS (padrão: 12)
- **Qualidade**: Rápida, Balanceada, Alta

### Geração de Vídeo
- **Progress Bar**: Acompanhamento do progresso
- **Preview**: Visualização do vídeo gerado
- **Download**: Baixar vídeo em MP4

## 🔧 Integração com Backend

Para conectar com o Stable Diffusion:

1. **Modifique `script.js`**:
   ```javascript
   async function callGenerationAPI(formData) {
     const response = await fetch('/api/generate-video', {
       method: 'POST',
       body: formData
     });
     return await response.json();
   }
   ```

2. **Crie função Netlify**:
   ```javascript
   // netlify/functions/generate-video.js
   exports.handler = async (event, context) => {
     // Processar imagem com Stable Diffusion
     // Retornar vídeo gerado
   };
   ```

## 🎨 Design

- **Gradiente Moderno**: Background com gradiente azul/roxo
- **Cards Elevados**: Sombras e bordas arredondadas
- **Animações Suaves**: Transições CSS
- **Responsivo**: Mobile-first design
- **Ícones FontAwesome**: Interface visual rica

## 📱 Responsividade

- **Mobile**: Layout adaptado para telas pequenas
- **Tablet**: Grid responsivo para configurações
- **Desktop**: Layout completo com todas as funcionalidades

## 🚀 Deploy Rápido

1. **Fork este repositório**
2. **Conecte ao Netlify**
3. **Configure build settings**:
   - Build command: `echo 'Static site - no build needed'`
   - Publish directory: `web_app`
4. **Deploy automático**!

## 🔗 Links Úteis

- [Netlify](https://netlify.com)
- [Stable Diffusion](https://huggingface.co/runwayml/stable-diffusion-v1-5)
- [FontAwesome](https://fontawesome.com)

## 📄 Licença

MIT License - Use livremente para projetos pessoais e comerciais.
