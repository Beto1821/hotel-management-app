<template>
  <div class="min-h-screen relative overflow-hidden flex flex-col">
    <!-- Background Image with Overlay -->
    <div class="absolute inset-0 z-0">
      <img src="/loginbackgrpound.png" alt="Hotel Background" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-br from-purple-900/80 via-indigo-900/70 to-blue-900/80 backdrop-blur-sm"></div>
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

    <!-- Animated Circles -->
    <div class="circle-animation absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-purple-400/10 animate-pulse-slow"></div>
    <div class="circle-animation absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-indigo-400/10 animate-pulse-slower"></div>

    <!-- Register Card - Centralizado -->
    <div class="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 relative z-10">
        <div class="flex justify-end">
          <ThemeToggle />
        </div>

        <!-- Glass Card Effect -->
        <div class="bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20 dark:border-gray-700/50">
        <!-- Header -->
        <div>
          <div class="mx-auto h-28 w-28 flex items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 shadow-lg transform hover:scale-110 transition-transform duration-300 p-5">
            <img src="/log_plataformahote.png" alt="Plataforma Hotel Logo" class="w-full h-full object-contain" />
          </div>
          <h2 class="mt-6 text-center text-4xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
            Criar nova conta
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400 font-medium">
            Junte-se à Plataforma Hotel
          </p>
        </div>

        <!-- Form -->
        <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
          <!-- Alert de erro -->
          <div v-if="error" class="rounded-xl bg-red-50 dark:bg-red-900/30 p-4 border border-red-200 dark:border-red-800 animate-shake">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
                  Erro no registro
                </h3>
                <div class="mt-2 text-sm text-red-700 dark:text-red-300">
                  {{ error }}
                </div>
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
                  <svg class="h-5 w-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input
                  id="username"
                  v-model="username"
                  name="username"
                  type="text"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-800/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 sm:text-sm"
                  placeholder="Digite seu usuário"
                  :disabled="loading"
                >
              </div>
            </div>

            <!-- Email field -->
            <div class="group">
              <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <input
                  id="email"
                  v-model="email"
                  name="email"
                  type="email"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-800/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 sm:text-sm"
                  placeholder="seu@email.com"
                  :disabled="loading"
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
                  <svg class="h-5 w-5 text-gray-400 group-focus-within:text-purple-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  id="password"
                  v-model="password"
                  name="password"
                  type="password"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-800/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 sm:text-sm"
                  placeholder="Digite sua senha"
                  :disabled="loading"
                >
              </div>
            </div>
          </div>

          <!-- Submit button -->
          <div>
            <button
              type="submit"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-900 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200"
              :disabled="loading || !username || !email || !password"
            >
              <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                <svg
                  v-if="!loading"
                  class="h-5 w-5 text-purple-200 group-hover:text-white transition-colors"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
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
              {{ loading ? 'Registrando...' : 'Criar Conta' }}
            </button>
          </div>

          <!-- Login link -->
          <div class="text-center">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Já tem uma conta?
              <NuxtLink to="/login" class="font-medium text-purple-600 dark:text-purple-400 hover:text-purple-500 dark:hover:text-purple-300 transition-colors">
                Faça login aqui
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

<script setup lang="ts">
import { ref } from 'vue'
import { registerRequest } from '~/services/apiClient'

// Meta da página
definePageMeta({
  layout: false,
  middleware: []
})

// Estado reativo
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

// Router
const router = useRouter()

// Função principal de registro
const handleRegister = async () => {
  loading.value = true
  error.value = null
  try {
    await registerRequest(username.value, email.value, password.value)
    router.push('/login?registered=true')
  } catch (err: any) {
    error.value = err.data?.detail || 'Ocorreu um erro ao tentar registrar.'
  } finally {
    loading.value = false
  }
}
</script>

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
</style>
