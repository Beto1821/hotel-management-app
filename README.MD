# 🏨 Hotel Management App

## 📖 Descrição do Projeto

O **Hotel Management App** é uma aplicação completa para gerenciamento de hotéis, desenvolvida com tecnologias modernas e arquitetura escalável. O sistema permite o cadastro de usuários, autenticação segura via JWT, e futuramente incluirá funcionalidades para reservas, clientes e inventário de quartos.

### 🎯 **Objetivos**
- Gerenciar reservas de quartos de hotel
- Controlar cadastro de clientes
- Sistema de autenticação seguro
- Interface web moderna e responsiva
- API REST completa e documentada

### 🏗️ **Arquitetura**
- **Backend**: FastAPI (Python) com SQLAlchemy e SQLite
- **Frontend**: Next.js (React/TypeScript) 
- **Autenticação**: JWT com OAuth2 Bearer
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)

---

# 🚀 Como Executar o Projeto

É necessário rodar o Backend (API) e o Frontend (Next.js) separadamente.

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
# Execute a API (o --reload é para desenvolvimento)
uvicorn main:app --reload

# Ou alternativamente:
# python -m uvicorn main:app --reload
```

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

### Problema: ModuleNotFoundError
```bash
# Certifique-se de que o ambiente virtual está ativo
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Reinstale as dependências
pip install -r requirements.txt
```

### Problema: Porta já em uso
```bash
# Use uma porta diferente
uvicorn main:app --reload --port 8001
```

### Problema: Banco de dados
```bash
# O arquivo app.db será criado automaticamente na primeira execução
# Se houver problemas, delete e reinicie:
rm app.db
uvicorn main:app --reload
```

---

## 🌐 3. Frontend (Next.js) - EM DESENVOLVIMENTO

### A. Configuração

```bash
cd ../frontend

# Instale as dependências
npm install # ou yarn install
```

### B. Variáveis de Ambiente

Crie um arquivo `.env.local` na raiz do frontend:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### C. Execução

```bash
# Execute o ambiente de desenvolvimento do Next.js
npm run dev # ou yarn dev
```

O Frontend estará acessível em `http://localhost:3000`.

---

## 🗺️ Estrutura da API (FastAPI)

A API segue uma arquitetura modular para separação de responsabilidades:

```
backend/
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── core/                      # Configurações centrais
│   ├── database.py           # Configuração do banco de dados
│   └── config.py             # Configurações da aplicação
├── models/                    # Modelos SQLAlchemy
│   ├── base.py              # Base declarativa
│   └── user_model.py        # Modelo de usuário
├── schemas/                   # Schemas Pydantic
│   └── user_schema.py       # Schemas de usuário
├── api/                       # Rotas da API
│   ├── api.py               # Agregador de rotas
│   └── endpoints/           # Endpoints específicos
│       └── auth.py          # Autenticação
├── services/                  # Lógica de negócio
│   └── auth_service.py      # Serviços de autenticação
└── dependencies/             # Dependências FastAPI
    └── auth.py              # Dependências de auth
```

### 🔑 Endpoints Principais

| Módulo | Endpoint | Descrição |
|--------|----------|-----------|
| **Root** | `GET /` | Informações da API |
| **Health** | `GET /health` | Status da aplicação |
| **Auth** | `POST /api/v1/auth/register` | Registrar novo usuário |
| **Auth** | `POST /api/v1/auth/token` | Login e geração de JWT |

---

## 🤝 Contribuições (Próximos Passos)

- [ ] Completar interface frontend (Next.js)
- [ ] Adicionar modelos de Cliente, Quarto, Reserva
- [ ] Implementar CRUD completo para entidades
- [ ] Adicionar sistema de permissões/roles
- [ ] Implementar upload de imagens
- [ ] Adicionar testes automatizados
- [ ] Configurar Docker
- [ ] Implementar CI/CD
- [ ] Adicionar logging estruturado
- [ ] Migração para PostgreSQL
- [ ] Deploy em produção

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **JWT** - Autenticação via tokens
- **Bcrypt** - Hash seguro de senhas
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend (Planejado)
- **Next.js** - Framework React
- **TypeScript** - JavaScript tipado
- **Tailwind CSS** - Framework CSS
- **Axios** - Cliente HTTP

---

## 📞 Contato

**Desenvolvido por**: [Seu Nome]  
**GitHub**: [Seu GitHub]  
**LinkedIn**: [Seu LinkedIn]

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.