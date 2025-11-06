<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and Title -->
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h1 class="text-xl font-semibold text-gray-900">Hotel Management</h1>
            </div>
          </div>

          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">
              Olá, <span class="font-medium">{{ userInfo?.username || 'Usuário' }}</span>
            </span>
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
        <h1 class="text-3xl font-bold text-gray-900">Dashboard do Hotel</h1>
        <p class="mt-2 text-sm text-gray-600">
          Bem-vindo ao sistema de gerenciamento de hotel
        </p>
      </div>

      <!-- Stats Cards -->
      <div class="px-4 py-6 sm:px-0">
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <!-- Total de Clientes -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Total de Clientes
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ stats.totalClients }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Reservas Ativas -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Reservas Ativas
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ stats.activeReservations }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Quartos Ocupados -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Quartos Ocupados
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      {{ stats.occupiedRooms }} / {{ stats.totalRooms }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <!-- Receita do Mês -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">
                      Receita do Mês
                    </dt>
                    <dd class="text-lg font-medium text-gray-900">
                      R$ {{ stats.monthlyRevenue.toLocaleString() }}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="px-4 py-6 sm:px-0">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Ações Rápidas</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Clientes -->
          <NuxtLink
            to="/clientes"
            class="block p-6 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">Clientes</h3>
                <p class="text-sm text-gray-500">Gerenciar clientes do hotel</p>
              </div>
            </div>
          </NuxtLink>

          <!-- Agendamentos -->
          <NuxtLink
            to="/agendamentos"
            class="block p-6 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">Agendamentos</h3>
                <p class="text-sm text-gray-500">Gerenciar reservas e agendamentos</p>
              </div>
            </div>
          </NuxtLink>

          <!-- Quartos -->
          <NuxtLink
            to="/quartos"
            class="block p-6 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0h2M7 7h.01M7 3h.01" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">Quartos</h3>
                <p class="text-sm text-gray-500">Gerenciar quartos e ocupação</p>
              </div>
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="px-4 py-6 sm:px-0">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Atividade Recente</h2>
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4">
            <div class="flow-root">
              <ul class="-mb-8">
                <li v-for="(activity, index) in recentActivities" :key="index">
                  <div class="relative pb-8" :class="{ 'pb-0': index === recentActivities.length - 1 }">
                    <span 
                      v-if="index !== recentActivities.length - 1"
                      class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                    ></span>
                    <div class="relative flex space-x-3">
                      <div>
                        <span class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white"
                              :class="activity.iconBg">
                          <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getIconPath(activity.icon)" />
                          </svg>
                        </span>
                      </div>
                      <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p class="text-sm text-gray-500">
                            {{ activity.description }}
                          </p>
                        </div>
                        <div class="text-right text-sm whitespace-nowrap text-gray-500">
                          {{ activity.time }}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuth } from '~/composables/useAuth'

// Meta da página - protegida por middleware de auth
definePageMeta({
  middleware: ['auth']
})

// Composables
const { logout, token } = useAuth()

// Estados reativos
const stats = ref({
  totalClients: 45,
  activeReservations: 12,
  occupiedRooms: 8,
  totalRooms: 20,
  monthlyRevenue: 25800
})

const recentActivities = ref([
  {
    description: 'Nova reserva criada para João Silva - Quarto 105',
    time: '2 min atrás',
    icon: 'calendar',
    iconBg: 'bg-green-500'
  },
  {
    description: 'Check-out realizado - Maria Santos - Quarto 203',
    time: '1 hora atrás',
    icon: 'user',
    iconBg: 'bg-blue-500'
  },
  {
    description: 'Novo cliente cadastrado - Pedro Oliveira',
    time: '3 horas atrás',
    icon: 'user-plus',
    iconBg: 'bg-purple-500'
  },
  {
    description: 'Manutenção concluída no Quarto 301',
    time: '1 dia atrás',
    icon: 'wrench',
    iconBg: 'bg-yellow-500'
  }
])

// Computed para informações do usuário
const userInfo = computed(() => {
  if (!token.value) return null
  
  try {
    // Decodificar payload do JWT para obter username
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
    user: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
    'user-plus': 'M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2m9-12a4 4 0 110-8 4 4 0 010 8zm6 0v6m3-3h-6',
    wrench: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'
  }
  return paths[iconType as keyof typeof paths] || paths.user
}

// Função de logout
const handleLogout = async () => {
  logout()
  await navigateTo('/login')
}

// SEO e meta tags
useHead({
  title: 'Dashboard - Hotel Management',
  meta: [
    { name: 'description', content: 'Dashboard do sistema de gerenciamento de hotel' }
  ]
})
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>