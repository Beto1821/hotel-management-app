# 🔧 Configuração de Ambientes (Local vs Produção)

Este guia explica como alternar entre configurações de desenvolvimento local e produção.

## 📋 Estrutura de Arquivos de Ambiente

### Backend

- **`.env`** - Arquivo ativo (NÃO commitar - está no .gitignore) ⚠️
- **`.env.example`** - Template de referência (pode commitar) ✅
- **`.env.production`** - Configuração de produção (NÃO commitar) ⚠️

### Frontend

- **`.env`** - Arquivo ativo (NÃO commitar - está no .gitignore) ⚠️

---

## 🖥️ Backend

### 1. Configurar Variáveis de Ambiente

#### `.env` (Desenvolvimento Local)
```env
# Database - Desenvolvimento
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/HOTEL_APP

# JWT - Gerar com: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=sua-chave-de-desenvolvimento-32-chars-minimo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Desenvolvimento
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000

# Environment
ENVIRONMENT=development
```

#### `.env.production` (Produção)
```env
# Database - PRODUÇÃO
DATABASE_URL=mysql+pymysql://usuario_prod:senha_forte_prod@localhost:3306/HOTEL_APP

# JWT - GERAR NOVA SECRET_KEY FORTE!
SECRET_KEY=use-python-c-import-secrets-print-secrets-token-urlsafe-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Produção
ALLOWED_ORIGINS=https://plataformahotel.online,https://www.plataformahotel.online

# Environment
ENVIRONMENT=production
```

### 2. Alternar entre Ambientes (Backend)

**Para Desenvolvimento Local:**
```bash
cd backend

# Criar .env baseado no .env.example
cp .env.example .env
nano .env  # Editar com suas credenciais locais

# Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Iniciar servidor de desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Para Produção (no servidor):**
```bash
cd backend

# Copiar configuração de produção
cp .env.production .env
nano .env  # Configurar credenciais de produção

# Reiniciar serviço
sudo systemctl restart hotel-api
# OU com PM2:
pm2 restart hotel-api
```

---

## 🌐 Frontend

### 1. Configurar `.env`

#### Desenvolvimento Local
```env
# API Base URL - Local Development
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
# OU
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

#### Produção
```env
# API Base URL - Production
NUXT_PUBLIC_API_BASE_URL=https://plataformahotel.online/api/v1
# OU se API estiver em subdomínio:
NUXT_PUBLIC_API_BASE_URL=https://api.plataformahotel.online/api/v1
```

### 2. Alternar entre Ambientes (Frontend)

**Para Desenvolvimento Local:**

Edite `frontend/.env`:
```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

Depois reinicie:
```bash
cd frontend
# Ctrl+C para parar
npm run dev
```

**Para Produção:**

Edite `frontend/.env`:
```env
NUXT_PUBLIC_API_BASE_URL=https://plataformahotel.online/api/v1
```

Depois faça build e deploy:
```bash
cd frontend
npm install
npm run build

# Deploy com PM2
pm2 restart hotel-frontend

