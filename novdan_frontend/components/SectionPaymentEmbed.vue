<template>
  <section class="background-black embed">
    <div class="container">
      <div>
        <div>
          <iframe
            class="payment-frame"
            :src="embedUrl"
            frameborder="0"
          ></iframe>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SectionPaymentEmbed',
  props: {
    campaignSlug: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'recurring'
    },
    amount: {
      type: Number,
      default: null
    }
  },
  data() {
    return {}
  },
  computed: {
    hasAmount() {
      return this.amount != null && !isNaN(this.amount) && this.amount > 0
    },
    embedUrl() {
      let url = `https://moj.djnd.si/${this.campaignSlug}/doniraj`
      if (this.hasAmount && this.type === 'one_time') {
        url += `/placilo?znesek=${this.amount}`
      } else if (this.hasAmount && this.type === 'recurring') {
        url += `/info?mesecna=1&znesek=${this.amount}`
      } else if (this.type === 'recurring') {
        url += '?mesecna=1'
      } else if (this.type === 'one_time') {
        url += '?enkratna=1'
      }
      return url
    }
  }
}
</script>

<style scoped lang="scss">
.embed {
  color: #fff;

  .payment-frame {
    width: 100%;
    height: 830px;
    border: none;
  }
}
</style>
