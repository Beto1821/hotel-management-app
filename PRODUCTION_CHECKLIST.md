# ✅ Checklist de Preparação para Produção

## 📋 Checklist Pré-Merge (Branch desenvolvimento → main)

### 1. Código e Qualidade ✅
- [x] Todos os testes passando (30/30 - 100%)
- [x] Sem warnings do Pydantic (model_dump em vez de .dict())
- [x] Código sem erros de linting (flake8)
- [x] Documentação de API atualizada (/docs, /redoc)

### 2. Configuração de Segurança ✅
- [x] SECRET_KEY obrigatória via variável de ambiente
- [x] CORS configurado via variável de ambiente
- [x] Senhas nunca hardcoded no código
- [x] .env no .gitignore
- [x] .env.example criado para referência
- [x] Documentação de segurança (SECURITY.md)

### 3. Variáveis de Ambiente ✅
- [x] Arquivo `.env.example` criado em `/backend`
- [x] `.env` listado no `.gitignore`
- [x] Variáveis necessárias documentadas:
  - DATABASE_URL
  - SECRET_KEY (obrigatória)
  - ALGORITHM
  - ACCESS_TOKEN_EXPIRE_MINUTES
  - ALLOWED_ORIGINS
  - ENVIRONMENT

### 4. Banco de Dados
- [ ] Script de migração testado (`database/init.sql`)
- [ ] Backup do banco de desenvolvimento criado
- [ ] Credenciais de produção separadas
- [ ] Índices de performance verificados

### 5. Frontend
- [ ] Build de produção testado (`npm run build`)
- [ ] Variáveis de ambiente do Nuxt configuradas
- [ ] API_BASE_URL apontando para produção
- [ ] Assets otimizados

---

## 🚀 Passos para Deploy em Produção

### Backend (FastAPI)

#### 1. Preparar Servidor
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.9+
sudo apt install python3 python3-pip python3-venv -y

# Instalar MySQL
sudo apt install mysql-server -y
sudo mysql_secure_installation
```

#### 2. Configurar Aplicação
```bash
# Clonar repositório
git clone https://github.com/Beto1821/hotel-management-app.git
cd hotel-management-app/backend

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

#### 3. Configurar Variáveis de Ambiente
```bash
# Criar arquivo .env (NUNCA commitar!)
nano .env
```

Conteúdo do `.env` de **PRODUÇÃO**:
```env
# Database - Usar credenciais de produção
DATABASE_URL=mysql+pymysql://usuario_prod:senha_forte@localhost:3306/hotel_prod

# JWT - GERAR NOVA SECRET_KEY!
SECRET_KEY=use-o-comando-abaixo-para-gerar
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Adicionar domínio de produção
ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com

# Environment
ENVIRONMENT=production
```

**IMPORTANTE**: Gerar SECRET_KEY segura:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 4. Configurar Banco de Dados
```bash
# Criar banco de dados
mysql -u root -p
```
```sql
CREATE DATABASE hotel_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'usuario_prod'@'localhost' IDENTIFIED BY 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON hotel_prod.* TO 'usuario_prod'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Executar script de inicialização
mysql -u usuario_prod -p hotel_prod < database/init.sql
```

#### 5. Configurar Gunicorn + Nginx
```bash
# Instalar Gunicorn
pip install gunicorn

# Criar arquivo de serviço systemd
sudo nano /etc/systemd/system/hotel-api.service
```

Conteúdo do `hotel-api.service`:
```ini
[Unit]
Description=Hotel Management API
After=network.target

[Service]
User=seu_usuario
Group=www-data
WorkingDirectory=/caminho/para/hotel-management-app/backend
Environment="PATH=/caminho/para/hotel-management-app/backend/venv/bin"
ExecStart=/caminho/para/hotel-management-app/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar serviço
sudo systemctl start hotel-api
sudo systemctl enable hotel-api
sudo systemctl status hotel-api
```

