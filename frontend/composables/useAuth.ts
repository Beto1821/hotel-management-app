import { computed, readonly } from 'vue'

const TOKEN_STORAGE_KEY = 'auth_token'

/**
 * Função auxiliar para validar tokens JWT no lado do cliente.
 * Retorna true quando o token possui payload com exp no futuro.
 */
const isJwtValid = (jwt: string | null): boolean => {
  if (!jwt || typeof jwt !== 'string') {
    return false
  }

  // Em ambiente server-side não há acesso ao window/atob.
  if (typeof window === 'undefined' || typeof window.atob !== 'function') {
    return true
  }

  try {
    const parts = jwt.split('.')
    if (parts.length < 2) {
      return false
    }

    const payload = JSON.parse(window.atob(parts[1]))
    const currentTime = Math.floor(Date.now() / 1000)

    return typeof payload.exp === 'number' && payload.exp > currentTime
  } catch (_error) {
    return false
  }
}

/**
 * Composable para gerenciamento de autenticação
 * Controla o estado do token JWT e funções de login/logout
 */
export const useAuth = () => {
  // Utilizar estado global do Nuxt para compartilhar o token entre componentes
  const token = useState<string | null>('auth.token', () => null)
  const initialized = useState<boolean>('auth.initialized', () => false)

  // Computed property para verificar se o usuário está autenticado
  const isAuthenticated = computed(() => {
    if (!initialized.value) {
      initializeAuth()
    }

    return token.value !== null && token.value.length > 0
  })

  /**
   * Função para fazer login
   * @param newToken - Token JWT recebido da API
   */
  const login = (newToken: string) => {
    // Salvar no estado reativo
    token.value = newToken
    initialized.value = true

    // Salvar no localStorage para persistência
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, newToken)
    }
  }

  /**
   * Função para fazer logout
   * Remove o token do estado e do localStorage
   */
  const logout = () => {
    // Limpar estado reativo
    token.value = null
    initialized.value = true

    // Remover do localStorage
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY)
    }
  }

  /**
   * Função para obter o token para requisições HTTP
   * @returns Token formatado para header Authorization
   */
  const getAuthHeader = () => {
    if (!initialized.value) {
      initializeAuth()
    }

    if (token.value) {
      return `Bearer ${token.value}`
    }
    return null
  }

  /**
   * Função para verificar se o token está válido
   * (Implementação básica - pode ser expandida para verificar expiração)
   */
  const isTokenValid = () => {
    if (!initialized.value) {
      initializeAuth()
    }

    return isJwtValid(token.value)
  }

  /**
   * Inicialização do composable
   * Verifica se existe token no localStorage
   */
  function initializeAuth(): void {
    if (initialized.value) {
      return
    }

    initialized.value = true

    if (typeof window === 'undefined') {
      token.value = null
      return
    }

    const storedToken = window.localStorage.getItem(TOKEN_STORAGE_KEY)

    if (!storedToken) {
      token.value = null
      return
    }

    token.value = storedToken

    if (!isJwtValid(storedToken)) {
      logout()
    }
  }

  // Garantir inicialização imediata quando o composable for utilizado (inclui middlewares)
  initializeAuth()

  // Retornar estado reativo e funções
  return {
    // Estado
    token: readonly(token),
    isAuthenticated,

    // Funções
    login,
    logout,
    getAuthHeader,
    isTokenValid,
    initializeAuth
  }
}
