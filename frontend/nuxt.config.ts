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
      apiUrl: process.env.API_BASE_URL || 'http://localhost:8000',
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