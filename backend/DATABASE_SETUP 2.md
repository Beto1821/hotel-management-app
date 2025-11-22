# Configuração do Banco de Dados MySQL

## ⚠️ AÇÃO NECESSÁRIA

O backend está configurado para usar MySQL, mas precisa de configuração inicial.

## Passos para Configurar:

### 1. Instalar o MySQL (se ainda não estiver instalado)

No macOS com Homebrew:
```bash
brew install mysql
brew services start mysql
```

### 2. Configurar a Senha do Root

Execute no terminal:
```bash
mysql -u root
```

Dentro do MySQL:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'sua_senha_aqui';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Criar o Banco de Dados

```bash
mysql -u root -p
```

Dentro do MySQL:
```sql
CREATE DATABASE HOTEL_APP;
EXIT;
```

### 4. Atualizar o Arquivo .env

Edite o arquivo `/backend/.env` e coloque a senha que você definiu:
```env
DB_PASSWORD=sua_senha_aqui
```

### 5. Reiniciar o Servidor

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Alternativa: Usar SQLite (mais simples para desenvolvimento)

Se preferir não usar MySQL agora, você pode usar SQLite temporariamente:

1. Edite `backend/core/database.py` e substitua a linha `DATABASE_URL` por:
```python
DATABASE_URL = "sqlite:///./hotel_app.db"
```

2. Reinicie o servidor

## Verificar Conexão

Execute o script de teste:
```bash
cd backend
python check_db_connection.py
```

## Problemas Comuns

### Erro: Access denied for user 'root'@'localhost'
- Verifique se a senha no arquivo `.env` está correta
- Verifique se o MySQL está rodando: `brew services list`

### Erro: Can't connect to MySQL server
- Verifique se o MySQL está instalado e rodando
- Verifique o host e porta no arquivo `.env`
