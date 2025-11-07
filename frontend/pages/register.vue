<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center">
    <div class="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-white mb-2">Criar Conta</h2>
        <p class="text-gray-400">Hotel Management System</p>
      </div>

      <!-- Error Message -->
      <div 
        v-if="error" 
        class="bg-red-900/50 border border-red-500 text-red-100 px-4 py-3 rounded mb-4"
      >
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          Erro no cadastro
        </div>
        <p class="mt-1 text-sm">{{ error }}</p>
      </div>

      <!-- Success Message -->
      <div 
        v-if="success" 
        class="bg-green-900/50 border border-green-500 text-green-100 px-4 py-3 rounded mb-4"
      >
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          Conta criada com sucesso!
        </div>
        <p class="mt-1 text-sm">{{ success }}</p>
      </div>

      <!-- Register Form -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block text-gray-300 text-sm font-medium mb-2">
            Usuário
          </label>
          <input
            v-model="form.username"
            type="text"
            required
            class="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Digite seu usuário"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-gray-300 text-sm font-medium mb-2">
            Senha
          </label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Digite sua senha"
          />
        </div>

        <!-- Confirm Password -->
        <div>
          <label class="block text-gray-300 text-sm font-medium mb-2">
            Confirmar Senha
          </label>
          <input
            v-model="form.confirmPassword"
            type="password"
            required
            class="w-full px-3 py-3 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Confirme sua senha"
          />
        </div>

        <!-- Register Button -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-md transition-colors duration-200 flex items-center justify-center"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? 'Criando...' : 'Criar Conta' }}
        </button>
      </form>

      <!-- Login Link -->
      <div class="mt-6 text-center">
        <p class="text-gray-400">
          Já tem uma conta?
          <NuxtLink 
            to="/login" 
            class="text-blue-400 hover:text-blue-300 font-medium transition-colors duration-200"
          >
            Faça login
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Meta da página
definePageMeta({
  layout: false,
  middleware: []
})

// State
const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

// Função de registro
async function handleRegister() {
  // Limpar mensagens
  error.value = ''
  success.value = ''

  // Validações
  if (!form.value.username.trim()) {
    error.value = 'Por favor, digite um usuário'
    return
  }

  if (!form.value.password.trim()) {
    error.value = 'Por favor, digite uma senha'
    return
  }

  if (form.value.password.length < 6) {
    error.value = 'A senha deve ter pelo menos 6 caracteres'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'As senhas não coincidem'
    return
  }

  loading.value = true

  try {
    // Fazer requisição de registro
    const response = await $fetch('/api/v1/auth/register', {
      method: 'POST',
      body: {
        username: form.value.username,
        password: form.value.password
      }
    })

    success.value = 'Conta criada com sucesso! Redirecionando...'
    
    // Redirecionar para login após 2 segundos
    setTimeout(() => {
      navigateTo('/login')
    }, 2000)

  } catch (err: any) {
    console.error('Erro ao criar conta:', err)
    
    if (err.statusCode === 400) {
      error.value = 'Este usuário já existe. Tente outro nome.'
    } else if (err.statusCode === 422) {
      error.value = 'Dados inválidos. Verifique os campos.'
    } else {
      error.value = 'Erro no servidor. Tente novamente mais tarde.'
    }
  } finally {
    loading.value = false
  }
}
</script>