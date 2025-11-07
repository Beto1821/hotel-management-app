<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and Title -->
          <div class="flex items-center">
            <NuxtLink to="/" class="flex items-center">
              <div class="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                </svg>
              </div>
              <div class="ml-4">
                <h1 class="text-xl font-semibold text-gray-900">Hotel Management</h1>
              </div>
            </NuxtLink>
          </div>

          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <NuxtLink to="/" class="text-sm text-blue-600 hover:text-blue-800">
              ← Voltar ao Dashboard
            </NuxtLink>
            <button
              @click="handleLogout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sair
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Clientes</h1>
            <p class="mt-2 text-sm text-gray-600">
              Gerencie os clientes do hotel
            </p>
          </div>
          <button
            @click="showAddForm = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Adicionar Cliente
          </button>
        </div>
      </div>

      <!-- Add Client Form -->
      <div v-if="showAddForm" class="px-4 py-6 sm:px-0">
        <div class="bg-white shadow rounded-lg p-6 mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-medium text-gray-900">
              {{ editingClient ? 'Editar Cliente' : 'Novo Cliente' }}
            </h2>
            <button
              @click="cancelForm"
              class="text-gray-400 hover:text-gray-600"
            >
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="submitForm" class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">Nome Completo</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="mt-1 input-field"
                placeholder="Digite o nome completo"
              />
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="mt-1 input-field"
                placeholder="cliente@exemplo.com"
              />
            </div>

            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700">Telefone</label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                required
                class="mt-1 input-field"
                placeholder="(11) 99999-9999"
              />
            </div>

            <div>
              <label for="document" class="block text-sm font-medium text-gray-700">Documento (CPF/RG)</label>
              <input
                id="document"
                v-model="form.document"
                type="text"
                required
                class="mt-1 input-field"
                placeholder="000.000.000-00"
              />
            </div>

            <div class="sm:col-span-2">
              <label for="address" class="block text-sm font-medium text-gray-700">Endereço</label>
              <textarea
                id="address"
                v-model="form.address"
                rows="3"
                class="mt-1 input-field"
                placeholder="Endereço completo (opcional)"
              ></textarea>
            </div>

            <div class="sm:col-span-2">
              <div class="flex justify-end space-x-3">
                <button
                  type="button"
                  @click="cancelForm"
                  class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="loading"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ loading ? 'Salvando...' : (editingClient ? 'Atualizar' : 'Salvar') }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <!-- Clients Table -->
      <div class="px-4 py-6 sm:px-0">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <!-- Loading State -->
          <div v-if="loadingClients" class="p-8 text-center">
            <div class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Carregando clientes...
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="clients.length === 0" class="p-8 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhum cliente cadastrado</h3>
            <p class="mt-1 text-sm text-gray-500">Comece adicionando o primeiro cliente do hotel.</p>
            <div class="mt-6">
              <button
                @click="showAddForm = true"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Adicionar Cliente
              </button>
            </div>
          </div>

          <!-- Table -->
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cliente
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contato
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Documento
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data de Cadastro
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Ações</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="client in clients" :key="client.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div class="text-sm font-medium text-gray-900">
                        {{ client.name }}
                      </div>
                      <div class="text-sm text-gray-500" v-if="client.address">
                        {{ client.address }}
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ client.email }}</div>
                    <div class="text-sm text-gray-500">{{ client.phone }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ client.document }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(client.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <button
                        @click="editClient(client)"
                        class="text-blue-600 hover:text-blue-900"
                        title="Editar cliente"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        @click="removeClient(client.id)"
                        class="text-red-600 hover:text-red-900"
                        title="Excluir cliente"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Success/Error Messages -->
      <div v-if="message" class="fixed bottom-4 right-4 max-w-sm">
        <div
          class="rounded-md p-4"
          :class="{
            'bg-green-50 border border-green-200': message.type === 'success',
            'bg-red-50 border border-red-200': message.type === 'error'
          }"
        >
          <div class="flex">
            <div class="flex-shrink-0">
              <svg
                v-if="message.type === 'success'"
                class="h-5 w-5 text-green-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
              <svg
                v-else
                class="h-5 w-5 text-red-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <p
                class="text-sm font-medium"
                :class="{
                  'text-green-800': message.type === 'success',
                  'text-red-800': message.type === 'error'
                }"
              >
                {{ message.text }}
              </p>
            </div>
            <div class="ml-auto pl-3">
              <div class="-mx-1.5 -my-1.5">
                <button
                  @click="message = null"
                  class="inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2"
                  :class="{
                    'text-green-500 hover:bg-green-100 focus:ring-green-600': message.type === 'success',
                    'text-red-500 hover:bg-red-100 focus:ring-red-600': message.type === 'error'
                  }"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { 
  getClients, 
  createClient, 
  updateClient, 
  deleteClient,
  type Client,
  type ClientCreate,
  type ClientUpdate
} from '~/services/apiClient'

