<template>
  <div class="min-h-screen relative overflow-hidden flex flex-col">
    <AnimatedBackground />
    
    <div class="relative z-10 flex flex-col flex-1">
    <nav class="bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl shadow-sm border-b border-gray-200/50 dark:border-gray-700/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-12 w-12 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center shadow-lg p-2">
                <img src="/log_plataformahote.png" alt="Plataforma Hotel" class="w-full h-full object-contain" />
              </div>
            </div>
            <div class="ml-4">
              <h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
                Plataforma Hotel
              </h1>
              <p v-if="userInfo" class="text-sm text-gray-500 dark:text-gray-400">
                Olá, {{ userInfo.username }}
              </p>
            </div>
          </div>

          <div class="flex items-center space-x-3">
            <ThemeToggle />
            <button
              type="button"
              class="text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors"
              @click="handleLogout"
            >
              Sair
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <header class="px-4 sm:px-0">
        <h1 class="text-3xl font-bold text-white dark:text-gray-100 drop-shadow-lg">
          Dashboard do Hotel
        </h1>
        <p class="mt-2 text-sm text-white/90 dark:text-gray-300">
          Bem-vindo ao sistema de gerenciamento de hotel
        </p>
      </header>

      <!-- Stats Cards -->
      <section class="px-4 py-6 sm:px-0">
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm overflow-hidden shadow-lg rounded-lg border border-white/20 dark:border-gray-700/30 hover:shadow-xl hover:scale-105 transition-all duration-300">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                      Total de Clientes
                    </dt>
                    <dd class="text-lg font-medium text-gray-900 dark:text-gray-100">
                      {{ stats.totalClients }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm overflow-hidden shadow-lg rounded-lg border border-white/20 dark:border-gray-700/30 hover:shadow-xl hover:scale-105 transition-all duration-300">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-500 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                      Reservas Ativas
                    </dt>
                    <dd class="text-lg font-medium text-gray-900 dark:text-gray-100">
                      {{ stats.activeReservas }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm overflow-hidden shadow-lg rounded-lg border border-white/20 dark:border-gray-700/30 hover:shadow-xl hover:scale-105 transition-all duration-300">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-purple-500 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                      Quartos Ocupados
                    </dt>
                    <dd class="text-lg font-medium text-gray-900 dark:text-gray-100">
                      {{ stats.occupiedRooms }} / {{ stats.totalRooms }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm overflow-hidden shadow-lg rounded-lg border border-white/20 dark:border-gray-700/30 hover:shadow-xl hover:scale-105 transition-all duration-300">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-green-500 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                      Receita do Mês
                    </dt>
                    <dd class="text-lg font-medium text-gray-900 dark:text-gray-100">
                      {{ formatCurrency(stats.monthlyRevenue) }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Quick Actions -->
      <section class="px-4 py-6 sm:px-0">
        <h2 class="text-lg font-medium text-white dark:text-gray-100 mb-4 drop-shadow-lg">
          Ações Rápidas
        </h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Clientes -->
          <NuxtLink
            to="/clients"
            class="block p-6 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg border border-white/20 dark:border-gray-700/30 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 bg-gradient-to-br from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700 rounded-lg flex items-center justify-center shadow-md">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Clientes
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-300">
                  Gerenciar clientes do hotel
                </p>
              </div>
            </div>
          </NuxtLink>

          <!-- Reservas -->
          <NuxtLink
            to="/reservas"
            class="block p-6 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg border border-white/20 dark:border-gray-700/30 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 bg-gradient-to-br from-green-500 to-green-600 dark:from-green-600 dark:to-green-700 rounded-lg flex items-center justify-center shadow-md">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Reservas
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-300">
                  Gerenciar reservas e hospedagens
                </p>
              </div>
            </div>
          </NuxtLink>

          <!-- Quartos -->
          <NuxtLink
            to="/quartos"
            class="block p-6 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg border border-white/20 dark:border-gray-700/30 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 bg-gradient-to-br from-orange-500 to-orange-600 dark:from-orange-600 dark:to-orange-700 rounded-lg flex items-center justify-center shadow-md">
                  <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
                  Quartos
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-300">
                  Gerenciar quartos e ocupação
                </p>
              </div>
            </div>
          </NuxtLink>
        </div>
      </section>

      <!-- Recent Activity -->
      <section class="px-4 py-6 sm:px-0">
        <h2 class="text-lg font-medium text-white dark:text-gray-100 mb-4 drop-shadow-lg">
          Atividade Recente
        </h2>
        <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm shadow-lg rounded-lg border border-white/20 dark:border-gray-700/30">
          <div class="px-6 py-4">
            <div v-if="isLoading" class="text-sm text-gray-600 dark:text-gray-300">
              Carregando dashboard...
            </div>
            <div v-else-if="errorMessage" class="text-sm text-red-500 dark:text-red-400">
              {{ errorMessage }}
            </div>
            <div v-else-if="recentActivities.length === 0" class="text-sm text-gray-600 dark:text-gray-300">
              Nenhuma atividade recente disponível.
            </div>
            <div v-else class="flow-root">
              <ul class="-mb-8">
                <li v-for="(activity, index) in recentActivities" :key="activity.id">
                  <div class="relative pb-8" :class="{ 'pb-0': index === recentActivities.length - 1 }">
                    <span
                      v-if="index !== recentActivities.length - 1"
                      class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200 dark:bg-gray-700"
                      aria-hidden="true"
                     />
                    <div class="relative flex space-x-3">
                      <div>
                        <span
                          class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white dark:ring-gray-800"
                          :class="activity.iconBg"
                        >
                          <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getIconPath(activity.icon)" />
                          </svg>
                        </span>
                      </div>
                      <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p class="text-sm text-gray-600 dark:text-gray-300">
                            {{ activity.description }}
                          </p>
                        </div>
                        <div class="text-right text-sm whitespace-nowrap text-gray-600 dark:text-gray-300">
                          {{ activity.relativeTime }}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </main>
    
    <AppFooter />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { getDashboardSummary, type DashboardActivityResponse } from '~/services/apiClient'

// Meta da página - protegida por middleware de auth
definePageMeta({
  middleware: ['auth']
})

interface DashboardStatsView {
  totalClients: number
  activeReservas: number
  occupiedRooms: number
  totalRooms: number
  monthlyRevenue: number
}

interface ActivityCard {
  id: number
  description: string
  relativeTime: string
  icon: string
  iconBg: string
}

const createInitialStats = (): DashboardStatsView => ({
  totalClients: 0,
  activeReservas: 0,
  occupiedRooms: 0,
  totalRooms: 0,
  monthlyRevenue: 0
})

// Composables
const { logout, token } = useAuth()

// Estados reativos
const stats = ref<DashboardStatsView>(createInitialStats())
const recentActivities = ref<ActivityCard[]>([])
const isLoading = ref(false)
const errorMessage = ref<string | null>(null)

const relativeTimeFormatter = new Intl.RelativeTimeFormat('pt-BR', {
  numeric: 'auto'
})

const eventIconMap: Record<string, { icon: string; iconBg: string }> = {
  reserva_confirmada: { icon: 'calendar', iconBg: 'bg-green-500' },
  reserva_cancelada: { icon: 'cancel', iconBg: 'bg-red-500' },
  default: { icon: 'calendar', iconBg: 'bg-blue-500' }
}

const formatCurrency = (value: number) => {
  const safeValue = Number.isFinite(value) ? value : 0
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2
  }).format(safeValue)
}

const formatRelativeTime = (dateString: string) => {
  const date = new Date(dateString)
  if (Number.isNaN(date.getTime())) {
    return ''
  }

  const diffSeconds = (date.getTime() - Date.now()) / 1000
  const DIVISIONS: { amount: number; unit: Intl.RelativeTimeFormatUnit }[] = [
    { amount: 60, unit: 'second' },
    { amount: 60, unit: 'minute' },
    { amount: 24, unit: 'hour' },
    { amount: 7, unit: 'day' },
    { amount: 4.34524, unit: 'week' },
    { amount: 12, unit: 'month' },
    { amount: Infinity, unit: 'year' }
  ]

  let duration = diffSeconds
  for (const division of DIVISIONS) {
    if (Math.abs(duration) < division.amount) {
      return relativeTimeFormatter.format(
        Math.round(duration),
        division.unit
      )
    }
    duration /= division.amount
  }

  return ''
}

const transformActivity = (activity: DashboardActivityResponse): ActivityCard => {
  const iconMeta = eventIconMap[activity.event_type] ?? eventIconMap.default

  return {
    id: activity.id,
    description: activity.description,
    relativeTime: formatRelativeTime(activity.created_at),
    icon: iconMeta.icon,
    iconBg: iconMeta.iconBg
  }
}

const resetDashboardState = () => {
  stats.value = createInitialStats()
  recentActivities.value = []
  errorMessage.value = null
}

const loadDashboard = async () => {
  if (!token.value) {
    return
  }

  isLoading.value = true
  errorMessage.value = null

  try {
    const data = await getDashboardSummary()

    stats.value = {
      totalClients: data.stats.total_clients,
      activeReservas: data.stats.active_reservas,
      occupiedRooms: data.stats.occupied_rooms,
      totalRooms: data.stats.total_rooms,
      monthlyRevenue: data.stats.monthly_revenue
    }

    // Buscar atividades recentes da API
    const activitiesResponse = await apiClient.get('/dashboard/activities')
    const activities = activitiesResponse.data
    
    // Transformar atividades para o formato esperado
    recentActivities.value = activities.map((activity: any) => {
      const actionMap: Record<string, { description: string; icon: string; iconBg: string }> = {
        'LOGIN_SUCCESS': { description: '🔐 Login realizado', icon: 'user', iconBg: 'bg-green-500' },
        'LOGIN_FAILED': { description: '❌ Falha no login', icon: 'cancel', iconBg: 'bg-red-500' },
        'LOGOUT': { description: '🚪 Logout', icon: 'user', iconBg: 'bg-gray-500' },
        'CREATE_CLIENT': { description: '➕ Cliente criado', icon: 'user-plus', iconBg: 'bg-blue-500' },
        'UPDATE_CLIENT': { description: '✏️ Cliente atualizado', icon: 'wrench', iconBg: 'bg-yellow-500' },
        'DELETE_CLIENT': { description: '🗑️ Cliente excluído', icon: 'cancel', iconBg: 'bg-red-500' },
        'CREATE_ROOM': { description: '🏨 Quarto criado', icon: 'calendar', iconBg: 'bg-green-500' },
        'UPDATE_ROOM': { description: '🔧 Quarto atualizado', icon: 'wrench', iconBg: 'bg-yellow-500' },
        'DELETE_ROOM': { description: '🗑️ Quarto excluído', icon: 'cancel', iconBg: 'bg-red-500' },
        'CREATE_RESERVATION': { description: '📅 Reserva criada', icon: 'calendar', iconBg: 'bg-green-500' },
        'UPDATE_RESERVATION': { description: '📝 Reserva atualizada', icon: 'wrench', iconBg: 'bg-yellow-500' },
        'DELETE_RESERVATION': { description: '❌ Reserva cancelada', icon: 'cancel', iconBg: 'bg-red-500' },
        'USER_CREATED': { description: '👤 Usuário criado', icon: 'user-plus', iconBg: 'bg-indigo-500' }
      }
      
      const actionInfo = actionMap[activity.action] || { 
        description: `${activity.action} - ${activity.resource}`, 
        icon: 'calendar', 
        iconBg: 'bg-gray-500' 
      }
      
      return {
        id: activity.id,
        description: actionInfo.description,
        relativeTime: formatRelativeTime(activity.timestamp),
        icon: actionInfo.icon,
        iconBg: actionInfo.iconBg
      }
    })
  } catch (error) {
    console.error('Erro ao carregar dashboard', error)
    errorMessage.value = 'Não foi possível carregar os dados do dashboard.'
  } finally {
    isLoading.value = false
  }
}

watch(
  token,
  (newToken) => {
    if (newToken) {
      loadDashboard()
    } else {
      resetDashboardState()
    }
  },
  { immediate: true }
)

// Computed para informações do usuário
const userInfo = computed(() => {
  if (!token.value) { return null }

  try {
    const payload = JSON.parse(atob(token.value.split('.')[1]))
    return {
      username: payload.sub
    }
  } catch (error) {
    return null
  }
})

// Função para retornar o caminho do ícone SVG
const getIconPath = (iconType: string) => {
  const paths = {
    calendar: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
    cancel: 'M6 18L18 6M6 6l12 12',
    user: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
    'user-plus': 'M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2m9-12a4 4 0 110-8 4 4 0 010 8zm6 0v6m3-3h-6',
    wrench: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
  }
  return paths[iconType as keyof typeof paths] || paths.calendar
}

// Função de logout
const handleLogout = async () => {
  logout()
  resetDashboardState()
  await navigateTo('/login')
}

// SEO e meta tags
useHead({
  title: 'Dashboard - Plataforma Hotel',
  meta: [
    { name: 'description', content: 'Dashboard da Plataforma Hotel' }
  ]
})
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>
