# 🔐 Páginas de Login

Este diretório contém as páginas de login para diferentes frameworks.

## 📁 Arquivos Disponíveis

### 1. `login.vue` (Nuxt 3/Vue 3)
Página de login em formato Single File Component (.vue).

### 2. `login-nextjs.tsx` (Next.js/React)
Página de login em formato React component (.tsx).

## ✨ Funcionalidades Implementadas

### 🎨 **Interface Completa:**
- ✅ **Design moderno** com Tailwind CSS
- ✅ **Formulário responsivo** para desktop e mobile
- ✅ **Estados visuais** (loading, erro, sucesso)
- ✅ **Accessibility** com labels e aria-labels
- ✅ **UX otimizada** com feedbacks visuais

### 🔧 **Funcionalidades:**
- ✅ **Campos reativos** (username e password)
- ✅ **Validação** de campos obrigatórios
- ✅ **Integração com API** usando form-data OAuth2
- ✅ **Tratamento de erros** com mensagens específicas
- ✅ **Loading states** com spinner animado
- ✅ **Credenciais demo** para teste rápido

### 🛡️ **Segurança:**
- ✅ **Integração com useAuth** composable/hook
- ✅ **Token JWT** salvo automaticamente
- ✅ **Redirecionamento** após login bem-sucedido
- ✅ **Prevenção de CSRF** com form submission
- ✅ **Validação client-side** e server-side

## 🚀 Como Usar

### Nuxt 3 (login.vue)

#### 1. Colocar no diretório pages/
```
pages/
└── login.vue
```

#### 2. Configurar variáveis de ambiente
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
    }
  }
})
```

#### 3. Acessar a página
```
http://localhost:3000/login
```

### Next.js (login-nextjs.tsx)

#### 1. Colocar no diretório pages/
```
pages/
└── login.tsx  # Renomear de login-nextjs.tsx
```

#### 2. Configurar variáveis de ambiente
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

#### 3. Acessar a página
```
http://localhost:3000/login
```

## 🎯 Fluxo de Autenticação

### 1. **Usuário preenche formulário**
```
Username: testuser
Password: 123456
```

### 2. **Submit do formulário**
- Validação client-side
- Loading state ativado
- Requisição para API

### 3. **Requisição para API**
```javascript
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=testuser&password=123456
```

### 4. **Resposta da API**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 5. **Sucesso**
- Token salvo via useAuth
- Mensagem de sucesso
- Redirecionamento para home

### 6. **Erro**
- Mensagem de erro específica
- Form liberado para nova tentativa

## 🎨 Componentes Visuais

### Estados da Interface

#### 1. **Estado Normal**
- Campos habilitados
- Botão "Entrar" disponível
- Ícone de cadeado

#### 2. **Estado Loading**
- Campos desabilitados
- Botão "Entrando..." com spinner
- Cursor not-allowed

#### 3. **Estado Erro**
- Alert vermelho com mensagem
- Campos liberados
- Foco no primeiro campo

#### 4. **Estado Sucesso**
- Alert verde com confirmação
- Redirecionamento automático

### Credenciais de Demonstração
```
Usuário: testuser
Senha: 123456
```

Botão para preenchimento automático disponível.

## 🔧 Personalização

### Tailwind CSS Classes

#### Cores e Tema
```css
/* Primária: Blue-600 */
bg-blue-600 hover:bg-blue-700

/* Sucesso: Green-50/400/800 */
bg-green-50 text-green-800

/* Erro: Red-50/400/800 */
bg-red-50 text-red-800
```

#### Layout Responsivo
```css
/* Mobile First */
px-4 sm:px-6 lg:px-8
max-w-md w-full
```

### Customizar Mensagens
```vue
<!-- Nuxt 3 -->
<script setup>
const messages = {
  success: 'Login realizado com sucesso!',
  errorAuth: 'Usuário ou senha incorretos',
  errorServer: 'Erro interno do servidor',
  errorNetwork: 'Erro de conexão'
}
</script>
```

```tsx
// Next.js
const messages = {
  success: 'Login realizado com sucesso!',
  errorAuth: 'Usuário ou senha incorretos',
  errorServer: 'Erro interno do servidor',
  errorNetwork: 'Erro de conexão'
}
```

## 🧪 Testes

### Cenários de Teste

#### 1. **Login Válido**
```
Input: testuser / 123456
Expected: Redirect para home
```

#### 2. **Credenciais Inválidas**
```
Input: wronguser / wrongpass
Expected: Mensagem "Usuário ou senha incorretos"
```

#### 3. **Campos Vazios**
```
Input: "" / ""
Expected: Mensagem "Preencha todos os campos"
```

#### 4. **API Offline**
```
Expected: Mensagem "Erro de conexão"
```

### Teste Manual
1. Executar backend (`uvicorn main:app --reload`)
2. Executar frontend (`npm run dev`)
3. Acessar `/login`
4. Testar todos os cenários acima

## 📱 Responsividade

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px

### Adaptações Mobile
- Form ocupa largura total
- Padding reduzido
- Fonte menor em alguns elementos
- Touch targets maiores

## 🔗 Integração com Middleware

As páginas têm configuração especial para não aplicar middleware de auth:

### Nuxt 3
```vue
<script setup>
definePageMeta({
  middleware: [] // Não aplicar auth middleware
})
</script>
```

### Next.js
```tsx
// Não usar withAuth() HOC nesta página
export default LoginPage // Sem wrapper
```

## 📋 SEO e Meta Tags

### Nuxt 3
```vue
<script setup>
useHead({
  title: 'Login - Hotel Management',
  meta: [
    { name: 'description', content: 'Faça login no sistema' }
  ]
})
</script>
```

### Next.js
```tsx
<Head>
  <title>Login - Hotel Management</title>
  <meta name="description" content="Faça login no sistema" />
</Head>
```

## ✅ Checklist de Implementação

- [x] Interface responsiva com Tailwind
- [x] Campos reativos (username/password)
- [x] Integração com useAuth composable/hook
- [x] Requisição OAuth2 form-data
- [x] Estados de loading/erro/sucesso
- [x] Credenciais de demonstração
- [x] Validação client-side
- [x] Tratamento robusto de erros
- [x] Redirecionamento após login
- [x] SEO e acessibilidade
- [x] Documentação completa