// Meta da página - protegida por middleware de auth
definePageMeta({
  middleware: ['auth']
})

// Interface local para o formulário
interface ClientForm {
  name: string
  email: string
  phone: string
  document: string
  address: string
}

// Composables
const { logout } = useAuth()

// Estados reativos
const clients = ref<Client[]>([])
const loadingClients = ref(true)
const loading = ref(false)
const showAddForm = ref(false)
const editingClient = ref<Client | null>(null)

// Formulário
const form = ref<ClientForm>({
  name: '',
  email: '',
  phone: '',
  document: '',
  address: ''
})

// Mensagens
const message = ref<{ type: 'success' | 'error', text: string } | null>(null)

// Função para formatar data
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

// Função para mostrar mensagem temporária
const showMessage = (type: 'success' | 'error', text: string) => {
  message.value = { type, text }
  setTimeout(() => {
    message.value = null
  }, 5000)
}

// Carregar lista de clientes
const loadClients = async () => {
  try {
    loadingClients.value = true
    
    // Implementação real com API
    const response = await getClients(0, 100)
    clients.value = response
    
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
    showMessage('error', 'Erro ao carregar lista de clientes')
    clients.value = []
  } finally {
    loadingClients.value = false
  }
}

// Submeter formulário (criar ou atualizar)
const submitForm = async () => {
  try {
    loading.value = true
    
    // Validação básica
    if (!form.value.name || !form.value.email || !form.value.phone || !form.value.document) {
      showMessage('error', 'Preencha todos os campos obrigatórios')
      return
    }
    
    const clientData = {
      name: form.value.name,
      email: form.value.email,
      phone: form.value.phone,
      document: form.value.document,
      address: form.value.address || undefined
    }
    
    if (editingClient.value) {
      // Atualizar cliente existente
      await updateClient(editingClient.value.id, clientData)
      showMessage('success', 'Cliente atualizado com sucesso!')
    } else {
      // Criar novo cliente
      await createClient(clientData)
      showMessage('success', 'Cliente adicionado com sucesso!')
    }
    
    // Recarregar lista
    await loadClients()
    cancelForm()
    
  } catch (error) {
    console.error('Erro ao salvar cliente:', error)
    showMessage('error', 'Erro ao salvar cliente. Verifique os dados e tente novamente.')
  } finally {
    loading.value = false
  }
}

// Editar cliente
const editClient = (client: Client) => {
  editingClient.value = client
  form.value = {
    name: client.name,
    email: client.email,
    phone: client.phone,
    document: client.document,
    address: client.address || ''
  }
  showAddForm.value = true
}

// Função para remover cliente
const removeClient = async (id: number) => {
  if (!confirm('Tem certeza que deseja excluir este cliente?')) {
    return
  }

  loading.value = true
  try {
    await deleteClient(id)
    await loadClients() // Recarregar a lista
    showMessage('success', 'Cliente excluído com sucesso!')
  } catch (error: any) {
    console.error('Erro ao excluir cliente:', error)
    showMessage(error.data?.detail || 'Falha ao excluir cliente.', 'error')
  } finally {
    loading.value = false
  }
}

// Cancelar formulário
const cancelForm = () => {
  showAddForm.value = false
  editingClient.value = null
  form.value = {
    name: '',
    email: '',
    phone: '',
    document: '',
    address: ''
  }
}

// Função de logout
const handleLogout = async () => {
  logout()
  await navigateTo('/login')
}

// Carregar clientes ao montar o componente
onMounted(() => {
  loadClients()
})

// SEO e meta tags
useHead({
  title: 'Clientes - Hotel Management',
  meta: [
    { name: 'description', content: 'Gerenciamento de clientes do hotel' }
  ]
})
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>