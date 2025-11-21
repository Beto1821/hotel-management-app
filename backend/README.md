# Backend - Hotel Management App

Sistema de gerenciamento de hotel com FastAPI, MySQL e autenticação JWT.

## 📋 Estrutura do Projeto

```
backend/
├── api/              # Rotas e endpoints da API
├── core/             # Configurações centrais (database, config)
├── dependencies/     # Dependências de injeção (auth, permissions)
├── models/           # Modelos SQLAlchemy
├── schemas/          # Schemas Pydantic
├── services/         # Lógica de negócio
├── tests/            # Testes automatizados
├── utils/            # Utilitários diversos
└── scripts/          # Scripts auxiliares (ver abaixo)
```

## 🔧 Scripts Utilitários

### Scripts de Configuração

#### `setup_mysql.sh`
**Objetivo**: Automatizar a configuração inicial do MySQL no macOS.

**Uso**:
```bash
./setup_mysql.sh
```

**O que faz**:
- Verifica se o MySQL está instalado
- Inicia o serviço MySQL via Homebrew
- Exibe instruções para configurar senha e criar banco de dados

---

### Scripts de Teste de Conexão

#### `test_db_connection.py`
**Objetivo**: Testar conexão com o banco de dados MySQL.

**Uso**:
```bash
python test_db_connection.py
```

**O que faz**:
- Conecta ao banco usando configurações do `.env`
- Verifica conectividade
- Lista tabelas existentes
- Mostra informações do banco de dados

**Saída esperada**:
```
✅ Conexão estabelecida com sucesso!
📊 Banco de dados conectado: HOTEL_APP
📋 Tabelas existentes: 6
   - users
   - clients
   - quartos
   - reservas
   - audit_logs
```

---

#### `check_db_connection.py`
**Objetivo**: Script legado de verificação de conexão (use `test_db_connection.py` no lugar).

---

### Scripts de Gestão de Usuários

#### `update_user_password.py`
**Objetivo**: Atualizar senha de usuários no banco de dados.

**Uso**:
```bash
python update_user_password.py
```

**O que faz**:
- Atualiza a senha do usuário "teste" para "teste123"
- Usa bcrypt para hash seguro
- Útil após mudanças no sistema de autenticação

**Quando usar**:
- Após atualizar bibliotecas de criptografia
- Para resetar senha de teste
- Quando migrar de passlib para bcrypt

---

#### `create_test_user.py`
**Objetivo**: Criar usuário de teste no banco de dados.

**Uso**:
```bash
python create_test_user.py
```

**O que faz**:
- Cria usuário "teste" com senha "teste123"
- Define role como VIEWER
- Útil para desenvolvimento e testes

---

#### `generate_test_user_sql.py`
**Objetivo**: Gerar SQL para inserir usuário de teste.

**Uso**:
```bash
python generate_test_user_sql.py
```

**Saída**: Script SQL para copiar/colar diretamente no MySQL.

---

#### `check_admin_password.py`
**Objetivo**: Verificar e validar senhas de administradores.

**Uso**:
```bash
python check_admin_password.py
```

---

### Scripts de Teste de API

#### `test_login.py`
**Objetivo**: Testar endpoint de login via HTTP.

**Uso**:
```bash
python test_login.py
```

**O que faz**:
- Faz requisição POST para `/api/v1/auth/token`
- Testa credenciais: teste/teste123
- Exibe token JWT retornado
- Mostra status code e resposta

**Saída esperada**:
```
🔐 Testando login com usuário: teste
📊 Status Code: 200
✅ Login bem-sucedido!
🎫 Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
📝 Token Type: bearer
```

---

#### `test_mysql.py`
**Objetivo**: Script de teste básico do MySQL (legado).

---

#### `test_api.py`
**Objetivo**: Testes gerais da API (na raiz do projeto).

---

## 📚 Documentação Adicional

- **[DATABASE_SETUP.md](./DATABASE_SETUP.md)** - Guia completo de configuração do MySQL
- **[SECURITY.md](./SECURITY.md)** - Práticas de segurança implementadas

## 🚀 Início Rápido

### 1. Configurar Ambiente

```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # ou .venv/Scripts/activate no Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

```bash
# Opção 1: Script automatizado
./setup_mysql.sh

# Opção 2: Manual (ver DATABASE_SETUP.md)
```

### 3. Configurar Variáveis de Ambiente

Crie o arquivo `.env`:
```env
# Database
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=HOTEL_APP

# JWT
SECRET_KEY=sua_chave_secreta_muito_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Testar Conexão

```bash
python test_db_connection.py
```

### 5. Criar Usuário de Teste

```bash
python update_user_password.py
```

### 6. Iniciar Servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Testar Login

```bash
python test_login.py
```

## 🧪 Testando a API

### Via Postman/Insomnia

1. **Login**:
   - POST `http://localhost:8000/api/v1/auth/token`
   - Body (x-www-form-urlencoded):
     - `username`: teste
     - `password`: teste123

2. **Acessar Dashboard** (requer autenticação):
   - GET `http://localhost:8000/api/v1/dashboard/`
   - Header: `Authorization: Bearer {seu_token}`

### Via Documentação Automática

Acesse: `http://localhost:8000/docs` (Swagger UI)

## 📝 Notas de Desenvolvimento

### Ordem de Execução Recomendada

1. `setup_mysql.sh` - Configurar MySQL
2. `test_db_connection.py` - Verificar conexão
3. `update_user_password.py` - Criar/atualizar usuário teste
4. `test_login.py` - Testar autenticação
5. Iniciar desenvolvimento

### Troubleshooting

**Erro: "Access denied for user 'root'@'localhost'"**
- Verifique senha no `.env`
- Execute: `mysql -u root -p` e teste manualmente

**Erro: "error reading bcrypt version"**
- Execute: `pip install --upgrade bcrypt>=4.0.0`
- Execute: `python update_user_password.py`

**Erro: "Could not validate credentials" (401)**
- Verifique se SECRET_KEY é a mesma em todos os módulos
- Verifique se o token está sendo enviado no header corretamente

## 🔐 Segurança

- ✅ Senhas hasheadas com bcrypt
- ✅ Autenticação JWT
- ✅ Proteção contra força bruta (bloqueio após 5 tentativas)
- ✅ Logs de auditoria
- ✅ Validação de força de senha
- ✅ Suporte a 2FA (2-Factor Authentication)

Ver [SECURITY.md](./SECURITY.md) para mais detalhes.

## 📦 Dependências Principais

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **PyMySQL** - Driver MySQL
- **bcrypt** - Hash de senhas
- **python-jose** - JWT
- **pydantic** - Validação de dados
- **uvicorn** - Servidor ASGI

## 🤝 Contribuindo

Ao adicionar novos scripts utilitários:
1. Adicione documentação neste README
2. Inclua docstrings no código
3. Adicione exemplo de uso
4. Documente saída esperada
