/**
 * Cliente API para Nuxt 3
 * Centraliza as requisições HTTP com autenticação automática
 */

/**
 * Função para fazer requisições HTTP autenticadas
 * @param endpoint - Endpoint da API (ex: '/auth/login', '/users')
 * @param options - Opções adicionais do RequestInit
 * @returns Promise com a resposta da API
 */
export const apiClient = async <T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  // Obter configuração do runtime (variáveis de ambiente)
  const config = useRuntimeConfig()

  // Obter token de autenticação usando o composable
  const { getAuthHeader } = useAuth()

  // URL base da API
  const baseURL = config.public.apiUrl || 'http://127.0.0.1:8000'

  // Construir URL completa
  const url = `${baseURL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`

  // Headers padrão
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json'
  }

  // Adicionar token de autenticação se disponível
  const authHeader = getAuthHeader()
  if (authHeader) {
    defaultHeaders.Authorization = authHeader
  }

  // Combinar headers
  const headers = {
    ...defaultHeaders,
    ...options.headers
  }

  // Opções finais da requisição
  const requestOptions = {
    ...options,
    headers
  } as any

  try {
    // Fazer requisição usando $fetch do Nuxt
    const response = await $fetch<T>(url, requestOptions)
    return response
  } catch (error: any) {
    // Tratar erros específicos
    if (error.status === 401) {
      // Token inválido/expirado, fazer logout
      const { logout } = useAuth()
      logout()

      // Redirecionar para login (opcional)
      if (typeof navigateTo !== 'undefined') {
        await navigateTo('/login')
      }
    }

    // Re-lançar o erro para tratamento no componente
    throw error
  }
}

/**
 * Funções auxiliares para métodos HTTP específicos
 */

/**
 * Requisição GET
 * @param endpoint - Endpoint da API
 * @param options - Opções adicionais
 */
export const apiGet = <T = any>(
  endpoint: string,
  options: Omit<RequestInit, 'method'> = {}
) => {
  return apiClient<T>(endpoint, { ...options, method: 'GET' })
}

/**
 * Requisição POST
 * @param endpoint - Endpoint da API
 * @param data - Dados para enviar
 * @param options - Opções adicionais
 */
export const apiPost = <T = any>(
  endpoint: string,
  data?: any,
  options: Omit<RequestInit, 'method' | 'body'> = {}
) => {
  return apiClient<T>(endpoint, {
    ...options,
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined
  })
}

/**
 * Requisição PUT
 * @param endpoint - Endpoint da API
 * @param data - Dados para enviar
 * @param options - Opções adicionais
 */
export const apiPut = <T = any>(
  endpoint: string,
  data?: any,
  options: Omit<RequestInit, 'method' | 'body'> = {}
) => {
  return apiClient<T>(endpoint, {
    ...options,
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined
  })
}

/**
 * Requisição DELETE
 * @param endpoint - Endpoint da API
 * @param options - Opções adicionais
 */
export const apiDelete = <T = any>(
  endpoint: string,
  options: Omit<RequestInit, 'method'> = {}
) => {
  return apiClient<T>(endpoint, { ...options, method: 'DELETE' })
}

/**
 * Requisição para login (form-data)
 * @param username - Nome de usuário
 * @param password - Senha
 */
export const loginRequest = (username: string, password: string) => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiUrl || 'http://127.0.0.1:8000'

  // Usar FormData para login (OAuth2PasswordRequestForm)
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)

  return $fetch<{ access_token: string; token_type: string }>(
    `${baseURL}/api/v1/auth/token`,
    {
      method: 'POST',
      body: formData
    }
  )
}

/**
 * Requisição para registro
 * @param username - Nome de usuário
 * @param password - Senha
 */
export const registerRequest = (username: string, password: string) =>
  apiPost('/api/v1/auth/register', {
    username,
    password
  })

// ============================================
// API de Clientes
// ============================================

/**
 * Interface para Cliente
 */
export interface Client {
  id: number
  name: string
  email: string
  phone: string
  document: string
  address?: string
  created_at: string
  updated_at?: string
}

/**
 * Interface para criar cliente
 */
export interface ClientCreate {
  name: string
  email: string
  phone: string
  document: string
  address?: string
}

/**
 * Interface para atualizar cliente
 */
export interface ClientUpdate {
  name?: string
  email?: string
  phone?: string
  document?: string
  address?: string
}

/**
 * Listar todos os clientes
 * @param skip - Número de registros para pular (paginação)
 * @param limit - Limite de registros por página
 */
export const getClients = (skip: number = 0, limit: number = 100) => {
  return apiGet<Client[]>(`/api/v1/clients?skip=${skip}&limit=${limit}`)
}

/**
 * Buscar cliente por ID
 * @param id - ID do cliente
 */
export const getClient = (id: number) => {
  return apiGet<Client>(`/api/v1/clients/${id}`)
}

/**
 * Criar novo cliente
 * @param clientData - Dados do cliente
 */
export const createClient = (clientData: ClientCreate) => {
  return apiPost<Client>('/api/v1/clients', clientData)
}

/**
 * Atualizar cliente existente
 * @param id - ID do cliente
 * @param clientData - Dados atualizados do cliente
 */
export const updateClient = (id: number, clientData: ClientUpdate) => {
  return apiPut<Client>(`/api/v1/clients/${id}`, clientData)
}

/**
 * Excluir cliente
 * @param id - ID do cliente
 */
export const deleteClient = (id: number) => {
  return apiDelete<void>(`/api/v1/clients/${id}`)
}

/**
 * Buscar clientes por nome ou email
 * @param query - Termo de busca
 * @param skip - Número de registros para pular
 * @param limit - Limite de registros por página
 */
export const searchClients = (query: string, skip: number = 0, limit: number = 100) => {
  return apiGet<Client[]>(`/api/v1/clients/search?q=${encodeURIComponent(query)}&skip=${skip}&limit=${limit}`)
}
