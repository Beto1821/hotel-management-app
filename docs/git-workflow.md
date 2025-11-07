# Git Workflow Checklist

Use esta referência rápida para versionar mudanças com segurança.

## Checklist Antes do Commit
- backend executa sem erros
- dependências atualizadas em `backend/requirements.txt`
- README.MD ou docs relevantes atualizados
- `.gitignore` cobre arquivos temporários e credenciais
- nada sensível (tokens, `.db`, `.env`) será versionado

## Fluxo Padrão
```bash
# inicializar (apenas uma vez)
git init
git remote add origin https://github.com/SEU_USUARIO/hotel-management-app.git

# trabalho diário
git checkout -b feature/minha-feature   # crie branchs curtas
git status                              # verifique alterações
git add <arquivos>                      # selecione mudanças
git commit -m "feat: descreva sua mudança"
git push -u origin feature/minha-feature
```

## Commits Semânticos
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `style`: formatação sem impacto lógico
- `refactor`: alteração estrutural sem mudar comportamento
- `test`: testes ou fixtures
- `chore`: tarefas de suporte

### Exemplos
```bash
git commit -m "feat: add reservation endpoints"
git commit -m "fix: handle missing auth header"
```

## Verificações Rápidas
```bash
git diff                # compare mudanças
git log --oneline       # veja histórico resumido
git stash push          # guarde mudanças temporárias
```

## Segurança
- nunca faça commit de senhas ou chaves
- confirme que o arquivo `backend/app.db` não está versionado
- use variáveis de ambiente para credenciais

> Quando concluir uma feature, abra um Pull Request descrevendo testes executados e passos para QA.
