<template>
  <div>
    <h3>REGISTRACIJA </h3>
    <form @submit.prevent="onSubmit">
      <div class="input-group">
        <label>Uporabniško ime</label>
        <input v-model="username" type="text" />
      </div>
      <div class="input-group">
        <label>E-pošta</label>
        <input v-model="email" type="email" />
      </div>
      <div class="input-group">
        <label>Geslo</label>
        <input v-model="password" type="password" />
      </div>
      <div class="input-group">
        <label>Potrdite geslo</label>
        <input v-model="confirm_password" type="password" />
      </div>
      <input type="submit" value="Ustvari račun" />
    </form>
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
      confirm_password: ''
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
        await this.$api.register(this.username, this.email, this.password, this.confirm_password)
        this.$router.push('/dash') // na placilo sajt
      } catch (error) {
        // TODO: show error
      }
    }
  }
}
</script>
