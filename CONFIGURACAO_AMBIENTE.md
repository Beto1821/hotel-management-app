# 🔧 Configuração de Ambientes (Local vs Produção)

Este guia explica como alternar entre configurações de desenvolvimento local e produção.

## 📋 Estrutura de Arquivos de Ambiente

### Backend

- **`.env`** - Arquivo ativo (NÃO commitar - está no .gitignore)
- **`.env.local`** - Template para desenvolvimento local
- **`.env.production`** - Template para produção

### Frontend

- **`.env`** - Arquivo ativo (NÃO commitar - está no .gitignore)

---

## 🖥️ Backend

### 1. Configurar Variáveis de Ambiente

#### `.env.local` (Desenvolvimento Local)
```env
# Database
DB_USER=root
DB_PASSWORD=sua_senha_mysql_local
DB_HOST=localhost
DB_PORT=3306
DB_NAME=HOTEL_APP

# JWT
SECRET_KEY=your-secret-key-for-development
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Pool de Conexões
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

#### `.env.production` (Produção)
```env
# Database
DB_USER=seu_usuario_producao
DB_PASSWORD=senha_super_segura_producao
DB_HOST=localhost
DB_PORT=3306
DB_NAME=HOTEL_APP

# JWT
SECRET_KEY=chave-secreta-super-segura-de-producao-mudar-isto
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Pool de Conexões
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### 2. Alternar entre Ambientes (Backend)

**Para Desenvolvimento Local:**
```bash
cd backend
cp .env.local .env
uvicorn main:app --reload
```

**Para Produção:**
```bash
cd backend
cp .env.production .env
pm2 restart hotel-api
```

---

## 🌐 Frontend

### 1. Configurar `.env`

#### Desenvolvimento Local
```env
# API Base URL - Local Development
NUXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

#### Produção
```env
# API Base URL - Production
NUXT_PUBLIC_API_URL=https://plataformahotel.online
```

### 2. Alternar entre Ambientes (Frontend)

**Para Desenvolvimento Local:**

Edite `frontend/.env`:
```env
NUXT_PUBLIC_API_URL=http://127.0.0.1:8000
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
NUXT_PUBLIC_API_URL=https://plataformahotel.online
```

Depois faça build e deploy:
```bash
cd frontend
npm run build
pm2 restart hotel-frontend
```

---

## 🔐 Segurança - IMPORTANTE!

### Arquivos que NÃO devem ir para o Git (já estão no .gitignore):

- ✅ `.env` (backend e frontend)
- ✅ `.env.local`
- ✅ `.env.production`
- ✅ Qualquer arquivo com senhas ou chaves

### Arquivos que podem ir para o Git:

- ✅ `.env.example` (template sem valores sensíveis)

---

## 📝 Checklist de Deploy

### Antes de fazer Deploy para Produção:

- [ ] Alterar `SECRET_KEY` no `.env.production` para uma chave segura
- [ ] Verificar credenciais do banco de dados
- [ ] Testar localmente antes
- [ ] Fazer backup do banco de dados de produção
- [ ] Commitar código (sem arquivos `.env`)
- [ ] SSH no servidor
- [ ] `git pull origin main`
- [ ] Copiar `.env.production` para `.env` no servidor
- [ ] `pm2 restart hotel-api`
- [ ] `pm2 restart hotel-frontend`
- [ ] Testar em produção

---

## 🚀 Comandos Rápidos

### Local (Desenvolvimento)

```bash
# Backend
cd backend
cp .env.local .env
uvicorn main:app --reload

# Frontend (outro terminal)
cd frontend
# Editar .env para usar http://127.0.0.1:8000
npm run dev
```

### Produção (Deploy)

```bash
# SSH no servidor
ssh u119-3ggbuuczowkc@srv1139419.hstgr.cloud

# Ir para o diretório do projeto
cd ~/hotel_app

# Atualizar código
git pull origin main

# Backend
cd backend
cp .env.production .env
pm2 restart hotel-api

# Frontend
cd ../frontend
# Verificar .env aponta para https://plataformahotel.online
npm run build
pm2 restart hotel-frontend
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

### Frontend não conecta ao backend
- Verificar `NUXT_PUBLIC_API_URL` no `.env` do frontend
- Reiniciar o servidor frontend após alterar `.env`

### Erro 401 (Unauthorized)
- Verificar se o usuário existe no banco correto (local ou produção)
- Verificar se a `SECRET_KEY` é a mesma em todos os arquivos de auth

### Banco de dados não conecta
- Verificar credenciais no `.env`
- Verificar se o MySQL está rodando
- Verificar se o banco `HOTEL_APP` existe
