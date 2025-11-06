# 🌐 API Client Services

Este diretório contém os utilitários para comunicação com a API backend.

## 📁 Arquivos Disponíveis

### 1. `apiClient.ts` (Nuxt 3)
Cliente API para projetos Nuxt 3 usando `$fetch` e `useRuntimeConfig`.

### 2. `apiClient-nextjs.ts` (Next.js)
Cliente API para projetos Next.js/React usando `fetch` nativo.

## 🚀 Configuração

### Variáveis de Ambiente

#### Nuxt 3 (nuxt.config.ts)
```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
    }
  }
})
```

#### Next.js (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## 🔧 Como Usar

### Nuxt 3 (apiClient.ts)

```vue
<template>
  <div>
    <button @click="login">Login</button>
    <button @click="getUsers">Carregar Usuários</button>
  </div>
</template>

<script setup lang="ts">
import { apiPost, apiGet, loginRequest } from '~/services/apiClient'

// Login
const login = async () => {
  try {
    const response = await loginRequest('testuser', '123456')
    const { login } = useAuth()
    login(response.access_token)
  } catch (error) {
    console.error('Erro no login:', error)
  }
}

// Requisição autenticada
const getUsers = async () => {
  try {
    const users = await apiGet('/api/v1/users')
    console.log('Usuários:', users)
  } catch (error) {
    console.error('Erro:', error)
  }
}
</script>
```

### Next.js (apiClient-nextjs.ts)

```tsx
import React from 'react'
import { apiPost, apiGet, loginRequest } from '../services/apiClient-nextjs'
import { useAuth } from '../hooks/useAuth'

const ApiExample = () => {
  const { login } = useAuth()

  // Login
  const handleLogin = async () => {
    try {
      const response = await loginRequest('testuser', '123456')
      login(response.access_token)
    } catch (error) {
      console.error('Erro no login:', error)
    }
  }

  // Requisição autenticada
  const fetchUsers = async () => {
    try {
      const users = await apiGet('/api/v1/users')
      console.log('Usuários:', users)
    } catch (error) {
      console.error('Erro:', error)
    }
  }

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={fetchUsers}>Carregar Usuários</button>
    </div>
  )
}

export default ApiExample
```

## 🔐 Autenticação Automática

Os clientes de API automaticamente:
- ✅ Adicionam o token JWT no header `Authorization`
- ✅ Tratam erros 401 (não autorizado)
- ✅ Fazem logout automático em caso de token inválido
- ✅ Redirecionam para login (opcional)

## 📚 API Disponível

### Funções Principais

#### `apiClient(endpoint, options)`
Função principal para requisições HTTP com autenticação automática.

#### Métodos HTTP Específicos
- `apiGet(endpoint, options)` - Requisição GET
- `apiPost(endpoint, data, options)` - Requisição POST
- `apiPut(endpoint, data, options)` - Requisição PUT  
- `apiDelete(endpoint, options)` - Requisição DELETE

#### Funções de Autenticação
- `loginRequest(username, password)` - Login com form-data
- `registerRequest(username, password)` - Registro de usuário

#### Utilitários
- `healthCheck()` - Verificar status da API
- `getApiInfo()` - Informações da API

## 🛡️ Tratamento de Erros

### Erros Comuns

#### 401 - Não Autorizado
```typescript
try {
  const data = await apiGet('/protected-endpoint')
} catch (error) {
  // Token inválido - usuário será deslogado automaticamente
  console.error('Não autorizado:', error.message)
}
```

#### Outros Erros HTTP
```typescript
try {
  const data = await apiPost('/endpoint', { invalid: 'data' })
} catch (error) {
  console.error('Erro:', error.message) // Mensagem da API ou erro genérico
}
```

#### Erro de Conexão
```typescript
try {
  const data = await apiGet('/endpoint')
} catch (error) {
  if (error.message.includes('fetch')) {
    console.error('Erro de conexão com a API')
  }
}
```

## 🧪 Exemplos Avançados

### Upload de Arquivo
```typescript
const uploadFile = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return apiClient('/api/v1/upload', {
    method: 'POST',
    body: formData,
    // Não definir Content-Type para FormData
    headers: {} 
  })
}
```

### Requisição com Query Parameters
```typescript
const getUsers = async (page: number = 1, limit: number = 10) => {
  return apiGet(`/api/v1/users?page=${page}&limit=${limit}`)
}
```

### Interceptador de Response
```typescript
const apiClientWithInterceptor = async <T>(endpoint: string, options: RequestInit = {}) => {
  try {
    const response = await apiClient<T>(endpoint, options)
    
    // Log de todas as requisições
    console.log(`✅ ${options.method || 'GET'} ${endpoint}:`, response)
    
    return response
  } catch (error) {
    // Log de erros
    console.error(`❌ ${options.method || 'GET'} ${endpoint}:`, error)
    throw error
  }
}
```

## ⚙️ Configurações Avançadas

### Timeout Personalizado
```typescript
const apiWithTimeout = (endpoint: string, timeout: number = 5000) => {
  const controller = new AbortController()
  
  setTimeout(() => controller.abort(), timeout)
  
  return apiClient(endpoint, {
    signal: controller.signal
  })
}
```

### Headers Personalizados
```typescript
const apiWithCustomHeaders = (endpoint: string, customHeaders: Record<string, string>) => {
  return apiClient(endpoint, {
    headers: customHeaders
  })
}
```