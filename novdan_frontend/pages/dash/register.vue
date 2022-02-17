<template>
  <div>
    <h3>REGISTRACIJA</h3>
    <loading v-if="processing" />
    <p>
      Za začetek vas prosimo, da si ustvariš uporabniški profil. Tvoje podatke
      bo do tvojega preklica hranil
      <a href="https://danesjenovdan.si">inštitut Danes je nov dan</a> na
      strežnikih v EU.
    </p>
    <form @submit.prevent="onSubmit">
      <div class="input-group">
        <label>Uporabniško ime</label>
        <input v-model="username" type="text" :disabled="processing" />
        <p
          v-for="(error, index) in errors.username"
          :key="'eu-' + index"
          class="form-input-error"
        >
          {{ error }}
        </p>
      </div>
      <div class="input-group">
        <label>E-pošta</label>
        <input v-model="email" type="email" :disabled="processing" />
        <p
          v-for="(error, index) in errors.email"
          :key="'ee-' + index"
          class="form-input-error"
        >
          {{ error }}
        </p>
      </div>
      <div class="input-group">
        <label>Geslo</label>
        <input v-model="password" type="password" :disabled="processing" />
        <p
          v-for="(error, index) in errors.password"
          :key="'ep-' + index"
          class="form-input-error"
        >
          {{ error }}
        </p>
      </div>
      <div class="input-group">
        <label>Potrdite geslo</label>
        <input
          v-model="confirm_password"
          type="password"
          :disabled="processing"
        />
        <p
          v-for="(error, index) in errors.confirm_password"
          :key="'ecp-' + index"
          class="form-input-error"
        >
          {{ error }}
        </p>
      </div>
      <p v-if="processing">Pošiljanje...</p>
      <input type="submit" value="Ustvari račun" :disabled="processing" />
      <nuxt-link to="/dash/login"> Prijavi se </nuxt-link>
    </form>
    <!-- <p v-if="error" class="error">Prišlo je do napake.</p> -->
    <a
      target="_blank"
      href="/terms"
      style="width: 100%; display: inline-block; padding-top: 20px"
      >Splošni pogoji uporabe</a
    >
  </div>
</template>

<script>
import Loading from '../../components/Loading.vue'
import api from '~/mixins/api.js'

export default {
  components: { Loading },
  mixins: [api],
  layout: 'login',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirm_password: '',
      processing: false,
      errors: {}
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
      this.errors = {}
      try {
        await this.$api.register(
          this.username,
          this.email,
          this.password,
          this.confirm_password
        )
        // redirect to payment
        this.$router.replace('/payment')
      } catch (e) {
        this.errors = e.response.data
      }
      this.processing = false
    }
  }
}
</script>

<style lang="scss" scoped>
p {
  max-width: 516px;
}
</style>
