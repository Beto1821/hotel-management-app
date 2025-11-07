# 🚀 Instruções para Execução do Frontend (Nuxt 3)

## 📋 Pré-requisitos
- Node.js (versão 16+ recomendada)
- npm ou yarn

## 🔧 Instalação

1. **Navegue para o diretório do frontend:**
```bash
cd frontend
```

2. **Configure as variáveis de ambiente:**
```bash
# Copie o arquivo .env.example para .env
cp .env.example .env

# Edite o arquivo .env se necessário
# O valor padrão já está configurado para desenvolvimento local
```

O arquivo `.env` contém:
```env
API_BASE_URL=http://localhost:8000
```

3. **Instale as dependências:**
```bash
npm install
# ou
yarn install
```

## 🏃‍♂️ Execução

1. **Inicie o servidor de desenvolvimento:**
```bash
npm run dev
# ou
yarn dev
```

O frontend estará disponível em: http://localhost:3000

## 🛠️ Scripts Disponíveis

- `npm run dev` - Inicia o servidor de desenvolvimento
- `npm run build` - Compila o projeto para produção  
- `npm run generate` - Gera o site estático
- `npm run preview` - Visualiza a build de produção

## 🔐 Sistema de Autenticação

### Fluxo de Autenticação:
1. **Login:** `/login` - Página de login com formulário
2. **Dashboard:** `/` - Página principal protegida por middleware
3. **Rotas Protegidas:** Todas as páginas exceto login são protegidas

### Middleware de Autenticação:
- Localizado em `middleware/auth.ts`
- Verifica automaticamente o token JWT
- Redireciona para login se não autenticado

### Composables:
- `useAuth()` - Gerencia estado de autenticação
- Funções: `login()`, `logout()`, `isAuthenticated`

## 📁 Estrutura do Projeto

```
frontend/
├── app.vue                 # Componente raiz do Nuxt
├── nuxt.config.ts         # Configuração do Nuxt
├── package.json           # Dependências e scripts
├── tailwind.config.js     # Configuração do Tailwind
├── assets/
│   └── css/
│       └── main.css       # Estilos globais
├── components/            # Componentes reutilizáveis
├── composables/
│   └── useAuth.ts        # Lógica de autenticação Vue 3
├── middleware/
│   └── auth.ts           # Middleware de proteção de rotas
├── pages/
│   ├── index.vue         # Dashboard principal
│   └── login.vue         # Página de login
├── services/
│   └── api.ts           # Serviços de API
└── public/              # Arquivos estáticos
```

## ⚙️ Configuração de Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configuração flexível:

### Arquivo .env
```env
# URL do backend FastAPI
API_BASE_URL=http://localhost:8000
```

### Como Usar
- Para **desenvolvimento local**: use o valor padrão `http://localhost:8000`
- Para **produção**: altere para a URL do seu servidor de produção
- As variáveis são carregadas automaticamente pelo Nuxt 3
- Acesse via `useRuntimeConfig().public.apiUrl` nos componentes

### Importante
- O arquivo `.env` está no `.gitignore` e não deve ser commitado
- Use `.env.example` como referência para criar seu `.env`
- Nunca commit segredos ou tokens no repositório

## 🎨 Estilização

O projeto usa **Tailwind CSS** para estilização:
- Classes utilitárias para rapidez no desenvolvimento
- Componentes customizados definidos em `assets/css/main.css`
- Design responsivo e moderno

## 🔗 Integração com Backend

- **Base URL:** http://localhost:8000 (configurável em `nuxt.config.ts`)
- **Endpoints utilizados:**
  - POST `/token` - Login/autenticação
  - POST `/register` - Registro de usuários

## ⚡ Funcionalidades Implementadas

### ✅ Dashboard (index.vue)
- Página principal protegida
- Estatísticas do hotel (cards informativos)
- Links para futuras páginas (Clientes, Agendamentos, Quartos)
- Atividades recentes
- Botão de logout funcional

### ✅ Sistema de Autenticação
- Login com validação de formulário
- Armazenamento seguro de token JWT
- Middleware de proteção automática
- Redirecionamento inteligente

### 🔜 Próximas Funcionalidades
- Página de Clientes
- Página de Agendamentos  
- Página de Quartos
- CRUD completo para entidades do hotel

## 🐛 Solução de Problemas

1. **Erro de módulos TypeScript:** 
   ```bash
   npm install
   # Reinicie o VS Code se necessário
   ```

2. **Erro de importações:** 
   - Verifique se todas as dependências estão instaladas
   - Execute `npm run dev` para inicializar o Nuxt

3. **Backend não responde:**
   - Verifique se o FastAPI está rodando na porta 8000
   - Confirme a URL da API em `nuxt.config.ts`

## 📝 Notas Importantes

- O middleware `auth` é aplicado automaticamente nas páginas
- Use `definePageMeta({ middleware: ['auth'] })` para proteger rotas
- O token JWT é armazenado no localStorage
- Navegação programática com `navigateTo()`