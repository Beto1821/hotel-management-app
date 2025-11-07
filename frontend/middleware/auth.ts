/**
 * Middleware de autenticação para Nuxt 3
 * Protege rotas que requerem autenticação
 */
export default defineNuxtRouteMiddleware((_to, _from) => {
  // Usar o composable de autenticação
  const { isAuthenticated, token, isTokenValid } = useAuth()

  // Verificar se o usuário está autenticado
  if (!isAuthenticated.value) {
    // Se não estiver autenticado, redirecionar para login
    return navigateTo('/login')
  }

  // Verificar se o token ainda é válido (não expirou)
  if (token.value && !isTokenValid()) {
    // Token expirado, fazer logout e redirecionar
    const { logout } = useAuth()
    logout()

    return navigateTo('/login')
  }

  // Se chegou até aqui, o usuário está autenticado
  return true
})
