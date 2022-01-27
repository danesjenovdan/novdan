<template>
  <div class="payment">
    <h3>PLAČILO</h3>

    <div class="buttons-wrapper links">
      <button
        :class="{ active: paymentType == 'card' }"
        @click="paymentType = 'card'"
      >
        Kreditna kartica
      </button>
      <button
        :class="{ active: paymentType == 'paypal' }"
        @click="paymentType = 'paypal'"
      >
        Paypal
      </button>
    </div>

    <Card
      v-if="token && paymentType == 'card'"
      :token="token"
      @ready="onPaymentReady"
      @validity-change="paymentInfoValid = $event"
      @payment-start="paymentInProgress = true"
      @success="paymentSuccess"
      @error="paymentError"
    />

    <Paypal
      v-if="token && paymentType == 'paypal'"
      :token="token"
      :amount="5"
      :recurring="false"
      @ready="onPaymentReady"
      @payment-start="paymentInProgress = true"
      @success="paymentSuccess"
    />

    <div class="buttons-wrapper">
      <button @click="finish">
        Plačaj
      </button>
    </div>
  </div>
</template>

<script>
import api from '~/mixins/api.js'

export default {
  mixins: [api],
  layout: 'login',
  data() {
    return {
      token: null,
      paymentInfoValid: false,
      paymentInProgress: false,
      paymentType: 'card',
      payFunction: undefined,
      nonce: undefined
    }
  },
  async mounted() {
    const response = await this.$api.activateSubscription()
    this.token = response.token
  },
  methods: {
    onPaymentReady({ pay } = {}) {
      this.checkoutLoading = false
      this.paymentInfoValid = false
      this.payFunction = pay
    },
    finish() {
      if (this.payFunction) {
        this.payFunction()
      }
    },
    async paymentSuccess({ nonce } = {}) {
      this.paymentInProgress = true
      this.nonce = nonce
      try {
        const response = await this.$api.activateSubscription2(this.nonce)
        this.$router.push('/dash')
        this.paymentInProgress = false
        // this.$router.push(
        //   response.upload_token
        //     ? `/doniraj/hvala?token=${response.upload_token}`
        //     : '/doniraj/hvala'
        // )
        console.log(response)
        // this.paymentInProgress = true
      } catch (error) {
        // eslint-disable-next-line no-console
        console.error(error.response)
        this.error = error.response
      }
    },
    paymentError(argument) {
      // eslint-disable-next-line
      console.log('ERROR VERY ERROR')
      // eslint-disable-next-line
      console.log(argument)
    }
  }
}
</script>

<style lang="scss" scoped>
h3 {
  text-align: center;
}
.buttons-wrapper {
  text-align: center;
  margin: 20px 0;
  button {
    border: 2px solid #000000;
    border-radius: 10px;
    background-color: #ffffff;
    font-family: 'Syne', sans-serif;
    font-size: 25px;
    font-weight: 700;
    padding: 8px 24px;
    margin: 10px 0;
    cursor: pointer;
    &.active {
      background-color: #ffd700;
    }
    &:hover {
      background-color: #1103b1;
      border-color: #1103b1;
      color: white;
    }
  }
}
.buttons-wrapper.links {
  button {
    border: none;
    border-radius: 0;
    background-color: transparent;
    font-size: 18px;
    font-weight: 400;
    padding: 8px;
    &.active {
      background-color: transparent;
      text-decoration: underline;
    }
    &:hover {
      background-color: #1103b1;
      border-color: #1103b1;
      color: white;
    }
  }
}

</style>
