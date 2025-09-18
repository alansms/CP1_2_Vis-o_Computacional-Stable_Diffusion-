# 🚀 Guia de Deploy - Netlify

## ❌ **Problema Identificado: 404 Error**

O erro 404 no Netlify ocorreu porque a configuração estava incorreta. **JÁ CORRIGIDO!**

## ✅ **Solução Aplicada**

### **1. Configuração Corrigida**
- ✅ Movido `netlify.toml` para a raiz do projeto
- ✅ Configurado `publish = "web_app"`
- ✅ Commit e push realizados

### **2. Estrutura Correta**
```
stable_diffusion_video_generator/
├── netlify.toml          # ← NA RAIZ (corrigido)
├── web_app/              # ← Diretório de publicação
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── ...
```

## 🔧 **Como Corrigir no Netlify**

### **Método 1: Redeploy Automático**
1. O Netlify deve detectar automaticamente as mudanças
2. Aguarde o redeploy (2-3 minutos)
3. Acesse novamente o site

### **Método 2: Redeploy Manual**
1. Acesse [Netlify Dashboard](https://app.netlify.com)
2. Vá para o seu site
3. Clique em **"Deploys"**
4. Clique em **"Trigger deploy"** → **"Deploy site"**

### **Método 3: Verificar Configuração**
1. No Netlify Dashboard, vá para **"Site settings"**
2. Clique em **"Build & deploy"**
3. Verifique se está configurado:
   - **Publish directory**: `web_app`
   - **Build command**: `echo 'Static site - no build needed'`

## 🎯 **Configuração Final**

### **netlify.toml** (na raiz do projeto)
```toml
[build]
  publish = "web_app"
  command = "echo 'Static site - no build needed'"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

## 🧪 **Teste Local**

Para testar localmente antes do deploy:

```bash
# Navegar para a pasta web_app
cd web_app

# Executar servidor local
python -m http.server 8000

# Acessar: http://localhost:8000
```

## 📊 **Verificação do Deploy**

### **URLs para Testar**
- **Interface Principal**: `https://seu-site.netlify.app`
- **Demo Mode**: `https://seu-site.netlify.app/demo.html`

### **Funcionalidades para Testar**
- ✅ **Drag & Drop**: Upload de imagens
- ✅ **Seleção de Versão**: Botões Versão 1 e 2
- ✅ **Configurações**: Sliders de Frames, FPS, Qualidade
- ✅ **Geração**: Botão "Gerar Vídeo"
- ✅ **Download**: Download do vídeo gerado

## 🚨 **Se Ainda Houver Problemas**

### **1. Limpar Cache do Netlify**
```bash
# No Netlify Dashboard
Site settings → Build & deploy → Clear cache
```

### **2. Verificar Logs**
```bash
# No Netlify Dashboard
Deploys → Clique no deploy mais recente → View logs
```

### **3. Redeploy Completo**
```bash
# No Netlify Dashboard
Deploys → Trigger deploy → Clear cache and deploy site
```

## ✅ **Status Atual**

- ✅ **Configuração corrigida**
- ✅ **Arquivos commitados**
- ✅ **Push realizado**
- ✅ **Pronto para redeploy**

**O deploy deve funcionar corretamente agora!** 🎉
