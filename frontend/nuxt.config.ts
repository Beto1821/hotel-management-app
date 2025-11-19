export default defineNuxtConfig({
  // Compatibilidade com Nitro
  compatibilityDate: '2025-11-06',

  // Configuração de desenvolvimento
  devtools: { enabled: true },

  // Módulos do Nuxt
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt'
  ],

  // Configuração de CSS
  css: [
    '~/assets/css/main.css'
  ],

  // Configuração do Tailwind
  tailwindcss: {
    config: {
      darkMode: 'class'
    }
  },

  // Configuração de TypeScript
  typescript: {
    strict: true,
    typeCheck: true
  },

  // Configuração de SSR
  ssr: true,

  // Configuração de roteamento
  router: {
    options: {
      hashMode: false
    }
  },

  // Configuração do runtime
  runtimeConfig: {
    // Variáveis privadas (apenas no servidor)
    apiSecret: '',

    // Variáveis públicas (expostas no cliente)
    public: {
      // Nova chave `apiUrl` — usada por `services/apiClient.ts`.
      // Primeiro procura `NUXT_PUBLIC_API_URL` (recomendado para Nuxt),
      // depois `API_BASE_URL` (compatibilidade com README),
      // e por fim `http://localhost:8000` como fallback.
      apiUrl: process.env.NUXT_PUBLIC_API_URL || process.env.API_BASE_URL || 'http://localhost:8000',

      // Mantemos `apiBase` por compatibilidade com configurações anteriores,
      // mas `apiUrl` é a chave que o cliente realmente consome.
      apiBase: process.env.API_BASE_URL || process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
      appName: 'Hotel Management'
    }
  },

  // Configuração de Nitro
  nitro: {
    preset: 'node-server'
  },

  // Configuração de plugins
  plugins: [],

  // Configuração de componentes
  components: {
    global: true,
    dirs: ['~/components']
  },

  // Configuração de imports automáticos
  imports: {
    dirs: ['composables/**', 'utils/**']
  },

  // Configuração de middleware
  // O middleware será aplicado automaticamente

  // Configuração de meta tags globais
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Hotel Management System',
      meta: [
        { name: 'description', content: 'Sistema de gerenciamento de hotel moderno e eficiente' },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  }
})
