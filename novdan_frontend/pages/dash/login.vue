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
    </form>
    <p v-if="error" class="error">
      Prijava ni uspela.
    </p>
    <a
      target="_blank"
      href="/terms"
      style="width: 100%; display: inline-block; padding-top: 20px"
    >Splošni pogoji uporabe</a>
    <div style="height: 2rem;"></div>
    <h3>Še nimaš računa?</h3>
    <nuxt-link to="/dash/register" class="btn-large">
      Ustvari račun
    </nuxt-link>
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
        console.log(error.response.data)
      }
    }
  }
}
</script>
