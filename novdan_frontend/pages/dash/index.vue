<template>
  <div>
    <h1>DASH</h1>
    <div>api base: {{ $config.apiBase }}</div>
    <div>{{ status }}</div>
    <nuxt-link to="/dash/login?logout=true"> Logout </nuxt-link>
  </div>
</template>

<script>
import api from '~/mixins/api.js'

export default {
  mixins: [api],
  data() {
    return {
      status: null
    }
  },
  async mounted() {
    if (!this.$api.hasToken()) {
      this.$router.replace('/dash/login')
    }
    this.status = await this.$api.getStatus()
  }
}
</script>

<style lang="scss" scoped></style>
