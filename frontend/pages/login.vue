<template>
  <div class="min-h-screen relative overflow-hidden flex flex-col">
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0 z-0">
      <img src="/loginbackgrpound.png" alt="Hotel Background" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-br from-blue-900/80 via-purple-900/70 to-indigo-900/80 backdrop-blur-sm"></div>
    </div>

    <!-- Floating Elements - Images -->
    <div class="floating-element absolute top-20 left-10 w-24 h-24 opacity-25">
      <img src="/cartoon.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float drop-shadow-lg" />
    </div>
    <div class="floating-element absolute top-40 right-20 w-32 h-32 opacity-20">
      <img src="/rec2.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-delayed drop-shadow-xl" />
    </div>
    <div class="floating-element absolute bottom-32 left-20 w-36 h-36 opacity-15">
      <img src="/cartoon.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-slow drop-shadow-2xl" />
    </div>
    <div class="floating-element absolute bottom-20 right-32 w-28 h-28 opacity-25">
      <img src="/rec2.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float drop-shadow-lg" />
    </div>
    <div class="floating-element absolute top-1/3 left-1/4 w-20 h-20 opacity-20">
      <img src="/cartoon.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-delayed drop-shadow-md" />
    </div>
    <div class="floating-element absolute bottom-1/3 right-1/4 w-24 h-24 opacity-15">
      <img src="/rec2.png" alt="Hotel Icon" class="w-full h-full object-contain animate-float-slow drop-shadow-lg" />
    </div>

    <!-- Floating SVG Icons -->
    <div class="absolute top-32 right-1/4 w-16 h-16 text-white/20 animate-float-slow">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-lg">
        <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5zm0 2.18l8 4V17c0 4.52-3.15 8.72-8 10-4.85-1.28-8-5.48-8-10V8.18l8-4zM11 9v2h2V9h-2zm0 4v6h2v-6h-2z"/>
        <path d="M3 10v10c0 2.76 2.24 5 5 5h8c2.76 0 5-2.24 5-5V10H3zm7 10H8v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm0-4H6v-2h12v2z"/>
      </svg>
    </div>
    <div class="absolute bottom-40 left-1/3 w-20 h-20 text-purple-300/20 animate-float">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-xl">
        <path d="M19 9.3V4h-3v2.6L12 3L2 12h3v8h5v-6h4v6h5v-8h3l-3-2.7zM10 10c0-1.1.9-2 2-2s2 .9 2 2h-4z"/>
      </svg>
    </div>
    <div class="absolute top-1/2 left-12 w-14 h-14 text-blue-200/25 animate-float-delayed">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-md">
        <path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 0 7.59 6.59C7.22 6.95 7 7.45 7 8v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2c0-1.1-.9-2-2-2z"/>
      </svg>
    </div>
    <div class="absolute top-2/3 right-16 w-18 h-18 text-indigo-200/20 animate-float-slow">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-lg">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5.5-2.5l7.51-3.49L17.5 6.5 9.99 9.99 6.5 17.5zm5.5-6.6c.61 0 1.1.49 1.1 1.1s-.49 1.1-1.1 1.1-1.1-.49-1.1-1.1.49-1.1 1.1-1.1z"/>
      </svg>
    </div>
    <div class="absolute bottom-1/4 left-1/2 w-16 h-16 text-pink-200/15 animate-float">
      <svg fill="currentColor" viewBox="0 0 24 24" class="drop-shadow-md">
        <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
      </svg>
    </div>

    <!-- Animated Circles -->
    <div class="circle-animation absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-blue-400/10 animate-pulse-slow"></div>
    <div class="circle-animation absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-purple-400/10 animate-pulse-slower"></div>

    <!-- Login Card - Centralizado -->
    <div class="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 relative z-10">
        <div class="flex justify-end">
          <ThemeToggle />
        </div>

        <!-- Glass Card Effect -->
        <div class="bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20 dark:border-gray-700/50">
        <div>
          <div class="mx-auto h-36 w-36 flex items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg transform hover:scale-110 transition-transform duration-300 p-2">
            <img src="/Ring.png" alt="Plataforma Hotel Logo" class="w-full h-full object-contain" />
          </div>
          <h2 class="mt-6 text-center text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Bem-vindo de volta
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400 font-medium">
            Plataforma Hotel
          </p>
        </div>

      <!-- Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div v-if="errorMessage" class="rounded-xl bg-red-50 dark:bg-red-900/30 p-4 border border-red-200 dark:border-red-800 animate-shake">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
                Erro no login
              </h3>
              <div class="mt-2 text-sm text-red-700 dark:text-red-300">
                {{ errorMessage }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="successMessage" class="rounded-xl bg-green-50 dark:bg-green-900/30 p-4 border border-green-200 dark:border-green-800 animate-fade-in">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-green-800 dark:text-green-200">
                {{ successMessage }}
              </p>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <!-- Username field -->
          <div class="group">
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nome de usuário
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                id="username"
                v-model="username"
                name="username"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-800/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 sm:text-sm"
                placeholder="Digite seu usuário"
                :disabled="isLoading"
              >
            </div>
          </div>

          <!-- Password field -->
          <div class="group">
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Senha
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400 group-focus-within:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                id="password"
                v-model="password"
                name="password"
                type="password"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-800/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 sm:text-sm"
                placeholder="Digite sua senha"
                :disabled="isLoading"
              >
            </div>
          </div>
        </div>

        <!-- Options -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded cursor-pointer"
            >
            <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
              Lembrar de mim
            </label>
          </div>

          <div class="text-sm">
            <a href="#" class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 transition-colors">
              Esqueceu sua senha?
            </a>
          </div>
        </div>

        <!-- Submit button -->
        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-900 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200"
            :disabled="isLoading || !username || !password"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg
                v-if="!isLoading"
                class="h-5 w-5 text-blue-200 group-hover:text-white transition-colors"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
              <svg
                v-else
                class="animate-spin h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </span>
            {{ isLoading ? 'Entrando...' : 'Entrar' }}
          </button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Não tem uma conta?
            <NuxtLink to="/register" class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 transition-colors">
              Cadastre-se aqui
            </NuxtLink>
          </p>
        </div>
      </form>
      </div>
      </div>
    </div>
    
    <AppFooter />
  </div>
</template>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes float-delayed {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(-5deg);
  }
}

