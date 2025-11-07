import { ref, computed, onMounted, readonly } from 'vue'

/**
 * Composable para gerenciamento de autenticação
 * Controla o estado do token JWT e funções de login/logout
 */
export const useAuth = () => {
  // Estado reativo do token
  const token = ref<string | null>(null)

  // Computed property para verificar se o usuário está autenticado
  const isAuthenticated = computed(() => {
    return token.value !== null && token.value.length > 0
  })

  /**
   * Função para fazer login
   * @param newToken - Token JWT recebido da API
   */
  const login = (newToken: string) => {
    // Salvar no estado reativo
    token.value = newToken

    // Salvar no localStorage para persistência
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', newToken)
    }
  }

  /**
   * Função para fazer logout
   * Remove o token do estado e do localStorage
   */
  const logout = () => {
    // Limpar estado reativo
    token.value = null

    // Remover do localStorage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
    }
  }

  /**
   * Função para obter o token para requisições HTTP
   * @returns Token formatado para header Authorization
   */
  const getAuthHeader = () => {
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
    if (!token.value) { return false }

    try {
      // Decodificar payload do JWT (sem verificação de assinatura)
      const payload = JSON.parse(atob(token.value.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)

      // Verificar se o token não expirou
      return payload.exp > currentTime
    } catch (error) {
      return false
    }
  }

  /**
   * Inicialização do composable
   * Verifica se existe token no localStorage
   */
  const initializeAuth = () => {
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('auth_token')

      if (storedToken) {
        // Verificar se o token ainda é válido
        token.value = storedToken

        if (!isTokenValid()) {
          // Token expirado, fazer logout
          logout()
        }
      }
    }
  }

  // Inicializar quando o composable for montado
  onMounted(() => {
    initializeAuth()
  })

  // Se não estiver em um contexto de componente, inicializar imediatamente
  if (typeof window !== 'undefined' && !token.value) {
    initializeAuth()
  }

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
