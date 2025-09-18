# 🚀 Guia de Deploy - Stable Diffusion Video Generator

## 📋 Pré-requisitos

- Conta no [Netlify](https://netlify.com)
- Repositório no GitHub
- Node.js 18+ (para desenvolvimento local)

## 🎯 Deploy Rápido no Netlify

### 1. Conectar Repositório

1. Acesse [Netlify Dashboard](https://app.netlify.com)
2. Clique em **"New site from Git"**
3. Conecte sua conta GitHub
4. Selecione o repositório `stable_diffusion_video_generator`
5. Configure as seguintes opções:

```
Build command: echo 'Static site - no build needed'
Publish directory: web_app
```

### 2. Configurar Variáveis de Ambiente

No painel do Netlify, vá em **Site settings > Environment variables** e adicione:

```
PYTHON_VERSION=3.11
PIP_VERSION=23.0
```

### 3. Deploy Automático

- Push para `main` → Deploy automático
- Pull Request → Preview automático

## 🔧 Configuração Avançada

### Netlify Functions (Backend)

Para funcionalidade completa, configure as Netlify Functions:

1. **Instalar dependências Python**:
```bash
# Criar requirements.txt na raiz
echo "diffusers==0.30.0
transformers==4.35.0
accelerate==0.24.0
safetensors==0.4.0
pillow==10.0.0
imageio==2.31.0
torch==2.1.0" > requirements.txt
```

2. **Configurar netlify.toml**:
```toml
[build]
  command = "pip install -r requirements.txt"
  functions = "netlify/functions"

[[plugins]]
  package = "@netlify/plugin-python"
```

3. **Deploy da função**:
```bash
# A função generate-video.js já está configurada
# Ela será automaticamente deployada
```

### GitHub Actions (Opcional)

Para CI/CD automático:

1. **Configurar secrets no GitHub**:
   - `NETLIFY_AUTH_TOKEN`: Token do Netlify
   - `NETLIFY_SITE_ID`: ID do site

2. **Workflow já configurado**:
   - Deploy automático em push para main
   - Preview em Pull Requests

## 🧪 Teste Local

### Desenvolvimento

```bash
# Navegar para o diretório
cd web_app

# Instalar dependências
npm install

# Executar servidor local
npm run dev
# ou
python -m http.server 8000
```

### Demo Mode

```bash
# Abrir demo.html no navegador
open demo.html
```

## 📱 URLs de Deploy

Após o deploy, você terá:

- **Produção**: `https://seu-site.netlify.app`
- **Preview**: `https://deploy-preview-123--seu-site.netlify.app`
- **Demo**: `https://seu-site.netlify.app/demo.html`

## 🔍 Verificação do Deploy

### Checklist

- [ ] Site carrega corretamente
- [ ] Drag & drop funciona
- [ ] Versões 1 e 2 selecionáveis
- [ ] Configurações funcionam
- [ ] Preview de imagem funciona
- [ ] Botão gerar ativa/desativa corretamente

### Teste de Funcionalidade

1. **Upload de imagem**:
   - Drag & drop
   - Click to upload
   - Preview

2. **Configurações**:
   - Sliders de frames e FPS
   - Selector de qualidade
   - Valores atualizados

3. **Geração**:
   - Progress bar
   - Simulação de progresso
   - Resultado (demo)

## 🐛 Troubleshooting

### Problemas Comuns

1. **Build falha**:
   ```bash
   # Verificar netlify.toml
   # Verificar package.json
   # Verificar dependências
   ```

2. **Functions não funcionam**:
   ```bash
   # Verificar netlify/functions/
   # Verificar logs no Netlify
   # Testar localmente
   ```

3. **CORS errors**:
   ```bash
   # Verificar headers no netlify.toml
   # Verificar fetch URLs
   ```

### Logs

- **Netlify**: Site settings > Functions > View logs
- **GitHub Actions**: Actions tab no repositório
- **Browser**: F12 > Console

## 🚀 Otimizações

### Performance

1. **CDN**: Netlify CDN automático
2. **Caching**: Headers configurados
3. **Compression**: Gzip automático
4. **Images**: Otimização automática

### SEO

1. **Meta tags**: Configuradas no HTML
2. **Sitemap**: Gerado automaticamente
3. **Robots.txt**: Configurado
4. **Analytics**: Google Analytics ready

## 📊 Monitoramento

### Netlify Analytics

- Page views
- Function invocations
- Build times
- Error rates

### Custom Analytics

```javascript
// Adicionar ao script.js
gtag('event', 'video_generated', {
  'version': selectedVersion,
  'frames': framesSlider.value,
  'quality': qualitySelect.value
});
```

## 🔄 Updates

### Deploy de Updates

```bash
# 1. Fazer mudanças no código
git add .
git commit -m "Update: Nova funcionalidade"
git push origin main

# 2. Deploy automático via Netlify
# 3. Verificar em https://app.netlify.com
```

### Rollback

```bash
# No Netlify Dashboard
# Site settings > Deploys
# Clicar em "Deploy" em uma versão anterior
```

## 📞 Suporte

- **Netlify Docs**: https://docs.netlify.com
- **GitHub Issues**: Criar issue no repositório
- **Community**: Netlify Community Forum

---

**🎉 Parabéns! Seu app está no ar!**

Acesse: `https://seu-site.netlify.app`