# OU deploy com servidor web estático
# Copiar pasta .output/public para servidor
```

---

## 🔐 Segurança - IMPORTANTE!

### ⚠️ Arquivos que NÃO devem ir para o Git (já estão no .gitignore):

- ✅ `.env` (backend e frontend) - **NUNCA COMMITAR!**
- ✅ `.env.production` - **NUNCA COMMITAR!**
- ✅ `.env.local` - **NUNCA COMMITAR!**
- ✅ Qualquer arquivo com senhas ou chaves reais

### ✅ Arquivos que podem (e devem) ir para o Git:

- ✅ `.env.example` - Template sem valores sensíveis
- ✅ `CONFIGURACAO_AMBIENTE.md` - Este arquivo de documentação

### 🔑 Como gerar SECRET_KEY segura:

```bash
# No terminal:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copie o resultado e cole no .env:
# SECRET_KEY=resultado_gerado_aqui
```

---

## 📝 Checklist de Deploy

### Antes de fazer Deploy para Produção:

- [ ] **Gerar SECRET_KEY forte** (32+ caracteres)
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] Alterar `DATABASE_URL` no `.env` de produção
- [ ] Configurar `ALLOWED_ORIGINS` com domínios de produção
- [ ] Definir `ENVIRONMENT=production`
- [ ] Verificar `NUXT_PUBLIC_API_BASE_URL` no frontend
- [ ] Testar localmente antes com `.env.example`
- [ ] Fazer backup do banco de dados de produção
- [ ] Garantir que `.env` NÃO está no Git
- [ ] Commitar código (apenas `.env.example`)
- [ ] SSH no servidor
- [ ] `git pull origin main`
- [ ] Copiar `.env.production` para `.env` no servidor
- [ ] Editar `.env` com credenciais reais
- [ ] Reiniciar serviços:
  ```bash
  sudo systemctl restart hotel-api  # Backend
  # OU
  pm2 restart hotel-api
  
  # Frontend
  cd frontend && npm run build
  pm2 restart hotel-frontend
  ```
- [ ] Testar em produção
- [ ] Verificar logs para erros

---

## 🚀 Comandos Rápidos

### Local (Desenvolvimento)

```bash
# Backend
cd backend
cp .env.example .env
nano .env  # Configurar DATABASE_URL, SECRET_KEY, etc.
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (outro terminal)
cd frontend
nano .env  # NUXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
npm run dev
```

### Produção (Deploy no Servidor)

```bash
# SSH no servidor
ssh usuario@seu-servidor.com

# Atualizar código
cd ~/caminho/projeto
git pull origin main

# Backend
cd backend
cp .env.production .env
nano .env  # Editar credenciais reais de produção
sudo systemctl restart hotel-api

# Frontend
cd ../frontend
nano .env  # NUXT_PUBLIC_API_BASE_URL=https://plataformahotel.online/api/v1
npm install
npm run build
sudo systemctl restart hotel-frontend
# OU pm2 restart hotel-frontend
```

---

## 🔑 Credenciais de Teste

### Local (Desenvolvimento)
- **Username:** `teste`
- **Password:** `teste123`

### Produção
- Criar usuários via SSH no banco de dados MySQL do servidor
- Usar senhas fortes para produção

---

## 💡 Dicas

1. **Nunca commite arquivos `.env`** - Eles contêm informações sensíveis
2. **Use senhas diferentes** para local e produção
3. **Teste sempre localmente** antes de fazer deploy
4. **Faça backup** do banco de dados antes de alterações importantes
5. **Documente mudanças** importantes nos arquivos de configuração

---

## 🆘 Troubleshooting

### Backend não inicia - "SECRET_KEY não definida"
**Causa:** Arquivo `.env` não existe ou SECRET_KEY não está definida  
**Solução:**
```bash
cd backend
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copiar resultado e colar em SECRET_KEY no .env
```

### Frontend não conecta ao backend
**Causa:** `NUXT_PUBLIC_API_BASE_URL` incorreta no `.env`  
**Solução:**
```bash
cd frontend
nano .env
# Verificar URL: http://localhost:8000/api/v1 (dev) ou https://... (prod)
# Reiniciar: Ctrl+C e npm run dev
```

### Erro 401 (Unauthorized)
**Causa:** Token inválido ou SECRET_KEY diferente  
**Solução:**
- Verificar se SECRET_KEY é a mesma no backend
- Fazer logout e login novamente
- Verificar se usuário existe no banco correto

### Banco de dados não conecta
**Causa:** DATABASE_URL incorreta ou MySQL não rodando  
**Solução:**
```bash
# Verificar MySQL
sudo systemctl status mysql
# OU
mysql -u root -p

# Verificar DATABASE_URL no .env
nano backend/.env
# Formato: mysql+pymysql://usuario:senha@host:porta/banco
```

### CORS Error no frontend
**Causa:** Origem não permitida em ALLOWED_ORIGINS  
**Solução:**
```bash
# Adicionar origem em backend/.env
nano backend/.env
# ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,...
# Reiniciar backend
```
