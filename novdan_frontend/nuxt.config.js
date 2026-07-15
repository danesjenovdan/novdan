import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  app: {
    head: {
      link: [{ rel: 'stylesheet', href: '/fonts/selfhosted.css' }]
    }
  },
  css: ['~/assets/main.scss'],
  runtimeConfig: {
    apiBase: process.env.NUXT_API_BASE,
    public: {
      apiClientId: process.env.NUXT_API_CLIENT_ID,
      apiBase: process.env.NUXT_API_BASE_BROWSER || process.env.NUXT_API_BASE
    }
  }
})
