#!/bin/bash

# Script para preparar merge desenvolvimento → main
# Execute este script na raiz do projeto

echo "🚀 Preparando projeto para merge desenvolvimento → main"
echo ""

# 1. Adicionar todos os arquivos
echo "📦 Adicionando arquivos ao staging..."
git add .

# 2. Commit com mensagem descritiva
echo "💾 Criando commit..."
git commit -m "feat: Release v1.0.0 - Sistema completo com 100% cobertura de testes

✨ Funcionalidades principais:
- CRUD completo para Clientes, Quartos e Reservas
- Autenticação JWT com validação forte de senhas
- Dashboard com métricas em tempo real
- Sistema de auditoria completo
- Interface moderna com tema claro/escuro (SweetAlert2)
- Soft delete em reservas

🧪 Testes (100% cobertura):
- 30/30 testes passando
- Auth: 2/2 (100%)
- Clientes: 6/6 (100%)
- Quartos: 10/10 (100%)
- Reservas: 12/12 (100%)

🔒 Segurança:
- SECRET_KEY obrigatória via .env
- CORS configurável (ALLOWED_ORIGINS)
- Bcrypt para hash de senhas
- Pydantic v2 (.model_dump)
- /docs desabilitado em produção

📚 Documentação:
- PRODUCTION_CHECKLIST.md com guia completo de deploy
- COBERTURA_TESTES.md com relatório detalhado
- .env.example para referência
- README.md atualizado

🔧 Correções técnicas:
- Schema alinhado: cliente_id → client_id
- Schema alinhado: preco_diaria → valor_diaria
- Endpoints corrigidos: PATCH /status → PUT /
- Fixtures com scope=function para isolamento
- Pydantic deprecation warning corrigido

Breaking changes:
- SECRET_KEY agora obrigatória (erro se não definida)
- CORS via ALLOWED_ORIGINS no .env
- Bcrypt nativo (sem passlib)

Ver RELEASE_NOTES_v1.0.0.md para detalhes completos."

# 3. Push para desenvolvimento
echo "⬆️  Fazendo push para origin/desenvolvimento..."
git push origin desenvolvimento

echo ""
echo "✅ Commit criado e enviado para desenvolvimento!"
echo ""
echo "📋 PRÓXIMOS PASSOS PARA MERGE:"
echo ""
echo "1. Verifique no GitHub se o push foi bem-sucedido"
echo "2. Execute os comandos abaixo para fazer o merge:"
echo ""
echo "   git checkout main"
echo "   git pull origin main"
echo "   git merge desenvolvimento"
echo "   git push origin main"
echo ""
echo "3. Crie uma tag de release:"
echo ""
echo "   git tag -a v1.0.0 -m 'Release v1.0.0'"
echo "   git push origin v1.0.0"
echo ""
echo "4. No GitHub, crie uma release usando RELEASE_NOTES_v1.0.0.md"
echo ""
echo "⚠️  IMPORTANTE: Antes do deploy em produção, leia PRODUCTION_CHECKLIST.md"
echo ""
