# Hotel Management App - Git Setup

Este arquivo contém instruções para configurar o Git e subir o projeto para o GitHub.

## 📋 Checklist antes do commit

- [ ] Backend funcionando
- [ ] Dependências documentadas no requirements.txt
- [ ] README.md atualizado
- [ ] .gitignore configurado
- [ ] Variáveis sensíveis removidas do código

## 🚀 Comandos para subir para o GitHub

### 1. Inicializar repositório Git (se ainda não foi feito)
```bash
git init
```

### 2. Adicionar todos os arquivos
```bash
git add .
```

### 3. Fazer o primeiro commit
```bash
git commit -m "🎉 Initial commit: Hotel Management App with FastAPI backend"
```

### 4. Renomear branch para main (opcional)
```bash
git branch -M main
```

### 5. Adicionar origem remota (substitua pela sua URL)
```bash
git remote add origin https://github.com/SEU_USUARIO/hotel-management-app.git
```

### 6. Push para o GitHub
```bash
git push -u origin main
```

## 🔧 Comandos úteis do Git

### Status dos arquivos
```bash
git status
```

### Ver diferenças
```bash
git diff
```

### Histórico de commits
```bash
git log --oneline
```

### Criar nova branch
```bash
git checkout -b feature/nova-funcionalidade
```

## ⚠️ Verificações de Segurança

Antes de fazer push, verifique se não há:
- [ ] Senhas hardcoded
- [ ] Chaves API expostas
- [ ] Tokens de desenvolvimento
- [ ] Arquivos de banco de dados (.db)
- [ ] Variáveis de ambiente sensíveis

## 📝 Padrões de Commit

Use commits semânticos:
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação
- `refactor:` - Refatoração de código
- `test:` - Testes
- `chore:` - Tarefas de manutenção

### Exemplos:
```bash
git commit -m "feat: add user authentication endpoints"
git commit -m "fix: resolve database connection issue"
git commit -m "docs: update API documentation"
```