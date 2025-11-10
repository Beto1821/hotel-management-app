import { VMoney3 } from 'v-money3'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('money3', VMoney3)
})
