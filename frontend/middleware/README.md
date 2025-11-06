# 🔐 Middleware de Autenticação

Este diretório contém middlewares para proteção de rotas que requerem autenticação.

## 📁 Arquivos Disponíveis

### 1. `auth.ts` (Nuxt 3)
Middleware de rota usando `defineNuxtRouteMiddleware`.

### 2. `auth-nextjs.tsx` (Next.js)
HOC (Higher-Order Component) e componentes para proteção de rotas.

## 🚀 Como Usar

### Nuxt 3 (auth.ts)

#### 1. Proteção de Página Individual
```vue
<!-- pages/dashboard.vue -->
<template>
  <div>
    <h1>Dashboard Privado</h1>
    <p>Esta página requer autenticação</p>
  </div>
</template>

<script setup lang="ts">
// Definir middleware para esta página
definePageMeta({
  middleware: 'auth'
})
</script>
```

#### 2. Proteção de Layout
```vue
<!-- layouts/private.vue -->
<template>
  <div>
    <nav>Menu do usuário logado</nav>
    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
// Aplicar middleware ao layout
definePageMeta({
  middleware: 'auth'
})
</script>
```

#### 3. Proteção Global (nuxt.config.ts)
```typescript
export default defineNuxtConfig({
  // Aplicar middleware globalmente
  router: {
    middleware: ['auth']
  }
})
```

### Next.js (auth-nextjs.tsx)

#### 1. Higher-Order Component (HOC)
```tsx
// pages/dashboard.tsx
import { withAuth } from '../middleware/auth-nextjs'

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard Privado</h1>
      <p>Esta página requer autenticação</p>
    </div>
  )
}

// Proteger a página com o HOC
export default withAuth(Dashboard)
```

#### 2. Hook useAuthGuard
```tsx
// pages/profile.tsx
import { useAuthGuard } from '../middleware/auth-nextjs'

const Profile = () => {
  const { isAuthenticated, isLoading } = useAuthGuard()

  if (isLoading) {
    return <div>Carregando...</div>
  }

  if (!isAuthenticated) {
    return <div>Redirecionando...</div>
  }

  return (
    <div>
      <h1>Meu Perfil</h1>
      <p>Página protegida</p>
    </div>
  )
}

export default Profile
```

#### 3. Componente AuthGuard
```tsx
// pages/settings.tsx
import { AuthGuard } from '../middleware/auth-nextjs'

const Settings = () => {
  return (
    <AuthGuard fallback={<div>Verificando permissões...</div>}>
      <div>
        <h1>Configurações</h1>
        <p>Conteúdo protegido</p>
      </div>
    </AuthGuard>
  )
}

export default Settings
```

#### 4. Proteção de Layout
```tsx
// components/PrivateLayout.tsx
import { AuthGuard } from '../middleware/auth-nextjs'

interface PrivateLayoutProps {
  children: React.ReactNode
}

const PrivateLayout: React.FC<PrivateLayoutProps> = ({ children }) => {
  return (
    <AuthGuard>
      <nav>
        <h2>Menu Privado</h2>
        {/* Menu do usuário */}
      </nav>
      <main>{children}</main>
    </AuthGuard>
  )
}

export default PrivateLayout
```

## 🔧 Configuração Avançada

### Nuxt 3 - Middleware Condicional

```typescript
// middleware/auth.ts - Versão avançada
export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated, token, isTokenValid } = useAuth()

  // Rotas que não precisam de autenticação
  const publicRoutes = ['/login', '/register', '/', '/about']
  
  if (publicRoutes.includes(to.path)) {
    return true
  }

  // Verificar autenticação para rotas privadas
  if (!isAuthenticated.value || !isTokenValid()) {
    // Salvar rota de destino para redirecionamento após login
    const redirectPath = to.fullPath
    return navigateTo(`/login?redirect=${encodeURIComponent(redirectPath)}`)
  }

  return true
})
```

### Next.js - Middleware com Permissões

```tsx
// middleware/auth-nextjs.tsx - Versão com roles
interface AuthOptions {
  requiredRoles?: string[]
  redirectTo?: string
}

export const withAuth = <T extends object>(
  WrappedComponent: React.ComponentType<T>,
  options: AuthOptions = {}
) => {
  const AuthenticatedComponent = (props: T) => {
    const { isAuthenticated, isLoading, getUserFromToken } = useAuth()
    const router = useRouter()
    
    const { requiredRoles = [], redirectTo = '/login' } = options

    useEffect(() => {
      if (isLoading) return

      if (!isAuthenticated) {
        router.push(redirectTo)
        return
      }

      // Verificar roles se especificado
      if (requiredRoles.length > 0) {
        const user = getUserFromToken()
        const userRoles = user?.roles || []
        
        const hasPermission = requiredRoles.some(role => 
          userRoles.includes(role)
        )

        if (!hasPermission) {
          router.push('/unauthorized')
          return
        }
      }
    }, [isAuthenticated, isLoading])

    if (isLoading || !isAuthenticated) {
      return <div>Carregando...</div>
    }

    return <WrappedComponent {...props} />
  }

  return AuthenticatedComponent
}

// Uso com roles
export default withAuth(AdminPanel, { 
  requiredRoles: ['admin'], 
  redirectTo: '/unauthorized' 
})
```

## 🛡️ Funcionalidades de Segurança

### Verificações Implementadas
- ✅ **Token existe** - Verifica se o usuário tem token
- ✅ **Token válido** - Verifica se o token não expirou
- ✅ **Redirecionamento** - Redireciona para login se não autenticado
- ✅ **Logout automático** - Limpa token inválido
- ✅ **Estado de loading** - Evita flash de conteúdo não autorizado

### Fluxo de Segurança
1. **Verificar autenticação** - Hook/composable useAuth
2. **Validar token** - Verificar expiração JWT
3. **Redirecionar** - Se não autenticado, vai para /login
4. **Renderizar** - Se autenticado, mostra o conteúdo

## 🧪 Testando Middleware

### Cenários de Teste

#### 1. Usuário não autenticado
```bash
# Deve redirecionar para /login
curl -I http://localhost:3000/dashboard
```

#### 2. Token expirado
```typescript
// Simular token expirado no localStorage
localStorage.setItem('auth_token', 'token.expirado.aqui')
// Acessar página protegida - deve redirecionar
```

#### 3. Usuário autenticado
```typescript
// Login válido
const { login } = useAuth()
login('token.valido.jwt')
// Acessar página protegida - deve funcionar
```

## ⚠️ Considerações Importantes

### Server-Side Rendering (SSR)
- Middleware funciona apenas no cliente
- Para SSR, use verificação adicional nos plugins
- Considere usar `process.server` para verificações

### Performance
- Middleware é executado a cada mudança de rota
- Cache o resultado da validação quando possível
- Use `computed` properties para otimizar

### UX (User Experience)
- Mostre loading states apropriados
- Evite redirecionamentos desnecessários
- Preserve a rota de destino após login