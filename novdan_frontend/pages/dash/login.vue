<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="onSubmit">
      <input v-model="username" type="text" />
      <input v-model="password" type="password" />
      <input type="submit" />
    </form>
  </div>
</template>

<script>
import api from '~/mixins/api.js'

export default {
  mixins: [api],
  data() {
    return {
      username: '',
      password: ''
    }
  },
  async mounted() {
    if (this.$route.query.logout) {
      await this.$api.logout()
      this.$router.replace('/dash/login')
    }
  },
  methods: {
    async onSubmit() {
      try {
        await this.$api.login(this.username, this.password)
        this.$router.push('/dash')
      } catch (error) {
        // TODO: show error
      }
    }
  }
}
</script>

<style lang="scss" scoped></style>
