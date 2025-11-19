# 🚀 Guia Completo de Deploy - Sistema de Hotel

**Última atualização:** 19 de novembro de 2025  
**Servidor:** VPS Hostinger (Ubuntu 24.04 LTS)  
**Domínio:** plataformahotel.online  
**IP:** 72.61.56.72

---

## 📋 Índice

1. [Informações de Acesso](#informações-de-acesso)
2. [Configuração Inicial do Servidor](#configuração-inicial-do-servidor)
3. [Instalação do MySQL](#instalação-do-mysql)
4. [Instalação do Python 3.11](#instalação-do-python-311)
5. [Instalação do Node.js](#instalação-do-nodejs)
6. [Deploy do Backend](#deploy-do-backend)
7. [Configuração do Nginx](#configuração-do-nginx)
8. [Configuração de DNS](#configuração-de-dns)
9. [Certificado SSL](#certificado-ssl)
10. [Manutenção e Monitoramento](#manutenção-e-monitoramento)

---

## 🔐 Informações de Acesso

### VPS Hostinger
```bash
IP: 72.61.56.72
Usuário: root
Porta SSH: 22
SO: Ubuntu 24.04 LTS
Localização: Brasil - São Paulo
```

### Banco de Dados MySQL
```bash
Host: localhost
Porta: 3306
Database: HOTEL_APP
Usuário: hotel_user
Senha: Hotel@2025
```

### Usuário Admin do Sistema
```bash
Username: Adalberto Ribeiro
Email: beto1821@uol.com.br
Senha: Lilica@007
Role: ADMIN
```

### Domínio
```bash
Domínio: plataformahotel.online
DNS: Hostinger
Registros A:
  @ → 72.61.56.72
  www (CNAME) → plataformahotel.online
```

---

## 1️⃣ Configuração Inicial do Servidor

### Conectar ao VPS via SSH
```bash
ssh root@72.61.56.72
```

### Atualizar o Sistema
```bash
apt update && apt upgrade -y
```

### Configurar Firewall (UFW)
```bash
ufw allow OpenSSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
ufw status
```

### Instalar Dependências Essenciais
```bash
apt install -y git curl wget vim build-essential
```

---

## 2️⃣ Instalação do MySQL

### Instalar MySQL 8.0
```bash
apt install mysql-server -y
```

### Configurar Segurança
```bash
mysql_secure_installation
```

**Respostas:**
- VALIDATE PASSWORD component? **N**
- Remove anonymous users? **Y**
- Disallow root login remotely? **Y**
- Remove test database? **Y**
- Reload privilege tables? **Y**

### Criar Banco de Dados e Usuário
```bash
mysql -u root -p
```

```sql
CREATE DATABASE HOTEL_APP CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'hotel_user'@'localhost' IDENTIFIED BY 'Hotel@2025';

GRANT ALL PRIVILEGES ON HOTEL_APP.* TO 'hotel_user'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

---

## 3️⃣ Instalação do Python 3.11

### Adicionar Repositório e Instalar
```bash
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install python3.11 python3.11-venv python3.11-dev python3-pip -y
```

### Verificar Instalação
```bash
python3.11 --version
# Python 3.11.x
```

---

## 4️⃣ Instalação do Node.js

### Instalar Node.js 20 LTS
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
```

### Verificar Instalação
```bash
node --version   # v20.x.x
npm --version    # 10.x.x
```

---

## 5️⃣ Deploy do Backend

### Criar Diretório e Clonar Repositório
```bash
mkdir -p /var/www
cd /var/www
git clone https://github.com/Beto1821/hotel-management-app.git
cd hotel-management-app/backend
```

### Criar Ambiente Virtual
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Instalar Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install passlib python-jose[cryptography]
pip install 'pydantic[email]'
pip install bcrypt==4.0.1
```

### Criar Arquivo .env
```bash
nano .env
```

**Conteúdo do .env:**
```bash
# Banco de Dados
DB_USER=hotel_user
DB_PASSWORD=Hotel@2025
DB_HOST=localhost
DB_PORT=3306
DB_NAME=HOTEL_APP

# JWT
SECRET_KEY=1iLbFSet9mKoegGWm6g34bTuL3n9KLGn2y8OipuF9Nw
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ambiente
ENVIRONMENT=production
DEBUG=False

# CORS
ALLOWED_ORIGINS=https://plataformahotel.online,https://www.plataformahotel.online

# Pool MySQL
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

### Gerar Nova SECRET_KEY (se necessário)
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Criar Tabelas no Banco
```bash
python -c "from core.database import create_tables; create_tables()"
```

### Criar Arquivo security.py (se não existir)
```bash
nano core/security.py
```

**Conteúdo:**
```python
"""Funções de segurança para autenticação e criptografia."""

from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt
import os

# Configuração do contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-padrao")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def get_password_hash(password: str) -> str:
    """Gera hash bcrypt da senha."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Criar Usuário Admin
```bash
python -c "
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user_model import User, UserRole
from core.security import get_password_hash
from datetime import datetime

db = SessionLocal()
admin = User(
    username='Adalberto Ribeiro',
    email='beto1821@uol.com.br',
    hashed_password=get_password_hash('Lilica@007'),
    role=UserRole.ADMIN,
    is_active=True,
    created_at=datetime.utcnow()
)
db.add(admin)
db.commit()
print('✅ Admin criado com sucesso!')
db.close()
"
```

### Instalar PM2 (Gerenciador de Processos)
```bash
npm install -g pm2
```

### Iniciar Backend com PM2
```bash
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name hotel-api
pm2 save
pm2 startup systemd
# Executar o comando que aparecer
```

### Verificar Status
```bash
pm2 status
pm2 logs hotel-api --lines 20
```

---

## 6️⃣ Configuração do Nginx

### Instalar Nginx
```bash
apt install nginx -y
```

### Criar Configuração do Site
```bash
nano /etc/nginx/sites-available/hotel_api
```

**Conteúdo (configuração inicial HTTP):**
```nginx
server {
    server_name plataformahotel.online www.plataformahotel.online;
    listen 80;
    listen [::]:80;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

### Ativar Site
```bash
ln -s /etc/nginx/sites-available/hotel_api /etc/nginx/sites-enabled/hotel_api
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl enable nginx
```

---

## 7️⃣ Configuração de DNS

### Registros DNS na Hostinger

1. Acesse o painel da Hostinger
2. Vá em **Domínios** → **plataformahotel.online** → **DNS / Nameservers**
3. Crie/edite os registros:

```
Tipo: A
Nome: @
Aponta para: 72.61.56.72
TTL: 300

Tipo: CNAME
Nome: www
Aponta para: plataformahotel.online
TTL: 300
```

### Verificar Propagação
```bash
dig +short plataformahotel.online
dig +short www.plataformahotel.online
# Ambos devem resolver para 72.61.56.72
```

### Limpar Cache DNS (Mac local)
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

---

## 8️⃣ Certificado SSL (Let's Encrypt)

### Instalar Certbot
```bash
apt install certbot python3-certbot-nginx -y
```

### Gerar Certificado
```bash
certbot --nginx -d plataformahotel.online -d www.plataformahotel.online \
  -m beto1821@uol.com.br --agree-tos --redirect
```

**Responder:**
- Share email with EFF? **Y** ou **N**

### Verificar Certificados
```bash
certbot certificates
```

### Testar Renovação Automática
```bash
certbot renew --dry-run
```

### Ver Timer de Renovação
```bash
systemctl list-timers | grep certbot
```

---

## 9️⃣ Ajuste do Endpoint /health (HEAD Support)

### Editar main.py
```bash
nano main.py
```

**Localizar:**
```python
@app.get("/health")
def health_check():
```

**Alterar para:**
```python
@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
```

### Reiniciar Backend
```bash
pm2 restart hotel-api
```

### Testar
```bash
curl -I https://plataformahotel.online/health
# Deve retornar HTTP/1.1 200 OK
```

---

## 🔟 Manutenção e Monitoramento

### Comandos PM2
```bash
# Ver status
pm2 status

# Ver logs em tempo real
pm2 logs hotel-api

# Ver últimas 50 linhas
pm2 logs hotel-api --lines 50

# Reiniciar aplicação
pm2 restart hotel-api

# Parar aplicação
pm2 stop hotel-api

# Remover do PM2
pm2 delete hotel-api

# Salvar configuração
pm2 save
```

### Logs do Nginx
```bash
# Acesso
tail -f /var/log/nginx/access.log

# Erros
tail -f /var/log/nginx/error.log

# Testar configuração
nginx -t

# Reiniciar Nginx
systemctl restart nginx
```

### Backup Manual do MySQL
```bash
mysqldump -u hotel_user -pHotel@2025 HOTEL_APP > /root/backup_hotel_$(date +%Y%m%d_%H%M%S).sql
```

### Configurar Backup Automático
```bash
# Criar script de backup
nano /root/backup_mysql.sh
```

**Conteúdo:**
```bash
#!/bin/bash
BACKUP_DIR="/root/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p $BACKUP_DIR

mysqldump -u hotel_user -pHotel@2025 HOTEL_APP > $BACKUP_DIR/hotel_$TIMESTAMP.sql

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "hotel_*.sql" -mtime +7 -delete
```

**Dar permissão e agendar:**
```bash
chmod +x /root/backup_mysql.sh

# Agendar no cron (diário às 2h)
crontab -e
# Adicionar linha:
0 2 * * * /root/backup_mysql.sh
```

### Atualizar Código do Backend
```bash
cd /var/www/hotel-management-app/backend
git pull
source .venv/bin/activate
pip install -r requirements.txt
pm2 restart hotel-api
```

### Monitorar Recursos do Servidor
```bash
# Uso de CPU e memória
htop

# Uso de disco
df -h

# Processos do PM2
pm2 monit

# Status dos serviços
systemctl status nginx
systemctl status mysql
```

---

## 🧪 Testes de Produção

### Testar Health Check
```bash
curl https://plataformahotel.online/health
# {"status":"healthy","message":"API is running"}
```

### Testar Redirecionamento HTTP → HTTPS
```bash
curl -I http://plataformahotel.online/health
# HTTP/1.1 301 Moved Permanently
# Location: https://plataformahotel.online/health
```

### Testar Autenticação (Login Admin)
```bash
curl -X POST https://plataformahotel.online/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=beto1821@uol.com.br&password=Lilica@007"
```

### Testar com Token
```bash
# Primeiro, fazer login e copiar o token
TOKEN="cole_aqui_o_token_recebido"

# Listar clientes (exemplo)
curl https://plataformahotel.online/api/v1/clientes \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔒 Segurança

### Alterar Senha Root do MySQL
```bash
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NovaSenhaForte@123';
FLUSH PRIVILEGES;
EXIT;
```

### Alterar Senha do Usuário hotel_user
```bash
mysql -u root -p
ALTER USER 'hotel_user'@'localhost' IDENTIFIED BY 'NovaSenha@2025';
FLUSH PRIVILEGES;
EXIT;

# Atualizar .env
nano .env
# DB_PASSWORD=NovaSenha@2025

# Reiniciar backend
pm2 restart hotel-api
```

### Gerar Nova SECRET_KEY
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Atualizar no .env
nano .env
# Reiniciar backend
pm2 restart hotel-api
```

---

## 📊 URLs Importantes

```
Backend API (HTTPS): https://plataformahotel.online
Health Check: https://plataformahotel.online/health
Docs (Swagger): https://plataformahotel.online/docs
ReDoc: https://plataformahotel.online/redoc
```

---

## 🆘 Troubleshooting

### Backend não inicia
```bash
pm2 logs hotel-api --lines 100
# Verificar erros nos logs
```

### Erro de conexão com MySQL
```bash
# Verificar se MySQL está rodando
systemctl status mysql

# Testar conexão
mysql -u hotel_user -pHotel@2025 HOTEL_APP

# Verificar .env
cat .env | grep DB_
```

### Nginx retorna 502 Bad Gateway
```bash
# Verificar se backend está rodando
pm2 status

# Reiniciar backend
pm2 restart hotel-api

# Ver logs do Nginx
tail -f /var/log/nginx/error.log
```

### SSL não funciona
```bash
# Verificar certificados
certbot certificates

# Testar configuração Nginx
nginx -t

# Renovar certificado
certbot renew --force-renewal
```

### DNS não resolve
```bash
# Verificar propagação
dig +short plataformahotel.online
dig +short www.plataformahotel.online

# Usar servidor DNS público
dig @8.8.8.8 plataformahotel.online

# Limpar cache local (Mac)
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

---

## 📝 Checklist de Deploy Completo

- [x] VPS Ubuntu 24.04 configurado
- [x] MySQL 8.0 instalado e seguro
- [x] Python 3.11 instalado
- [x] Node.js 20 instalado
- [x] Código clonado do GitHub
- [x] Ambiente virtual criado
- [x] Dependências instaladas
- [x] Arquivo .env configurado
- [x] Tabelas criadas no banco
- [x] Usuário admin criado
- [x] PM2 instalado e configurado
- [x] Backend rodando na porta 8000
- [x] Nginx instalado
- [x] Proxy reverso configurado
- [x] DNS @ e www configurados
- [x] SSL/HTTPS ativo
- [x] Redirecionamento HTTP → HTTPS
- [x] Endpoint /health funcionando (GET e HEAD)
- [x] Pool MySQL otimizado
- [x] Backup automático configurado
- [x] Renovação SSL automática

---

## 🎯 Próximos Passos

1. **Deploy do Frontend Nuxt** (em desenvolvimento)
2. **Configurar CI/CD** (GitHub Actions)
3. **Implementar monitoramento** (Grafana, Prometheus)
4. **Configurar alertas** (Slack, email)
5. **Otimizar performance** (cache, CDN)

---

**Documentação criada por:** Adalberto Ribeiro  
**GitHub:** https://github.com/Beto1821/hotel-management-app  
**Data:** 19/11/2025
