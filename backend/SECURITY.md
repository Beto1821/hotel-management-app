# Guia de Segurança - Sistema de Autenticação e Autorização

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Sistema de Roles](#sistema-de-roles)
3. [Autenticação](#autenticação)
4. [Autorização](#autorização)
5. [Auditoria](#auditoria)
6. [Recursos de Segurança](#recursos-de-segurança)
7. [Migração do Banco de Dados](#migração-do-banco-de-dados)
8. [Exemplos de Uso](#exemplos-de-uso)

## 🔒 Visão Geral

O sistema implementa um conjunto completo de funcionalidades de segurança para produção:

- **Controle de Acesso Baseado em Roles (RBAC)**
- **Autenticação JWT com proteção de conta**
- **Autenticação de Dois Fatores (2FA)** - TOTP
- **Recuperação de Senha** segura
- **Auditoria Completa** de ações
- **Proteção contra Força Bruta**
- **Bloqueio Progressivo de Conta**

## 👥 Sistema de Roles

### Roles Disponíveis

O sistema possui 4 níveis de acesso hierárquicos:

```python
class UserRole(str, Enum):
    ADMIN = "ADMIN"           # Acesso total
    MANAGER = "MANAGER"       # Gerenciamento operacional
    RECEPTIONIST = "RECEPTIONIST"  # Operações diárias
    VIEWER = "VIEWER"         # Apenas visualização
```

### Hierarquia de Permissões

```
ADMIN
  └── Todas as permissões
      ├── Gerenciar usuários
      ├── Configurações do sistema
      └── Todas as operações do MANAGER
      
MANAGER
  └── Gerenciamento operacional
      ├── Criar/editar/excluir quartos
      ├── Gerenciar reservas
      ├── Relatórios financeiros
      └── Todas as operações do RECEPTIONIST
      
RECEPTIONIST
  └── Operações diárias
      ├── Check-in/Check-out
      ├── Criar reservas
      ├── Gerenciar clientes
      └── Todas as operações do VIEWER
      
VIEWER
  └── Apenas visualização
      ├── Ver reservas
      ├── Ver quartos
      └── Ver clientes
```

## 🔐 Autenticação

### Registro de Usuário

```python
POST /api/v1/auth/register
{
    "username": "usuario",
    "email": "usuario@hotel.com",
    "password": "SenhaForte123!"
}
```

**Validações de Senha:**
- Mínimo 8 caracteres
- Pelo menos 1 letra maiúscula
- Pelo menos 1 letra minúscula
- Pelo menos 1 número
- Pelo menos 1 caractere especial (!@#$%^&*(),.?":{}|<>)

### Login

```python
POST /api/v1/auth/token
Form Data:
  username: "usuario"
  password: "SenhaForte123!"

Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

**Proteções de Login:**
- Verificação de conta ativa
- Verificação de bloqueio
- Contador de tentativas falhadas
- Bloqueio progressivo após 5 tentativas
- Registro de auditoria

### Recuperação de Senha

#### 1. Solicitar Reset

```python
POST /api/v1/auth/forgot-password
{
    "username": "usuario"  # pode ser username ou email
}

Response:
{
    "message": "Token de reset gerado",
    "reset_token": "abc123...",  # Apenas em dev, remover em produção
    "expires_at": "2024-01-01T12:00:00"
}
```

#### 2. Resetar Senha

```python
POST /api/v1/auth/reset-password
{
    "token": "abc123...",
    "new_password": "NovaSenhaForte456!"
}

Response:
{
    "message": "Senha resetada com sucesso"
}
```

**Características:**
- Token expira em 1 hora
- Token de uso único
- Validação de força da nova senha
- Reseta contador de tentativas falhadas
- Desbloqueia conta automaticamente

## 🛡️ Autorização

### Usando Permissões em Endpoints

```python
from fastapi import APIRouter, Depends
from dependencies.permissions import require_admin, require_manager, require_staff
from models.user_model import User

router = APIRouter()

# Apenas ADMIN pode acessar
@router.get("/admin-only")
def admin_endpoint(current_user: User = Depends(require_admin)):
    return {"message": f"Olá Admin {current_user.username}"}

# ADMIN e MANAGER podem acessar
@router.get("/managers")
def manager_endpoint(current_user: User = Depends(require_manager)):
    return {"message": f"Olá {current_user.role} {current_user.username}"}

# ADMIN, MANAGER e RECEPTIONIST podem acessar
@router.get("/staff")
def staff_endpoint(current_user: User = Depends(require_staff)):
    return {"message": f"Olá {current_user.role} {current_user.username}"}

# Permissão customizada
from dependencies.permissions import require_role
from models.user_model import UserRole

@router.get("/custom")
def custom_endpoint(
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.MANAGER))
):
    return {"message": "Apenas ADMIN e MANAGER"}
```

### Permissões Disponíveis

```python
from dependencies.permissions import (
    require_admin,          # Apenas ADMIN
    require_manager,        # ADMIN ou MANAGER
    require_staff,          # ADMIN, MANAGER ou RECEPTIONIST
    require_any_authenticated,  # Qualquer usuário autenticado
    require_role            # Customizável
)
```

## 📊 Auditoria

### Log Automático de Ações

O sistema registra automaticamente:

- ✅ Login (sucesso e falhas)
- ✅ Logout
- ✅ Criação de recursos
- ✅ Atualização de recursos
- ✅ Exclusão de recursos
- ✅ Solicitação de reset de senha
- ✅ Conclusão de reset de senha
- ✅ Habilitação/desabilitação de 2FA

### Usando o Serviço de Auditoria

```python
from services.audit_service import AuditService
from utils.request_utils import get_client_info

@router.post("/quartos")
def create_quarto(
    quarto_data: QuartoCreate,
    request: Request,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    # Criar quarto
    quarto = Quarto(**quarto_data.dict())
    db.add(quarto)
    db.commit()
    
    # Registrar auditoria
    client_info = get_client_info(request)
    AuditService.log_create(
        db=db,
        user_id=current_user.id,
        resource="ROOM",
        resource_id=quarto.id,
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"numero": quarto.numero, "tipo": quarto.tipo}
    )
    
    return quarto
```

### Métodos Disponíveis

```python
# Login
AuditService.log_login(db, user_id, success, ip_address, user_agent, details)

# Logout
AuditService.log_logout(db, user_id, ip_address, user_agent)

# CRUD
AuditService.log_create(db, user_id, resource, resource_id, ...)
AuditService.log_update(db, user_id, resource, resource_id, ...)
AuditService.log_delete(db, user_id, resource, resource_id, ...)

# Ação genérica
AuditService.log_action(db, user_id, action, resource, ...)
```

## 🔐 Recursos de Segurança

### 1. Proteção Contra Força Bruta

- Contador de tentativas de login falhadas
- Bloqueio progressivo:
  - 5 falhas: 15 minutos
  - 6 falhas: 30 minutos
  - 7 falhas: 1 hora
  - 8 falhas: 2 horas
  - 9+ falhas: até 24 horas

### 2. Validação de Senha Forte

```python
from services.auth_service import validate_password_strength

is_valid, message = validate_password_strength("senha123")
# is_valid = False
# message = "A senha deve conter pelo menos uma letra maiúscula"
```

### 3. Informações de Cliente (IP e User Agent)

```python
from utils.request_utils import get_client_info, get_client_ip, get_user_agent

# Obter tudo
client_info = get_client_info(request)
# {"ip_address": "192.168.1.100", "user_agent": "Mozilla/5.0..."}

# Individual
ip = get_client_ip(request)
ua = get_user_agent(request)
```

### 4. Verificação de Conta Ativa

O sistema automaticamente verifica:
- Se o usuário está ativo (`is_active`)
- Se a conta não está bloqueada (`locked_until`)

### 5. Auditoria de IP e User Agent

Todos os logs de auditoria capturam:
- Endereço IP do cliente
- User Agent do navegador
- Timestamp da ação

## 💾 Migração do Banco de Dados

### Executar Migração

Para adicionar os novos campos de segurança ao banco:

```bash
cd backend
python migrations/add_security_fields.py
```

A migração adiciona:

**Tabela `users`:**
- `email` - Email do usuário (único)
- `role` - Role do usuário (ADMIN, MANAGER, RECEPTIONIST, VIEWER)
- `is_active` - Se a conta está ativa
- `totp_secret` - Secret para 2FA
- `is_2fa_enabled` - Se 2FA está habilitado
- `reset_token` - Token para reset de senha
- `reset_token_expires` - Expiração do token
- `failed_login_attempts` - Contador de falhas
- `locked_until` - Data/hora de bloqueio
- `created_at` - Data de criação
- `updated_at` - Data de atualização
- `last_login` - Último login
- `last_login_ip` - IP do último login

**Tabela `audit_logs`:**
- Nova tabela para logs de auditoria
- Índices otimizados para consultas

### Rollback Manual

Se precisar reverter:

```sql
-- Remover campos da tabela users
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users DROP COLUMN role;
-- ... (remover todos os campos)

-- Remover tabela de auditoria
DROP TABLE audit_logs;
```

## 📚 Exemplos de Uso

### Exemplo 1: Endpoint Protegido com Role

```python
from fastapi import APIRouter, Depends, HTTPException
from dependencies.permissions import require_manager
from models.user_model import User
from services.audit_service import AuditService
from utils.request_utils import get_client_info

router = APIRouter(prefix="/api/v1/quartos", tags=["Quartos"])

@router.delete("/{quarto_id}")
def delete_quarto(
    quarto_id: int,
    request: Request,
    current_user: User = Depends(require_manager),  # Apenas MANAGER ou ADMIN
    db: Session = Depends(get_db)
):
    # Buscar quarto
    quarto = db.query(Quarto).filter(Quarto.id == quarto_id).first()
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    
    # Registrar auditoria ANTES de deletar
    client_info = get_client_info(request)
    AuditService.log_delete(
        db=db,
        user_id=current_user.id,
        resource="ROOM",
        resource_id=quarto.id,
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"numero": quarto.numero, "tipo": quarto.tipo}
    )
    
    # Deletar
    db.delete(quarto)
    db.commit()
    
    return {"message": "Quarto deletado com sucesso"}
```

### Exemplo 2: Verificar Role Manualmente

```python
from models.user_model import UserRole

@router.post("/action")
def special_action(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verificação manual de role
    if current_user.role == UserRole.ADMIN:
        # Ação especial para admin
        pass
    elif current_user.role == UserRole.MANAGER:
        # Ação para manager
        pass
    else:
        raise HTTPException(
            status_code=403,
            detail="Permissão insuficiente"
        )
```

### Exemplo 3: Listar Logs de Auditoria

```python
@router.get("/audit-logs")
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),  # Apenas admin
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).offset(skip).limit(limit).all()
    
    return logs
```

## 🚀 Próximos Passos

### Para Produção:

1. **Rate Limiting:**
   ```bash
   pip install slowapi
   ```
   Implementar limite de requisições por IP

2. **HTTPS:**
   - Configurar certificado SSL
   - Forçar HTTPS em produção

3. **Variáveis de Ambiente:**
   ```bash
   # .env
   SECRET_KEY=<gerar-chave-secreta-forte>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Email para Reset de Senha:**
   ```bash
   pip install fastapi-mail
   ```
   Configurar serviço de email

5. **Implementar 2FA:**
   - Criar endpoints para habilitar/desabilitar 2FA
   - Endpoint para gerar QR Code
   - Verificação de token na autenticação

6. **Monitoramento:**
   - Implementar alertas de segurança
   - Dashboard de auditoria
   - Notificações de atividade suspeita

## 📖 Documentação Adicional

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

## 🆘 Suporte

Em caso de dúvidas ou problemas:
1. Verificar logs de auditoria
2. Verificar configuração de ambiente
3. Verificar migração do banco de dados
4. Consultar este guia

---

**Última atualização:** 2024
**Versão:** 1.0.0
