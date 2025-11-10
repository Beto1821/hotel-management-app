<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <NuxtLink to="/" class="flex items-center">
              <div class="h-8 w-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                </svg>
              </div>
              <div class="ml-4">
                <h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
                  Gestão de Quartos
                </h1>
              </div>
            </NuxtLink>
          </div>

          <div class="flex items-center space-x-4">
            <NuxtLink to="/" class="text-sm text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300">
              ← Voltar ao Dashboard
            </NuxtLink>
            <ThemeToggle />
            <button
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-700 dark:text-gray-700 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-900 focus:ring-purple-500"
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
            <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
              Quartos
            </h1>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Controle o inventário de quartos e acompanhe a ocupação
            </p>
          </div>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div class="relative">
              <label class="sr-only" for="search-rooms">Buscar quartos</label>
              <input
                id="search-rooms"
                v-model="searchTerm"
                type="search"
                class="input-field pl-10 pr-9 w-full sm:w-64"
                placeholder="Buscar por número ou tipo"
              >
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z" />
              </svg>
              <button
                v-if="searchTerm"
                type="button"
                class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:text-gray-400"
                aria-label="Limpar busca"
                @click="searchTerm = ''"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div>
              <label class="sr-only" for="status-filter">Status</label>
              <select
                id="status-filter"
                v-model="statusFilter"
                class="input-field"
              >
                <option value="todos">Todos os status</option>
                <option v-for="option in statusOptions" :key="option" :value="option">
                  {{ statusLabels[option] || option }}
                </option>
              </select>
            </div>

            <button
              class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              @click="showForm = true"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Adicionar Quarto
            </button>
          </div>
        </div>
      </div>

      <div v-if="showForm" class="px-4 py-6 sm:px-0">
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
              {{ editingRoom ? 'Editar Quarto' : 'Novo Quarto' }}
            </h2>
            <button class="text-gray-400 hover:text-gray-600 dark:text-gray-400" @click="cancelForm">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form class="grid grid-cols-1 gap-6 sm:grid-cols-2" @submit.prevent="submitForm">
            <div>
              <label for="numero" class="block text-sm font-medium text-gray-700">Número</label>
              <input
                id="numero"
                v-model="form.numero"
                type="text"
                required
                class="mt-1 input-field"
                placeholder="Ex: 101"
              >
            </div>

            <div>
              <label for="tipo" class="block text-sm font-medium text-gray-700">Tipo</label>
              <input
                id="tipo"
                v-model="form.tipo"
                type="text"
                required
                class="mt-1 input-field"
                placeholder="Standard, Luxo, etc."
              >
            </div>

            <div>
              <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
              <select
                id="status"
                v-model="form.status"
                class="mt-1 input-field"
                required
              >
                <option v-for="option in statusOptions" :key="option" :value="option">
                  {{ statusLabels[option] || option }}
                </option>
              </select>
            </div>

            <div>
              <label for="capacidade" class="block text-sm font-medium text-gray-700">Capacidade</label>
              <input
                id="capacidade"
                v-model.number="form.capacidade"
                type="number"
                min="1"
                class="mt-1 input-field"
                required
              >
            </div>

            <div>
              <label for="valor_diaria" class="block text-sm font-medium text-gray-700">Diária (R$)</label>
              <input
                id="valor_diaria"
                v-model="form.valor_diaria"
                v-money3="moneyConfig"
                class="mt-1 input-field"
                required
              >
            </div>

            <div class="sm:col-span-2">
              <label for="descricao" class="block text-sm font-medium text-gray-700">Descrição</label>
              <textarea
                id="descricao"
                v-model="form.descricao"
                rows="3"
                class="mt-1 input-field"
                placeholder="Detalhes adicionais do quarto (opcional)"
              />
            </div>

            <div class="sm:col-span-2 flex justify-end space-x-3">
              <button
                type="button"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                @click="cancelForm"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                {{ loading ? 'Salvando...' : (editingRoom ? 'Atualizar' : 'Salvar') }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="px-4 py-6 sm:px-0">
        <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
          <div v-if="loadingRooms" class="p-8 text-center">
            <div class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Carregando quartos...
            </div>
          </div>

          <div v-else-if="filteredRooms.length === 0" class="p-8 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m12-6l-4-4-4 4" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">
              {{ searchTerm || statusFilter !== 'todos' ? 'Nenhum quarto encontrado' : 'Nenhum quarto cadastrado' }}
            </h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {{ searchTerm || statusFilter !== 'todos' ? 'Ajuste os filtros para visualizar outros quartos.' : 'Adicione o primeiro quarto para começar.' }}
            </p>
            <div class="mt-6">
              <button
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                @click="showForm = true"
              >
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Adicionar Quarto
              </button>
            </div>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50 dark:bg-gray-900">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Número
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Capacidade
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Diária
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Ações</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200">
                <tr v-for="room in filteredRooms" :key="room.id" class="hover:bg-gray-50 dark:bg-gray-900">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                    {{ room.numero }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                    {{ room.tipo }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex px-2 py-1 text-xs font-semibold leading-5 rounded-full"
                      :class="statusBadgeClass(room.status)"
                    >
                      {{ statusLabels[room.status] || room.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                    {{ room.capacidade }} hóspedes
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                    {{ formatCurrency(room.valor_diaria) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <button
                        class="text-purple-600 hover:text-purple-900"
                        title="Editar quarto"
                        @click="editRoom(room)"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        class="text-red-600 hover:text-red-900"
                        title="Excluir quarto"
                        @click="removeRoom(room.id)"
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

      <section class="px-4 py-6 sm:px-0">
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
                Calendário de Ocupação
              </h2>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Visualize rapidamente quais quartos estão livres ou reservados no período selecionado.
              </p>
            </div>
            <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
              <div>
                <label for="inicio" class="block text-sm font-medium text-gray-700">Data inicial</label>
                <input
                  id="inicio"
                  v-model="calendarRange.inicio"
                  type="date"
                  class="mt-1 input-field"
                >
              </div>
              <div>
                <label for="fim" class="block text-sm font-medium text-gray-700">Data final</label>
                <input
                  id="fim"
                  v-model="calendarRange.fim"
                  type="date"
                  class="mt-1 input-field"
                >
              </div>
              <button
                class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                :disabled="calendarLoading"
                @click="fetchCalendar"
              >
                <svg
                  v-if="calendarLoading"
                  class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                {{ calendarLoading ? 'Carregando...' : 'Atualizar calendário' }}
              </button>
            </div>
          </div>

          <div v-if="calendarLoading" class="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
            Carregando ocupação...
          </div>

          <div v-else-if="calendarData.length === 0" class="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
            {{ rooms.length ? 'Nenhum quarto encontrado no período selecionado.' : 'Cadastre quartos para visualizar a ocupação.' }}
          </div>

          <div v-else class="mt-6 space-y-6">
            <div
              v-for="quarto in calendarData"
              :key="quarto.quarto_id"
              class="border border-gray-200 dark:border-gray-700 rounded-lg"
            >
              <div class="p-4 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 class="text-base font-semibold text-gray-900 dark:text-gray-100">
                    Quarto {{ quarto.numero }} · {{ quarto.tipo }}
                  </h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    Capacidade: {{ quarto.capacidade }} · Diária: {{ formatCurrency(quarto.valor_diaria) }}
                  </p>
                </div>
                <span
                  class="inline-flex px-2 py-1 text-xs font-semibold leading-5 rounded-full"
                  :class="statusBadgeClass(quarto.status)"
                >
                  {{ statusLabels[quarto.status] || quarto.status }}
                </span>
              </div>

              <div class="p-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6">
                <div
                  v-for="dia in quarto.ocupacao"
                  :key="`${quarto.quarto_id}-${dia.data}`"
                  class="border border-gray-200 dark:border-gray-700 rounded-md p-3"
                  :class="dia.status === 'reservado' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'"
                >
                  <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {{ formatDate(dia.data) }}
                  </p>
                  <p
                    class="text-xs font-semibold uppercase tracking-wide"
                    :class="dia.status === 'reservado' ? 'text-red-600' : 'text-green-600'"
                  >
                    {{ dia.status }}
                  </p>
                  <p v-if="dia.reserva_id" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Reserva #{{ dia.reserva_id }} · Cliente {{ dia.cliente_id }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

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
import { computed, onMounted, ref, watch, reactive } from 'vue'
import { useAuth } from '~/composables/useAuth'
import {
  createRoom,
  deleteRoom,
  getRoomCalendar,
  getRooms,
  updateRoom,
  type Room,
  type RoomCalendar,
  type RoomCreate,
  type RoomUpdate
} from '~/services/apiClient'
import { VMoney3 } from 'v-money3'

definePageMeta({
  middleware: ['auth'],
  alias: ['/rooms']
})

const { logout } = useAuth()

const rooms = ref<Room[]>([])
const loadingRooms = ref(true)
const loading = ref(false)
const showForm = ref(false)
const editingRoom = ref<Room | null>(null)
const searchTerm = ref('')
const statusFilter = ref<'todos' | string>('todos')
const statusOptions = ['disponivel', 'ocupado', 'manutencao']

type RoomFormState = {
  numero: string
  tipo: string
  status: string
  capacidade: number | ''
  valor_diaria: number | ''
  descricao: string
}

const moneyConfig = {
  decimal: ',',
  thousands: '.',
  prefix: 'R$ ',
  suffix: '',
  precision: 2,
  masked: false,
}

const form = reactive<RoomFormState>({
  numero: '',
  tipo: '',
  status: 'disponivel',
  capacidade: 1,
  valor_diaria: '',
  descricao: ''
})

const calendarLoading = ref(false)
const calendarData = ref<RoomCalendar[]>([])
const calendarRange = ref({
  inicio: formatDateInput(new Date()),
  fim: formatDateInput(addDays(new Date(), 7))
})

const message = ref<{ type: 'success' | 'error'; text: string } | null>(null)

const statusLabels: Record<string, string> = {
  disponivel: 'Disponível',
  ocupado: 'Ocupado',
  manutencao: 'Em manutenção'
}

const filteredRooms = computed(() => {
  return rooms.value.filter((room) => {
    const matchesStatus =
      statusFilter.value === 'todos' || room.status === statusFilter.value
    const term = searchTerm.value.trim().toLowerCase()

    if (!term) {
      return matchesStatus
    }

    const text = `${room.numero} ${room.tipo}`.toLowerCase()
    return matchesStatus && text.includes(term)
  })
})

function formatCurrency(value: number): string {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function formatDateInput(date: Date): string {
  return date.toISOString().split('T')[0]
}

function addDays(date: Date, days: number): Date {
  const clone = new Date(date)
  clone.setDate(clone.getDate() + days)
  return clone
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

function statusBadgeClass(status: string): string {
  const map: Record<string, string> = {
    disponivel: 'bg-green-100 text-green-800',
    ocupado: 'bg-red-100 text-red-800',
    manutencao: 'bg-yellow-100 text-yellow-800'
  }
  return map[status] || 'bg-gray-100 dark:bg-gray-800 text-gray-800'
}

function showMessage(type: 'success' | 'error', text: string) {
  message.value = { type, text }
  setTimeout(() => {
    if (message.value?.text === text) {
      message.value = null
    }
  }, 5000)
}

async function loadRooms() {
  try {
    loadingRooms.value = true
    rooms.value = await getRooms(0, 200)
  } catch (error) {
    showMessage('error', 'Erro ao carregar quartos.')
    rooms.value = []
  } finally {
    loadingRooms.value = false
  }
}

async function fetchCalendar() {
  if (!calendarRange.value.inicio || !calendarRange.value.fim) {
    showMessage('error', 'Informe as datas inicial e final.')
    return
  }

  try {
    calendarLoading.value = true
    calendarData.value = await getRoomCalendar(
      calendarRange.value.inicio,
      calendarRange.value.fim
    )
  } catch (error) {
    showMessage('error', 'Não foi possível carregar o calendário.')
    calendarData.value = []
  } finally {
    calendarLoading.value = false
  }
}

async function submitForm() {
  if (!form.numero || !form.tipo || !form.valor_diaria) {
    showMessage('error', 'Preencha os campos obrigatórios.')
    return
  }

  const capacidadeValue = Number(form.capacidade) || 1
  const valorDiariaNumber = Number(
    String(form.valor_diaria)
      .replace(/[R$\s]/g, '') // remove R$ e espaços
      .replace('.', '')        // remove separador de milhar
      .replace(',', '.')
  )

  if (!Number.isFinite(valorDiariaNumber) || valorDiariaNumber <= 0) {
    showMessage('error', 'Informe um valor de diária válido.')
    return
  }

  const basePayload = {
    numero: form.numero.trim(),
    tipo: form.tipo.trim(),
    status: form.status,
    capacidade: capacidadeValue,
    valor_diaria: valorDiariaNumber,
    descricao: form.descricao.trim() ? form.descricao.trim() : undefined
  }

  try {
    loading.value = true
    if (editingRoom.value) {
      const updatePayload: RoomUpdate = { ...basePayload }
      await updateRoom(editingRoom.value.id, updatePayload)
      showMessage('success', 'Quarto atualizado com sucesso!')
    } else {
      const createPayload: RoomCreate = { ...basePayload }
      await createRoom(createPayload)
      showMessage('success', 'Quarto criado com sucesso!')
    }

    await loadRooms()
    await fetchCalendar()
    cancelForm()
  } catch (error: any) {
    const detail = error?.data?.detail || 'Erro ao salvar quarto.'
    showMessage('error', detail)
  }
}

function editRoom(room: Room) {
  editingRoom.value = room
  form.numero = room.numero
  form.tipo = room.tipo
  form.status = room.status
  form.capacidade = room.capacidade
  form.valor_diaria = room.valor_diaria
  form.descricao = room.descricao || ''
  showForm.value = true
}

async function removeRoom(id: number) {
  if (!confirm('Deseja realmente excluir este quarto?')) {
    return
  }

  try {
    loading.value = true
    await deleteRoom(id)
    showMessage('success', 'Quarto removido com sucesso!')
    await loadRooms()
    await fetchCalendar()
  } catch (error: any) {
    const detail = error?.data?.detail || 'Falha ao remover quarto.'
    showMessage('error', detail)
  } finally {
    loading.value = false
  }
}

function cancelForm() {
  showForm.value = false
  editingRoom.value = null
  form.numero = ''
  form.tipo = ''
  form.status = 'disponivel'
  form.capacidade = ''
  form.valor_diaria = ''
  form.descricao = ''
}

function handleLogout() {
  logout()
  navigateTo('/login')
}

onMounted(async () => {
  await loadRooms()
  await fetchCalendar()
})

let debounceTimer: ReturnType<typeof setTimeout> | null = null
watch([
  () => calendarRange.value.inicio,
  () => calendarRange.value.fim
], () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  debounceTimer = setTimeout(() => {
    fetchCalendar()
  }, 600)
})

useHead({
  title: 'Quartos - Hotel Management',
  meta: [
    { name: 'description', content: 'Gestão de quartos e ocupação do hotel' }
  ]
})
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>
