<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <NuxtLink to="/" class="flex items-center">
              <div class="h-8 w-8 bg-green-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="ml-4">
                <h1 class="text-xl font-semibold text-gray-900">
                  Gestão de Reservas
                </h1>
              </div>
            </NuxtLink>
          </div>

          <div class="flex items-center space-x-4">
            <NuxtLink to="/" class="text-sm text-green-600 hover:text-green-800">
              ← Voltar ao Dashboard
            </NuxtLink>
            <button
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              @click="handleLogout"
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

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              Reservas
            </h1>
            <p class="mt-2 text-sm text-gray-600">
              Cadastre e acompanhe as hospedagens ativas, pendentes e concluídas
            </p>
          </div>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div class="flex gap-2">
              <div>
                <label class="sr-only" for="status-filter">Status</label>
                <select id="status-filter" v-model="statusFilter" class="input-field">
                  <option value="todos">Todos os status</option>
                  <option v-for="status in statusOptions" :key="status" :value="status">
                    {{ statusLabels[status] || status }}
                  </option>
                </select>
              </div>
              <div>
                <label class="sr-only" for="month-filter">Mês</label>
                <input id="month-filter" v-model="monthFilter" type="month" class="input-field">
              </div>
            </div>
            <button
              class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              @click="openCreateForm"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Nova Reserva
            </button>
          </div>
        </div>
      </div>

      <div v-if="showForm" class="px-4 py-6 sm:px-0">
        <div class="bg-white shadow rounded-lg p-6 mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-medium text-gray-900">
              {{ editingReservation ? 'Atualizar Reserva' : 'Cadastrar Reserva' }}
            </h2>
            <button class="text-gray-400 hover:text-gray-600" @click="cancelForm">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form class="grid grid-cols-1 gap-6 sm:grid-cols-2" @submit.prevent="submitForm">
            <div>
              <label class="block text-sm font-medium text-gray-700" for="client">
                Cliente
              </label>
              <select
                id="client"
                v-model.number="form.client_id"
                class="mt-1 input-field"
                :disabled="Boolean(editingReservation)"
                required
              >
                <option value="">Selecione um cliente</option>
                <option v-for="client in clients" :key="client.id" :value="client.id">
                  {{ client.name }} · {{ client.document }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700" for="room">
                Quarto
              </label>
              <select
                id="room"
                v-model.number="form.quarto_id"
                class="mt-1 input-field"
                :disabled="Boolean(editingReservation)"
                required
              >
                <option value="">Selecione um quarto</option>
                <option v-for="room in rooms" :key="room.id" :value="room.id">
                  {{ room.numero }} · {{ room.tipo }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700" for="checkin">
                Check-in
              </label>
              <input
                id="checkin"
                v-model="form.data_checkin"
                type="date"
                class="mt-1 input-field"
                required
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700" for="checkout">
                Check-out
              </label>
              <input
                id="checkout"
                v-model="form.data_checkout"
                type="date"
                class="mt-1 input-field"
                required
              >
            </div>

            <div v-if="editingReservation" class="sm:col-span-2">
              <label class="block text-sm font-medium text-gray-700" for="status">
                Status
              </label>
              <select id="status" v-model="form.status" class="mt-1 input-field">
                <option v-for="status in statusOptions" :key="status" :value="status">
                  {{ statusLabels[status] || status }}
                </option>
              </select>
            </div>

            <div class="sm:col-span-2 flex justify-end space-x-3">
              <button
                type="button"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                @click="cancelForm"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                {{ loading ? 'Salvando...' : (editingReservation ? 'Atualizar' : 'Salvar') }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="px-4 py-6 sm:px-0">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div v-if="loadingReservations" class="p-8 text-center">
            <div class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Carregando reservas...
            </div>
          </div>

          <div v-else-if="filteredReservations.length === 0" class="p-8 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">
              {{ statusFilter !== 'todos' || monthFilter ? 'Nenhuma reserva encontrada' : 'Nenhuma reserva cadastrada' }}
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              {{ statusFilter !== 'todos' || monthFilter ? 'Ajuste os filtros e tente novamente.' : 'Comece registrando a primeira reserva.' }}
            </p>
            <div class="mt-6">
              <button
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                @click="openCreateForm"
              >
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Nova Reserva
              </button>
            </div>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Reserva
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cliente
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quarto
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Período
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Valor
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Ações</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="reserva in filteredReservations" :key="reserva.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    #{{ reserva.id }}
                    <span class="block text-xs text-gray-400">{{ formatDateTime(reserva.created_at) }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ reserva.client?.name || 'Cliente #' + reserva.client_id }}
                    <span v-if="reserva.client?.email" class="block text-xs text-gray-500">
                      {{ reserva.client.email }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ reserva.quarto?.numero || 'Quarto ' + reserva.quarto_id }}
                    <span v-if="reserva.quarto?.tipo" class="block text-xs text-gray-500">
                      {{ reserva.quarto.tipo }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDate(reserva.data_check_in) }} - {{ formatDate(reserva.data_check_out) }}
                    <span class="block text-xs text-gray-500">
                      {{ quantidadeNoites(reserva.data_check_in, reserva.data_check_out) }} noites
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex px-2 py-1 text-xs font-semibold leading-5 rounded-full"
                      :class="statusBadgeClass(reserva.status)"
                    >
                      {{ statusLabels[reserva.status] || reserva.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatCurrency(reserva.valor_total) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <button
                        class="text-green-600 hover:text-green-900"
                        title="Editar reserva"
                        @click="editReservation(reserva)"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        class="text-red-600 hover:text-red-900"
                        title="Cancelar reserva"
                        @click="removeReservation(reserva.id)"
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
              <svg v-if="message.type === 'success'" class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
              <svg v-else class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
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
                  class="inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2"
                  :class="{
                    'text-green-500 hover:bg-green-100 focus:ring-green-600': message.type === 'success',
                    'text-red-500 hover:bg-red-100 focus:ring-red-600': message.type === 'error'
                  }"
                  @click="message = null"
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
import { computed, onMounted, ref } from 'vue'
import { useAuth } from '~/composables/useAuth'
import {
  createReservation,
  deleteReservation,
  getReservations,
  updateReservation,
  type Reservation,
  type ReservationCreate,
  type ReservationUpdate,
  getClients,
  getRooms,
  type Client,
  type Room
} from '~/services/apiClient'

definePageMeta({
  middleware: ['auth'],
  alias: ['/bookings']
})

const { logout } = useAuth()

const reservations = ref<Reservation[]>([])
const clients = ref<Client[]>([])
const rooms = ref<Room[]>([])
const loadingReservations = ref(true)
const loading = ref(false)
const showForm = ref(false)
const editingReservation = ref<Reservation | null>(null)

const statusOptions = ['pendente', 'ativa', 'concluida', 'cancelada']
const statusLabels: Record<string, string> = {
  pendente: 'Pendente',
  ativa: 'Ativa',
  concluida: 'Concluída',
  cancelada: 'Cancelada'
}

const statusFilter = ref<'todos' | string>('todos')
const monthFilter = ref('')

const form = ref<{
  client_id: number | ''
  quarto_id: number | ''
  data_checkin: string
  data_checkout: string
  status: string
}>({
  client_id: '',
  quarto_id: '',
  data_checkin: '',
  data_checkout: '',
  status: 'pendente'
})

const message = ref<{ type: 'success' | 'error'; text: string } | null>(null)

const filteredReservations = computed(() => {
  return reservations.value.filter((reserva) => {
    const matchesStatus =
      statusFilter.value === 'todos' || reserva.status === statusFilter.value

    const matchesMonth = monthFilter.value
      ? reserva.data_check_in.slice(0, 7) === monthFilter.value
      : true

    return matchesStatus && matchesMonth
  })
})

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

function formatDateTime(value: string): string {
  return new Date(value).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatCurrency(value: number): string {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function quantidadeNoites(checkin: string, checkout: string): number {
  const start = new Date(checkin)
  const end = new Date(checkout)
  return Math.max(1, Math.round((end.getTime() - start.getTime()) / 86_400_000))
}

function statusBadgeClass(status: string): string {
  const map: Record<string, string> = {
    pendente: 'bg-yellow-100 text-yellow-800',
    ativa: 'bg-blue-100 text-blue-800',
    concluida: 'bg-green-100 text-green-800',
    cancelada: 'bg-red-100 text-red-800'
  }
  return map[status] || 'bg-gray-100 text-gray-800'
}

function showMessage(type: 'success' | 'error', text: string) {
  message.value = { type, text }
  setTimeout(() => {
    if (message.value?.text === text) {
      message.value = null
    }
  }, 5000)
}

async function loadReservations() {
  try {
    loadingReservations.value = true
    reservations.value = await getReservations()
  } catch (error) {
    showMessage('error', 'Erro ao carregar reservas.')
    reservations.value = []
  } finally {
    loadingReservations.value = false
  }
}

async function loadAuxiliaryData() {
  try {
    const [clientList, roomList] = await Promise.all([
      getClients(0, 200),
      getRooms(0, 200)
    ])
    clients.value = clientList
    rooms.value = roomList
  } catch (error) {
    showMessage('error', 'Não foi possível carregar dados auxiliares.')
  }
}

async function submitForm() {
  if (!form.value.client_id || !form.value.quarto_id) {
    showMessage('error', 'Selecione cliente e quarto.')
    return
  }

  if (!form.value.data_checkin || !form.value.data_checkout) {
    showMessage('error', 'Informe as datas de check-in e check-out.')
    return
  }

  if (form.value.data_checkin >= form.value.data_checkout) {
    showMessage('error', 'O check-out deve ser posterior ao check-in.')
    return
  }

  try {
    loading.value = true
    if (editingReservation.value) {
      const payload: ReservationUpdate = {}

      if (form.value.data_checkin !== editingReservation.value.data_check_in) {
        payload.data_checkin = form.value.data_checkin
      }
      if (form.value.data_checkout !== editingReservation.value.data_check_out) {
        payload.data_checkout = form.value.data_checkout
      }
      if (form.value.status !== editingReservation.value.status) {
        payload.status = form.value.status
      }

      await updateReservation(editingReservation.value.id, payload)
      showMessage('success', 'Reserva atualizada com sucesso!')
    } else {
      const payload: ReservationCreate = {
        client_id: Number(form.value.client_id),
        quarto_id: Number(form.value.quarto_id),
        data_checkin: form.value.data_checkin,
        data_checkout: form.value.data_checkout
      }
      await createReservation(payload)
      showMessage('success', 'Reserva criada com sucesso!')
    }

    await loadReservations()
    cancelForm()
  } catch (error: any) {
    const detail = error?.data?.detail || 'Erro ao salvar reserva.'
    showMessage('error', detail)
  } finally {
    loading.value = false
  }
}

function editReservation(reserva: Reservation) {
  editingReservation.value = reserva
  form.value = {
  client_id: reserva.client_id,
    quarto_id: reserva.quarto_id,
    data_checkin: reserva.data_check_in,
    data_checkout: reserva.data_check_out,
    status: reserva.status
  }
  showForm.value = true
}

async function removeReservation(id: number) {
  if (!confirm('Deseja cancelar esta reserva?')) {
    return
  }

  try {
    loading.value = true
    await deleteReservation(id)
    showMessage('success', 'Reserva cancelada com sucesso!')
    await loadReservations()
  } catch (error: any) {
    const detail = error?.data?.detail || 'Falha ao cancelar reserva.'
    showMessage('error', detail)
  } finally {
    loading.value = false
  }
}

function cancelForm() {
  showForm.value = false
  editingReservation.value = null
  form.value = {
    client_id: '',
    quarto_id: '',
    data_checkin: '',
    data_checkout: '',
    status: 'pendente'
  }
}

function handleLogout() {
  logout()
  navigateTo('/login')
}

async function openCreateForm() {
  if (clients.value.length === 0 || rooms.value.length === 0) {
    await loadAuxiliaryData()
  }
  showForm.value = true
}

onMounted(async () => {
  await Promise.all([loadReservations(), loadAuxiliaryData()])
})

useHead({
  title: 'Reservas - Hotel Management',
  meta: [
    { name: 'description', content: 'Gestão de reservas do hotel' }
  ]
})
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>
