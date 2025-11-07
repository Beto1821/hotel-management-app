<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
      <h2 class="text-2xl font-bold text-center text-gray-900">Criar Conta</h2>
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Nome</label>
          <input
            id="name"
            v-model="name"
            type="text"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div v-if="error" class="text-sm text-red-600">
          {{ error }}
        </div>
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full px-4 py-2 font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            <span v-if="loading">Registrando...</span>
            <span v-else>Registrar</span>
          </button>
        </div>
      </form>
      <p class="text-sm text-center text-gray-600">
        Já tem uma conta?
        <NuxtLink to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
          Faça login
        </NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';

// Define o layout da página como 'auth'
definePageMeta({
  layout: 'auth',
  auth: false // Não requer autenticação para acessar
});

const { register } = useAuth();
const router = useRouter();

const name = ref('');
const email = ref('');
const password = ref('');
const error = ref<string | null>(null);
const loading = ref(false);

const handleRegister = async () => {
  loading.value = true;
  error.value = null;
  try {
    await register(name.value, email.value, password.value);
    // Redireciona para a página de login após o registro bem-sucedido
    router.push('/login');
  } catch (err: any) {
    error.value = err.data?.detail || 'Ocorreu um erro ao tentar registrar.';
    console.error('Registration failed:', err);
  } finally {
    loading.value = false;
  }
};
</script>
