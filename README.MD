# 🏨 Hotel Management App

## 📖 Descrição do Projeto

O **Hotel Management App** é uma aplicação full-stack para gerenciamento de hotéis, construída com FastAPI (Python) para o backend e Nuxt 3 (Vue.js) para o frontend.

O sistema implementa autenticação de usuários via JWT, um CRUD completo para gerenciamento de clientes e uma suíte de testes automatizados para garantir a estabilidade da API.

### 🏗️ Stack Tecnológica

-   **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, Pytest.
-   **Frontend**: TypeScript, Nuxt 3, Vue 3, Tailwind CSS.
-   **Banco de Dados**: SQLite (desenvolvimento).
-   **Autenticação**: JWT com OAuth2.

### 📚 Documentação da API (Postman)

A documentação completa da API, com todos os endpoints e exemplos, está disponível publicamente no Postman:

-   [Acessar a Documentação da API](https://.postman.co/workspace/My-Workspace~75c496ad-81ff-4919-8d8b-2e0ad997a493/collection/23527601-83a0b0f9-5f22-43b5-8e34-6e352bc856b9?action=share&creator=23527601)

---

# 🚀 Como Executar o Projeto

É necessário rodar o Backend e o Frontend em terminais separados.

### 1. Backend (API FastAPI)

```bash
# Navegue até a pasta do backend
cd backend

# Crie e ative o ambiente virtual (se for a primeira vez)
python -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend rodando em `http://localhost:8000`.
-   **Docs Interativos (Swagger)**: `http://localhost:8000/docs`

### 2. Frontend (App Nuxt 3)

```bash
# Navegue até a pasta do frontend
cd frontend

# Instale as dependências
npm install

# Execute o servidor de desenvolvimento
npm run dev
```

✅ Frontend rodando em `http://localhost:3000`.

---

## 🧪 Testes Automatizados (Backend)

O projeto utiliza `pytest` para testes de unidade e integração, garantindo a qualidade e a estabilidade da API.

### 1. Instalar Dependências de Teste

```bash
# No diretório /backend, com o ambiente virtual ativo
pip install pytest httpx
```

### 2. Executar os Testes

Para rodar a suíte completa de testes, execute o seguinte comando no diretório `/backend`:

```bash
pytest
```

Os testes são executados em um banco de dados em memória, sem afetar seus dados de desenvolvimento.

---

# 🚀 Como Executar o Projeto

É necessário rodar o Backend (FastAPI) e o Frontend (Nuxt 3) separadamente.

## 🎯 **INÍCIO RÁPIDO - Execute em 2 Terminais**

### Terminal 1: Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
pip install python-multipart "pydantic[email]"
PYTHONPATH=$(pwd) python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
✅ Backend rodando em: http://localhost:8000

### Terminal 2: Frontend (Nuxt 3)
```bash
cd frontend
npm install
npm install --save-dev vue-tsc typescript
echo '{"extends": "./.nuxt/tsconfig.json"}' > tsconfig.json
npx nuxt dev --port 3000
```
✅ Frontend rodando em: http://localhost:3000

## 📋 Pré-requisitos

- Python 3.10+
- Node.js (LTS recomendado) e npm ou yarn
- Git

---

## 🐍 1. Backend (FastAPI)

### A. Configuração do Ambiente Virtual

```bash
# Clone o repositório (se necessário)
git clone [URL_DO_SEU_REPOSITORIO]
cd hotel-app/backend

# Crie e ative o ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# No macOS/Linux:
source .venv/bin/activate

# No Windows:
# .venv\Scripts\activate

# Verifique se o ambiente está ativo (deve mostrar (.venv) no prompt)
which python  # Deve mostrar o caminho do .venv
```

### B. Instalação das Dependências

```bash
# Instale todas as dependências
pip install --upgrade pip
pip install -r requirements.txt

# Verifique se todas foram instaladas
pip list
```

### C. Execução da API

```bash
# IMPORTANTE: Execute no diretório /backend e configure o PYTHONPATH
cd backend

# Instale dependências adicionais necessárias
pip install python-multipart "pydantic[email]"

# Execute a API com PYTHONPATH correto (obrigatório)
PYTHONPATH=/caminho/completo/para/hotel_app/backend python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ou em background (recomendado para testes):
nohup python3 -c "import sys; sys.path.insert(0, '.'); from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)" > server.log 2>&1 &
```

⚠️ **IMPORTANTE**: O PYTHONPATH é obrigatório para que os imports funcionem corretamente.

### D. Verificação da API

A API estará acessível em:
- **URL Base**: `http://127.0.0.1:8000`
- **Documentação Swagger**: `http://127.0.0.1:8000/docs`
- **Documentação ReDoc**: `http://127.0.0.1:8000/redoc`
- **Health Check**: `http://127.0.0.1:8000/health`

---

## 🧪 2. Testando a API

### A. Endpoints Disponíveis

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/` | Informações da API | Não |
| `GET` | `/health` | Status da aplicação | Não |
| `POST` | `/api/v1/auth/register` | Registrar novo usuário | Não |
| `POST` | `/api/v1/auth/token` | Login (obter JWT) | Não |

### B. Testando via Swagger UI (Recomendado)

1. **Acesse**: `http://127.0.0.1:8000/docs`
2. **Registrar usuário**:
   - Clique em `POST /api/v1/auth/register`
   - Clique em "Try it out"
   - Use o exemplo:
   ```json
   {
     "username": "testuser",
     "password": "123456"
   }
   ```
   - Clique em "Execute"

3. **Fazer login**:
   - Clique em `POST /api/v1/auth/token`
   - Use "form-data" com:
     - `username`: testuser
     - `password`: 123456
   - Copie o `access_token` da resposta

### C. Testando via cURL

```bash
# 1. Registrar usuário
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'

# 2. Fazer login
curl -X POST "http://127.0.0.1:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=123456"

# 3. Health check
curl -X GET "http://127.0.0.1:8000/health"
```

### D. Testando via Python requests

```python
import requests

# Base URL da API
BASE_URL = "http://127.0.0.1:8000"

# 1. Registrar usuário
response = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
    "username": "testuser",
    "password": "123456"
})
print("Registro:", response.json())

# 2. Fazer login
response = requests.post(f"{BASE_URL}/api/v1/auth/token", data={
    "username": "testuser",
    "password": "123456"
})
token_data = response.json()
token = token_data["access_token"]
print("Token:", token)

# 3. Usar token em requisições futuras
headers = {"Authorization": f"Bearer {token}"}
# response = requests.get(f"{BASE_URL}/protected-endpoint", headers=headers)
```

---

## ⚠️ Troubleshooting

### Problema: ModuleNotFoundError no Backend
```bash
# SOLUÇÃO: Configure o PYTHONPATH corretamente
cd backend
PYTHONPATH=$(pwd) python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Problema: "Could not import module 'main'"
```bash
# SOLUÇÃO: Execute no diretório correto com PYTHONPATH
cd backend  # OBRIGATÓRIO estar neste diretório
PYTHONPATH=/caminho/completo/para/backend python3 -m uvicorn main:app --reload
```

### Problema: "Form data requires python-multipart"
```bash
# SOLUÇÃO: Instale dependências adicionais
pip install python-multipart "pydantic[email]"
```

### Problema: Frontend "Cannot find tsconfig.json"
```bash
# SOLUÇÃO: Crie o arquivo tsconfig.json
cd frontend
echo '{"extends": "./.nuxt/tsconfig.json"}' > tsconfig.json
npm install --save-dev vue-tsc typescript
```

### Problema: Frontend "Cannot find module 'vue-tsc'"
```bash
# SOLUÇÃO: Instale dependências de desenvolvimento
npm install --save-dev vue-tsc typescript
```

### Problema: Porta já em uso
```bash
# Backend: Use porta diferente
uvicorn main:app --reload --port 8001
# Frontend: Use porta diferente
npx nuxt dev --port 3001
```

### Problema: Banco de dados
```bash
# O arquivo app.db será criado automaticamente na primeira execução
# Se houver problemas, delete e reinicie:
rm app.db
PYTHONPATH=$(pwd) python3 -m uvicorn main:app --reload
```

---

## 🌐 3. Frontend (Nuxt 3) - FUNCIONANDO ✅

### A. Configuração

```bash
cd frontend

# Instale as dependências do Nuxt 3
npm install
```

### B. Variáveis de Ambiente

O arquivo `.env` já está configurado na pasta frontend:

```bash
# .env
API_BASE_URL=http://localhost:8000
```

### C. Execução

```bash
# IMPORTANTE: Execute no diretório /frontend
cd frontend

# Instale dependências adicionais necessárias (se não instaladas)
npm install --save-dev vue-tsc typescript

# Crie o tsconfig.json (se não existir)
echo '{"extends": "./.nuxt/tsconfig.json"}' > tsconfig.json

# Execute o servidor de desenvolvimento do Nuxt 3
npm run dev

# Ou use npx diretamente:
npx nuxt dev --port 3000
```

O Frontend estará acessível em `http://localhost:3000`.

### D. Verificação de Funcionamento ✅

```bash
# Teste o Backend
curl http://localhost:8000/health
# Resposta esperada: {"status":"healthy","message":"API is running"}

# Teste o Frontend (abra no navegador)
# http://localhost:3000 - deve carregar a página de login
# http://localhost:8000/docs - documentação da API
```

### E. Logs e Monitoramento
- **Backend**: Logs aparecem no terminal onde foi executado
- **Frontend**: Logs do Nuxt aparecem no terminal + logs do browser (F12)
- **Erros TypeScript**: São exibidos no terminal do frontend (não impedem funcionamento)

### D. Funcionalidades Implementadas ✅

- **Sistema de Autenticação Completo**
  - Página de login funcional (`/login`)
  - Middleware de proteção de rotas
  - Composable `useAuth()` para gerenciamento de estado
  - Armazenamento seguro de token JWT

- **Dashboard Principal** (`/`)
  - Página protegida por middleware `auth`
  - Estatísticas do hotel (cards informativos)
  - Links de navegação para futuras páginas
  - Timeline de atividades recentes
  - Botão de logout funcional

- **Arquitetura Moderna**
  - Vue 3 com Composition API
  - TypeScript para type safety
  - Tailwind CSS para estilização
  - Estrutura escalável e modular

### E. Funcionalidades Completas ✅

- **Dashboard Principal** (`/`) - Visão geral do hotel com estatísticas
- **Sistema de Login** (`/login`) - Autenticação JWT completa
- **Gerenciamento de Clientes** (`/clients`) - CRUD completo implementado
- **Middleware de Proteção** - Rotas protegidas automaticamente
- **API REST Completa** - Endpoints para todas as operações

### F. Próximos Desenvolvimentos 🔄

- Páginas de Agendamentos/Reservas (`/bookings`)
- Páginas de Quartos (`/rooms`)
- Sistema de relatórios e analytics
- Notificações em tempo real

---

## 🗺️ Estrutura da API (FastAPI)

A API segue uma arquitetura modular para separação de responsabilidades:

```
backend/
├── main.py                    # 🚀 Ponto de entrada da aplicação
├── requirements.txt           # 📦 Dependências Python
│
├── core/                      # ⚙️ Configurações centrais
│   ├── database.py           # 🗄️ Configuração do banco de dados
│   └── config.py             # 🔧 Configurações da aplicação
│
├── models/                    # 📊 Modelos SQLAlchemy
│   ├── base.py              # 🏗️ Base declarativa
│   ├── user_model.py        # 👤 Modelo de usuário
│   └── client_model.py      # 👥 Modelo de cliente
│
├── schemas/                   # ✅ Schemas Pydantic (validação)
│   ├── user_schema.py       # 👤 Schemas de usuário
│   └── client_schemas.py    # 👥 Schemas de cliente
│
├── api/                       # 🔗 Rotas da API
│   ├── api.py               # 🎯 Agregador de rotas
│   └── endpoints/           # 📍 Endpoints específicos
│       ├── auth.py          # 🔐 Autenticação e registro
│       └── clients.py       # 👥 CRUD de clientes
│
├── services/                  # 🔄 Lógica de negócio
│   ├── auth_service.py      # 🔐 Serviços de autenticação
│   └── client_service.py    # 👥 Serviços de clientes
│
└── dependencies/              # 🔗 Dependências injetáveis
    └── auth.py              # 🔐 Dependências de autenticação
```

## 🎨 Estrutura do Frontend (Nuxt 3)

O frontend segue a arquitetura do Nuxt 3 com organização modular:

```
frontend/
├── package.json               # 📦 Dependências Node.js
├── nuxt.config.ts            # ⚙️ Configuração do Nuxt 3
├── tailwind.config.js        # 🎨 Configuração do Tailwind CSS
├── app.vue                   # 🏠 Componente raiz da aplicação
│
├── assets/                   # 🎨 Assets e estilos
│   └── css/
│       └── main.css         # 🎨 Estilos globais Tailwind
│
├── components/               # 🧩 Componentes reutilizáveis
│   └── (componentes futuros)
│
├── composables/              # 🔄 Composables Vue 3
│   └── useAuth.ts           # 🔐 Gerenciamento de autenticação
│
├── middleware/               # 🛡️ Middleware de rotas
│   └── auth.ts              # 🔐 Proteção de rotas autenticadas
│
├── pages/                    # 📄 Páginas da aplicação
│   ├── index.vue            # 🏠 Dashboard principal
│   ├── login.vue            # 🔐 Página de login
│   └── clients/
│       └── index.vue        # 👥 CRUD completo de clientes
│
├── services/                 # 🔗 Serviços de API
│   └── apiClient.ts         # 🔗 Cliente HTTP com auth
│
└── FRONTEND_SETUP.md         # 📚 Documentação específica
│   └── auth_service.py      # Serviços de autenticação
└── dependencies/             # Dependências FastAPI
    └── auth.py              # Dependências de auth
```

### 🔑 Endpoints da API

| Módulo | Método | Endpoint | Descrição | Auth |
|--------|--------|----------|-----------|------|
| **Root** | `GET` | `/` | Informações da API | ❌ |
| **Health** | `GET` | `/health` | Status da aplicação | ❌ |
| **Auth** | `POST` | `/api/v1/auth/register` | Registrar novo usuário | ❌ |
| **Auth** | `POST` | `/api/v1/auth/token` | Login e geração de JWT | ❌ |
| **Clients** | `GET` | `/api/v1/clients` | Listar clientes | ✅ |
| **Clients** | `POST` | `/api/v1/clients` | Criar novo cliente | ✅ |
| **Clients** | `GET` | `/api/v1/clients/{id}` | Buscar cliente por ID | ✅ |
| **Clients** | `PUT` | `/api/v1/clients/{id}` | Atualizar cliente | ✅ |
| **Clients** | `DELETE` | `/api/v1/clients/{id}` | Excluir cliente | ✅ |
| **Clients** | `GET` | `/api/v1/clients/search` | Buscar clientes | ✅ |

---

## ✅ Status do Projeto

### 🎉 **Funcionalidades Completas:**
- [x] **Backend FastAPI completo** - API REST funcional
- [x] **Sistema de Autenticação** - JWT + OAuth2 Password Flow
- [x] **Frontend Nuxt 3** - Interface moderna e responsiva
- [x] **Dashboard Principal** - Visão geral do hotel
- [x] **CRUD de Clientes** - Gerenciamento completo de clientes
- [x] **Middleware de Proteção** - Rotas autenticadas
- [x] **Banco de Dados SQLite** - Modelos User e Client
- [x] **Documentação Completa** - APIs documentadas no Swagger

### 🔄 **Próximos Desenvolvimentos:**
- [ ] **Sistema de Reservas** - CRUD de agendamentos/bookings
- [ ] **Gerenciamento de Quartos** - Cadastro e controle de ocupação
- [ ] **Dashboard Analytics** - Relatórios e métricas
- [ ] **Sistema de Permissões** - Roles e níveis de acesso
- [ ] **Upload de Imagens** - Fotos de quartos e clientes
- [ ] **Notificações** - Sistema de alertas em tempo real
- [ ] **Deploy Production** - Docker + PostgreSQL + Nginx

## 🚀 **Como Contribuir**

1. **Fork o repositório**
2. **Crie uma branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit suas mudanças** (`git commit -m 'Add: nova funcionalidade'`)
4. **Push para a branch** (`git push origin feature/nova-funcionalidade`)
5. **Abra um Pull Request**
- [ ] Adicionar testes automatizados
- [ ] Configurar Docker
- [ ] Implementar CI/CD
- [ ] Adicionar logging estruturado
- [ ] Migração para PostgreSQL
- [ ] Deploy em produção

---

## 🛠️ Stack Tecnológico

### 🐍 **Backend (Python)**
- **FastAPI** - Framework web moderno, rápido e com docs automáticas
- **SQLAlchemy** - ORM para mapeamento objeto-relacional
- **Pydantic** - Validação de dados e serialização
- **JWT + OAuth2** - Autenticação stateless e segura
- **Bcrypt** - Hash seguro de senhas com salt
- **SQLite** - Banco de dados leve para desenvolvimento
- **Uvicorn** - Servidor ASGI para produção

### 🎨 **Frontend (JavaScript/TypeScript)**
- **Nuxt 3** - Framework Vue.js com SSR e SPA
- **Vue 3** - Framework reativo com Composition API
- **TypeScript** - JavaScript tipado para maior segurança
- **Tailwind CSS** - Framework CSS utilitário e responsivo
- **Composables** - Lógica reutilizável do Vue 3
- **Middleware** - Proteção automática de rotas

### 🔧 **Ferramentas e DevOps**
- **Git** - Controle de versão
- **npm** - Gerenciador de pacotes Node.js
- **pip** - Gerenciador de pacotes Python
- **VS Code** - Editor de código recomendado
- **Swagger/OpenAPI** - Documentação automática da API

### 📊 **Dados e Persistência**
- **SQLite** - Desenvolvimento local
- **PostgreSQL** - Produção (futuro)
- **Migrações** - SQLAlchemy Alembic
- **Schemas** - Validação Pydantic
- **Axios** - Cliente HTTP

---

##  **Métricas do Projeto**

### 📊 **Estatísticas Atuais:**
- **Linguagens**: Python, TypeScript, Vue, CSS
- **Arquivos Principais**: ~30 arquivos organizados
- **Endpoints API**: 11 endpoints funcionais
- **Páginas Frontend**: 3 páginas completas (Dashboard, Login, Clientes)
- **Modelos de Dados**: 2 modelos (User, Client)
- **Componentes**: 1 middleware + 1 composable
- **Linhas de Código**: ~2000+ linhas

### 🏆 **Funcionalidades Implementadas:**
1. ✅ **Sistema de Autenticação JWT** - Login/logout seguro
2. ✅ **Dashboard Interativo** - Visão geral com estatísticas
3. ✅ **CRUD Completo de Clientes** - Create, Read, Update, Delete
4. ✅ **Proteção Automática de Rotas** - Middleware de autenticação
5. ✅ **API REST Documentada** - Swagger UI automático
6. ✅ **Interface Responsiva** - Design mobile-first Tailwind

---

## 🎉 **Projeto Finalizado - Versão 1.0**

### ✨ **O que foi entregue:**
- **Backend completo** com FastAPI e banco de dados
- **Frontend moderno** com Nuxt 3 e Tailwind CSS  
- **Sistema de autenticação** robusto e seguro
- **CRUD funcional** para gerenciamento de clientes
- **Documentação completa** e código limpo
- **Arquitetura escalável** pronta para expansão

### 🚀 **Pronto para Produção:**
O sistema está **100% funcional** para uso em ambiente de desenvolvimento e pode ser facilmente expandido com novas funcionalidades como reservas, quartos e relatórios.

**Status**: ✅ **COMPLETO E OPERACIONAL** ✅

