"""
Script de migração para adicionar campos de segurança ao modelo User
e criar tabela de auditoria

Execute este script para atualizar o banco de dados com os novos campos de segurança.
"""
from sqlalchemy import text
from core.database import engine, SessionLocal


def migrate_user_table():
    """Adiciona novos campos à tabela users"""
    
    with engine.begin() as conn:
        # Adiciona campo email
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN email VARCHAR(255) UNIQUE
            """))
            print("✓ Campo 'email' adicionado")
        except Exception as e:
            print(f"Campo 'email' já existe ou erro: {e}")
        
        # Adiciona campo role
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR(20) DEFAULT 'VIEWER'
            """))
            print("✓ Campo 'role' adicionado")
        except Exception as e:
            print(f"Campo 'role' já existe ou erro: {e}")
        
        # Adiciona campo is_active
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN is_active BOOLEAN DEFAULT TRUE
            """))
            print("✓ Campo 'is_active' adicionado")
        except Exception as e:
            print(f"Campo 'is_active' já existe ou erro: {e}")
        
        # Campos 2FA
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN totp_secret VARCHAR(255)
            """))
            print("✓ Campo 'totp_secret' adicionado")
        except Exception as e:
            print(f"Campo 'totp_secret' já existe ou erro: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN is_2fa_enabled BOOLEAN DEFAULT FALSE
            """))
            print("✓ Campo 'is_2fa_enabled' adicionado")
        except Exception as e:
            print(f"Campo 'is_2fa_enabled' já existe ou erro: {e}")
        
        # Campos de recuperação de senha
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN reset_token VARCHAR(255)
            """))
            print("✓ Campo 'reset_token' adicionado")
        except Exception as e:
            print(f"Campo 'reset_token' já existe ou erro: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN reset_token_expires DATETIME
            """))
            print("✓ Campo 'reset_token_expires' adicionado")
        except Exception as e:
            print(f"Campo 'reset_token_expires' já existe ou erro: {e}")
        
        # Campos de bloqueio de conta
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN failed_login_attempts INTEGER DEFAULT 0
            """))
            print("✓ Campo 'failed_login_attempts' adicionado")
        except Exception as e:
            print(f"Campo 'failed_login_attempts' já existe ou erro: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN locked_until DATETIME
            """))
            print("✓ Campo 'locked_until' adicionado")
        except Exception as e:
            print(f"Campo 'locked_until' já existe ou erro: {e}")
        
        # Campos de auditoria
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            """))
            print("✓ Campo 'created_at' adicionado")
        except Exception as e:
            print(f"Campo 'created_at' já existe ou erro: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """))
            print("✓ Campo 'updated_at' adicionado")
        except Exception as e:
            print(f"Campo 'updated_at' já existe ou erro: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN last_login DATETIME
            """))
            print("✓ Campo 'last_login' adicionado")
        except Exception as e:
            print(f"Campo 'last_login' já existe ou erro: {e}")
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN last_login_ip VARCHAR(45)
            """))
            print("✓ Campo 'last_login_ip' adicionado")
        except Exception as e:
            print(f"Campo 'last_login_ip' já existe ou erro: {e}")


def create_audit_log_table():
    """Cria a tabela de logs de auditoria"""
    
    with engine.begin() as conn:
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    user_id INTEGER NOT NULL,
                    action VARCHAR(50) NOT NULL,
                    resource VARCHAR(50) NOT NULL,
                    resource_id INTEGER,
                    ip_address VARCHAR(45),
                    user_agent VARCHAR(255),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    details JSON,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_action (action),
                    INDEX idx_resource (resource),
                    INDEX idx_timestamp (timestamp)
                )
            """))
            print("✓ Tabela 'audit_logs' criada")
        except Exception as e:
            print(f"Tabela 'audit_logs' já existe ou erro: {e}")


def update_existing_users():
    """Atualiza usuários existentes com valores padrão"""
    
    db = SessionLocal()
    try:
        # Define role ADMIN para o primeiro usuário (assumindo que é o admin)
        db.execute(text("""
            UPDATE users 
            SET role = 'ADMIN', is_active = TRUE 
            WHERE id = (SELECT MIN(id) FROM (SELECT id FROM users) AS temp)
        """))
        
        # Define role VIEWER para os demais usuários
        db.execute(text("""
            UPDATE users 
            SET role = 'VIEWER', is_active = TRUE 
            WHERE role IS NULL OR role = ''
        """))
        
        db.commit()
        print("✓ Usuários existentes atualizados com roles padrão")
    except Exception as e:
        print(f"Erro ao atualizar usuários existentes: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Executa todas as migrações"""
    print("=== Iniciando migração do banco de dados ===\n")
    
    print("1. Atualizando tabela 'users'...")
    migrate_user_table()
    print()
    
    print("2. Criando tabela 'audit_logs'...")
    create_audit_log_table()
    print()
    
    print("3. Atualizando usuários existentes...")
    update_existing_users()
    print()
    
    print("=== Migração concluída com sucesso! ===")


if __name__ == "__main__":
    main()
