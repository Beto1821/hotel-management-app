# 🔐 Composables/Hooks de Autenticação

Este diretório contém os utilitários de autenticação para diferentes frameworks.

## 📁 Arquivos Disponíveis

### 1. `useAuth.ts` (Vue 3/Nuxt 3)
Composable para projetos Vue 3 e Nuxt 3.

### 2. `../hooks/useAuth.ts` (Next.js/React)
Hook customizado para projetos Next.js e React.

## 🚀 Como Usar

### Vue 3/Nuxt 3 (composables/useAuth.ts)

```vue
<template>
  <div>
    <div v-if="isAuthenticated">
      <p>Usuário logado!</p>
      <button @click="logout">Sair</button>
    </div>
    <div v-else>
      <button @click="handleLogin">Entrar</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'

const { isAuthenticated, login, logout, getAuthHeader } = useAuth()

const handleLogin = () => {
  // Após receber o token da API
  const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
  login(token)
}

// Usar em requisições HTTP
const authHeader = getAuthHeader() // "Bearer token..."
</script>
```

### Next.js/React (hooks/useAuth.ts)

```tsx
import React from 'react'
import { useAuth } from '../hooks/useAuth'

const LoginComponent = () => {
  const { isAuthenticated, login, logout, getAuthHeader, isLoading } = useAuth()

  if (isLoading) {
    return <div>Carregando...</div>
  }

  const handleLogin = () => {
    // Após receber o token da API
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    login(token)
  }

  return (
    <div>
      {isAuthenticated ? (
        <div>
          <p>Usuário logado!</p>
          <button onClick={logout}>Sair</button>
        </div>
      ) : (
        <button onClick={handleLogin}>Entrar</button>
      )}
    </div>
  )
}

export default LoginComponent
```

## 🔧 API do Composable/Hook

### Estado
- `token`: Token JWT atual (string | null)
- `isAuthenticated`: Boolean indicando se o usuário está logado
- `isLoading`: (Apenas React) Boolean indicando carregamento inicial

### Funções
- `login(token: string)`: Salva o token e marca como autenticado
- `logout()`: Remove o token e desmarca autenticação
- `getAuthHeader()`: Retorna header Authorization formatado
- `isTokenValid()`: Verifica se o token ainda é válido
- `getUserFromToken()`: (Apenas React) Extrai dados do usuário do token

## 💾 Persistência

O token é automaticamente salvo no `localStorage` e restaurado na inicialização da aplicação.

## 🔒 Segurança

- Verificação automática de expiração do token
- Limpeza automática de tokens inválidos
- Validação de estrutura JWT básica

## 🧪 Exemplo de Integração com API

```typescript
// Exemplo de login com a API
const loginUser = async (username: string, password: string) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username,
        password
      })
    })

    const data = await response.json()
    
    if (response.ok) {
      login(data.access_token)
      return { success: true }
    } else {
      return { success: false, error: data.detail }
    }
  } catch (error) {
    return { success: false, error: 'Erro de conexão' }
  }
}

// Exemplo de requisição autenticada
const fetchProtectedData = async () => {
  const authHeader = getAuthHeader()
  
  if (!authHeader) {
    throw new Error('Usuário não autenticado')
  }

  const response = await fetch('http://127.0.0.1:8000/api/v1/protected', {
    headers: {
      'Authorization': authHeader
    }
  })

  return response.json()
}
```