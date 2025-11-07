# Manutenção e Limpeza do Projeto

Resumo das ações já executadas para manter o repositório enxuto e como repetir o processo.

## Histórico de Limpezas
- removidos arquivos herdados do antigo frontend Next.js (configurações, hooks, páginas duplicadas)
- excluídas pastas vazias da estrutura do frontend (`src/`, `hooks/`)
- centralização da documentação no README principal e nesta pasta `docs`

## Estrutura Atual (abridged)
```
hotel_app/
├── backend/            # FastAPI + SQLAlchemy
├── frontend/           # Nuxt 3 + Tailwind CSS
├── docs/               # Documentação complementar
└── README.MD           # Visão geral e onboarding
```

## Checklist de Limpeza Periódica
- [ ] remover arquivos gerados automaticamente (`__pycache__`, `.pytest_cache`, `.nuxt`)
- [ ] garantir que arquivos de banco locais (`app.db`) não estejam versionados
- [ ] revisar duplicidades entre README e docs auxiliares
- [ ] atualizar capturas de tela em `frontend/public/` quando o layout mudar

## Como auditar rapidamente
```bash
# localizar possíveis duplicidades markdown
git ls-files '*.md' | sort

# identificar arquivos grandes ou fora do padrão
find . -type f -size +5M

# listar dependências não utilizadas (exemplos)
pip list --not-required
npm prune --dry-run
```

> Necessidades de limpeza adicionais (novos módulos, remoções ou merges) devem ser registradas em issues para manter rastreabilidade.