#### 6. Configurar Nginx
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/hotel-api
```

Conteúdo do `hotel-api`:
```nginx
server {
    listen 80;
    server_name api.seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/hotel-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. Configurar SSL (Certbot)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.seu-dominio.com
```

---

### Frontend (Nuxt 3)

#### 1. Configurar Variáveis de Ambiente
```bash
cd ../frontend
nano .env
```

Conteúdo do `.env` de **PRODUÇÃO**:
```env
NUXT_PUBLIC_API_BASE_URL=https://api.seu-dominio.com/api/v1
```

#### 2. Build de Produção
```bash
npm install
npm run build
```

#### 3. Configurar Nginx para Frontend
```bash
sudo nano /etc/nginx/sites-available/hotel-frontend
```

Conteúdo do `hotel-frontend`:
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    root /caminho/para/hotel-management-app/frontend/.output/public;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (opcional se usar domínio separado)
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/hotel-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. SSL para Frontend
```bash
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

---

## 🔒 Checklist de Segurança em Produção

### Obrigatório
- [ ] SECRET_KEY única e forte (32+ caracteres)
- [ ] Credenciais de banco diferentes de desenvolvimento
- [ ] HTTPS/SSL configurado (certbot)
- [ ] Firewall configurado (UFW)
  ```bash
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```
- [ ] Desabilitar /docs e /redoc em produção (já configurado via ENVIRONMENT)
- [ ] Rate limiting no Nginx
- [ ] Backup automático do banco de dados

### Recomendado
- [ ] Monitoring (Prometheus, Grafana)
- [ ] Logs centralizados (ELK Stack)
- [ ] Alerts de erro (Sentry)
- [ ] CI/CD configurado (GitHub Actions)
- [ ] Testes automáticos no pipeline

---

## 📊 Verificações Pós-Deploy

### Backend
```bash
# Verificar se API está rodando
curl https://api.seu-dominio.com/

# Verificar logs
sudo journalctl -u hotel-api -f

# Status do serviço
sudo systemctl status hotel-api
```

### Frontend
```bash
# Verificar se site carrega
curl https://seu-dominio.com/

# Verificar logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Banco de Dados
```bash
# Conectar e verificar tabelas
mysql -u usuario_prod -p hotel_prod
SHOW TABLES;
SELECT COUNT(*) FROM users;
```

---

## 🔄 Fluxo de Atualização

### 1. Testar em Desenvolvimento
```bash
git checkout desenvolvimento
# Fazer alterações
python -m pytest tests/
git add .
git commit -m "feat: nova funcionalidade"
git push origin desenvolvimento
```

### 2. Merge para Main
```bash
git checkout main
git merge desenvolvimento
git push origin main
```

### 3. Deploy em Produção
```bash
# No servidor
cd /caminho/para/hotel-management-app
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart hotel-api

# Frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart nginx
```

---

## 📝 Comandos Úteis de Manutenção

```bash
# Backup do banco
mysqldump -u usuario_prod -p hotel_prod > backup_$(date +%Y%m%d).sql

# Restaurar backup
mysql -u usuario_prod -p hotel_prod < backup_20241121.sql

# Ver logs da API
sudo journalctl -u hotel-api --since "1 hour ago"

# Reiniciar todos os serviços
sudo systemctl restart hotel-api nginx mysql

# Limpar logs antigos
sudo journalctl --vacuum-time=7d
```

---

## ⚠️ IMPORTANTE - Antes do Merge

1. **Criar arquivo .env local** seguindo `.env.example`
2. **Testar localmente** com as novas configurações
3. **Rodar todos os testes** (30/30 devem passar)
4. **Verificar se não há .env commitado** no git
5. **Revisar CORS e origens permitidas**
6. **Documentar mudanças** no CHANGELOG ou release notes

---

## 📞 Suporte e Troubleshooting

### Erro: "SECRET_KEY não definida"
**Solução**: Criar arquivo `.env` com SECRET_KEY

### Erro: 502 Bad Gateway
**Solução**: Verificar se API está rodando (`systemctl status hotel-api`)

### Erro: CORS
**Solução**: Adicionar origem em ALLOWED_ORIGINS no `.env`

### Erro: Database connection
**Solução**: Verificar DATABASE_URL e credenciais no `.env`

---

**Data**: 21/11/2024  
**Status**: ✅ Pronto para merge desenvolvimento → main  
**Versão**: 1.0.0
