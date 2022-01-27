<template>
  <div>
    <h3>PRIJAVA</h3>
    <form @submit.prevent="onSubmit">
      <div class="input-group">
        <label>Uporabniško ime</label>
        <input v-model="username" type="text" />
      </div>
      <div class="input-group">
        <label>Geslo</label>
        <input v-model="password" type="password" />
      </div>
      <input type="submit" value="Prijava" />
      <nuxt-link to="/dash/register">
        Ustvari račun
      </nuxt-link>
    </form>
    <p v-if="error" class="error">
      Prišlo je do napake.
    </p>
  </div>
</template>

<script>
import api from '~/mixins/api.js'

export default {
  mixins: [api],
  layout: 'login',
  data() {
    return {
      username: '',
      password: '',
      error: false
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
        this.error = true
      }
    }
  }
}
</script>
