<template>
  <div class="register-form-container">
    <h3>REGISTRACIJA</h3>
    <loading v-if="processing" />
    <p>
      Za začetek te prosimo, da si ustvariš uporabniški račun. Tvoje podatke bo
      do tvojega preklica hranil
      <a href="https://danesjenovdan.si" target="_blank">inštitut Danes je nov dan</a>, in sicer
      na strežnikih v EU.
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
        <label>E-naslov</label>
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
        <label>Potrdi geslo</label>
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
      <p v-if="processing">
        Pošiljanje...
      </p>
      <input type="submit" value="Ustvari račun" :disabled="processing" />
    </form>
    <!-- <p v-if="error" class="error">Prišlo je do napake.</p> -->
    <a
      target="_blank"
      href="/terms"
      style="width: 100%; display: inline-block; padding-top: 20px"
    >Splošni pogoji uporabe</a>
    <div style="height: 2rem"></div>
    <h3>Že imaš račun?</h3>
    <nuxt-link to="/dash/login" class="btn-large">
      Prijavi se
    </nuxt-link>
  </div>
</template>

<script>
import api from '~/mixins/api.js'

export default {
  mixins: [api],
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

.register-form-container {
  h3 {
    font-size: 3rem;
    font-weight: 400;
    font-family: 'wf-le-murmure', serif;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 0;
    margin-bottom: 2rem;
  }
  form {
    .input-group {
      margin-bottom: 20px;
    }
    label {
      display: block;
      color: #1103b1;
      font-family: 'wf-syne-tactile', cursive;
      font-size: 20px;
      line-height: 0.8;
      letter-spacing: 1px;
      margin-bottom: 10px;
    }
    .form-input-error {
      color: red;
      margin: 6px 0 6px 16px;
    }
    span {
      margin-left: 16px;
      text-decoration: underline;
    }
    input[type='text'],
    input[type='email'],
    input[type='password'] {
      border-radius: 10px;
      border: 2px solid #1103b1;
      padding: 8px 16px;
      font-size: 20px;
      width: 90%;
      @media (min-width: 576px) {
        width: 480px;
      }
      @media (min-width: 992px) {
        width: 480px;
      }
    }
    input[type='submit'] {
      border: 2px solid #000000;
      border-radius: 10px;
      background-color: #ffffff;
      font-family: 'wf-syne', sans-serif;
      font-size: 25px;
      font-weight: 700;
      padding: 8px 24px;
      margin: 10px 0;
      cursor: pointer;
      &:hover {
        background-color: #1103b1;
        border-color: #1103b1;
        color: white;
      }
    }
    a {
      margin-left: 10px;
    }
  }
  .error {
    color: red;
  }
  .btn-large {
    border: 2px solid #000000;
    border-radius: 10px;
    background-color: #ffffff;
    font-family: 'wf-syne', sans-serif;
    font-size: 25px;
    font-weight: 700;
    padding: 8px 24px;
    margin: 10px 0;
    cursor: pointer;
    color: inherit;
    text-decoration: none;

    &:hover {
      background-color: #1103b1;
      border-color: #1103b1;
      color: white;
    }
  }
}
</style>
