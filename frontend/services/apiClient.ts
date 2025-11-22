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

  // OAuth2PasswordRequestForm **requires** x-www-form-urlencoded
  // Não usar FormData (multipart/form-data) — isso quebrou o login.
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)

  // Enviar como application/x-www-form-urlencoded
  return $fetch<{ access_token: string; token_type: string }>(
    `${baseURL}/api/v1/auth/token`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params.toString()
    }
  )
}

/**
 * Requisição para registro
 * @param username - Nome de usuário
 * @param email - Email do usuário
 * @param password - Senha
 */
export const registerRequest = (username: string, email: string, password: string) =>
  apiPost('/api/v1/auth/register', {
    username,
    email,
    password
  })

// ============================================
// API de Dashboard
// ============================================

export interface DashboardStatsResponse {
  total_clients: number
  active_reservas: number
  occupied_rooms: number
  total_rooms: number
  monthly_revenue: number
}

export interface DashboardActivityResponse {
  id: number
  description: string
  status: string
  event_type: string
  created_at: string
}

export interface DashboardSummaryResponse {
  stats: DashboardStatsResponse
  recent_activities: DashboardActivityResponse[]
}

export const getDashboardSummary = () => {
  return apiGet<DashboardSummaryResponse>('/api/v1/dashboard/')
}

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
  return apiGet<Client[]>(`/api/v1/clients/?skip=${skip}&limit=${limit}`)
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
  return apiPost<Client>('/api/v1/clients/', clientData)
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

// ============================================
// API de Quartos
// ============================================

export interface Room {
  id: number
  numero: string
  tipo: string
  status: string
  capacidade: number
  valor_diaria: number
  descricao?: string | null
}

export interface RoomCreate {
  numero: string
  tipo: string
  status?: string
  capacidade?: number
  valor_diaria: number
  descricao?: string
}

export interface RoomUpdate {
  numero?: string
  tipo?: string
  status?: string
  capacidade?: number
  valor_diaria?: number
  descricao?: string
}

export interface RoomCalendarDay {
  data: string
  status: string
  reserva_id?: number
  reserva_status?: string
  cliente_id?: number
}

export interface RoomCalendar {
  quarto_id: number
  numero: string
  tipo: string
  status: string
  capacidade: number
  valor_diaria: number
  periodo_inicio: string
  periodo_fim: string
  ocupacao: RoomCalendarDay[]
}

export const getRooms = (skip: number = 0, limit: number = 100) => {
  return apiGet<Room[]>(`/api/v1/quartos/?skip=${skip}&limit=${limit}`)
}

export const getRoom = (id: number) => {
  return apiGet<Room>(`/api/v1/quartos/${id}`)
}

export const createRoom = (roomData: RoomCreate) => {
  return apiPost<Room>('/api/v1/quartos/', roomData)
}

export const updateRoom = (id: number, roomData: RoomUpdate) => {
  return apiPut<Room>(`/api/v1/quartos/${id}`, roomData)
}

export const deleteRoom = (id: number) => {
  return apiDelete<void>(`/api/v1/quartos/${id}`)
}

export const getRoomCalendar = (
  dataInicio: string,
  dataFim: string
) => {
  const params = new URLSearchParams({
    data_inicio: dataInicio,
    data_fim: dataFim
  })
  return apiGet<RoomCalendar[]>(`/api/v1/quartos/calendario?${params.toString()}`)
}

// ============================================
// API de Reservas
// ============================================

export interface Reservation {
  id: number
  data_checkin: string
  data_checkout: string
  quarto_id: number
  client_id: number
  valor_total: number
  status: string
  quarto?: Room
  client?: Client
  created_at: string
  updated_at?: string | null
}

export interface ReservationCreate {
  quarto_id: number
  client_id: number
  data_checkin: string
  data_checkout: string
}

export interface ReservationUpdate {
  data_checkin?: string
  data_checkout?: string
  status?: string
}

interface ReservationListOptions {
  skip?: number
  limit?: number
  status?: string
  mes?: string
}

export const getReservations = ({
  skip = 0,
  limit = 100,
  status,
  mes
}: ReservationListOptions = {}) => {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit)
  })

  if (status) {
    params.set('status', status)
  }

  if (mes) {
    params.set('mes', mes)
  }

  return apiGet<Reservation[]>(`/api/v1/reservas/?${params.toString()}`)
}

export const getReservation = (id: number) => {
  return apiGet<Reservation>(`/api/v1/reservas/${id}`)
}

export const createReservation = (data: ReservationCreate) => {
  return apiPost<Reservation>('/api/v1/reservas/', data)
}

export const updateReservation = (
  id: number,
  data: ReservationUpdate
) => {
  return apiPut<Reservation>(`/api/v1/reservas/${id}`, data)
}

export const deleteReservation = (id: number) => {
  return apiDelete<Reservation>(`/api/v1/reservas/${id}`)
}
