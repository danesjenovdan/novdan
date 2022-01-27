<template>
  <div>
    <h3>REGISTRACIJA</h3>
    <form @submit.prevent="onSubmit">
      <div class="input-group">
        <label>Uporabniško ime</label>
        <input v-model="username" type="text" :disabled="processing" />
      </div>
      <div class="input-group">
        <label>E-pošta</label>
        <input v-model="email" type="email" :disabled="processing" />
      </div>
      <div class="input-group">
        <label>Geslo</label>
        <input v-model="password" type="password" :disabled="processing" />
      </div>
      <div class="input-group">
        <label>Potrdite geslo</label>
        <input v-model="confirm_password" type="password" :disabled="processing" />
      </div>
      <p v-if="processing">
        Pošiljanje...
      </p>
      <input type="submit" value="Ustvari račun" :disabled="processing" />
      <nuxt-link to="/dash/login">
        Prijavi se
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
      email: '',
      password: '',
      confirm_password: '',
      processing: false,
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
      this.processing = true
      try {
        await this.$api.register(this.username, this.email, this.password, this.confirm_password)
        // redirect to payment
        this.$router.replace('/payment')
      } catch (error) {
        // TODO: show error
        this.error = true
        console.log(error)
      }
      this.processing = false
    }
  }
}
</script>