@keyframes float-slow {
  0%, 100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-15px) scale(1.05);
  }
}

@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

@keyframes pulse-slower {
  0%, 100% {
    opacity: 0.2;
    transform: scale(1);
  }
  50% {
    opacity: 0.4;
    transform: scale(1.05);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 7s ease-in-out infinite;
  animation-delay: 1s;
}

.animate-float-slow {
  animation: float-slow 8s ease-in-out infinite;
  animation-delay: 2s;
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

.animate-pulse-slower {
  animation: pulse-slower 6s ease-in-out infinite;
}

.animate-shake {
  animation: shake 0.5s;
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>

<script setup lang="ts">
// Imports e composables
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { loginRequest } from '~/services/apiClient'

// Meta da página
definePageMeta({
  layout: false, // Não usar layout padrão
  middleware: [] // Não aplicar middleware de auth nesta página
})

// Estado reativo
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Composables
const { login } = useAuth()
const route = useRoute()
const router = useRouter()

// Função para preencher credenciais de demonstração
const fillDemoCredentials = () => {
  username.value = 'testuser'
  password.value = '123456'
}

// Função principal de login
const handleLogin = async () => {
  // Limpar mensagens anteriores
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  const { $toast, $alert } = useNuxtApp()

  try {
    // Chamar a API de login
    const response = await loginRequest(username.value, password.value)

    // Salvar o token usando o composable
    login(response.access_token)

    // Mostrar notificação de sucesso
    $toast.fire({
      icon: 'success',
      title: 'Login realizado com sucesso!'
    })

    // Redirecionar para o dashboard
    await router.push('/')
  } catch (error: any) {
    // Tratar erro de credenciais inválidas
    if (error.status === 401) {
      errorMessage.value = 'Nome de usuário ou senha incorretos.'
      await $alert.error('Erro de Autenticação', 'Nome de usuário ou senha incorretos.')
    } else {
      errorMessage.value = error.data?.detail || 'Ocorreu um erro inesperado. Tente novamente.'
      await $alert.error('Erro', error.data?.detail || 'Ocorreu um erro inesperado. Tente novamente.')
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (route.query.registered === 'true') {
    successMessage.value = 'Registro concluído com sucesso! Faça o login para continuar.'
    // Limpar o parâmetro da URL
    router.replace({ query: {} })
  }
})

// SEO e meta tags
useHead({
  title: 'Login - Hotel Management',
  meta: [
    { name: 'description', content: 'Faça login no sistema de gerenciamento de hotel' }
  ]
})
</script>

<style scoped>
/* Estilos adicionais se necessário */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
