<template>
  <section class="background-black chooser">
    <div class="container">
      <div>
        <div class="headline">
          <h2>POSTANI PODPORNIK</h2>
          <p>Izberi višino mesečne podpore.</p>
        </div>
        <div class="amount-buttons">
          <template v-for="da in donationAmounts">
            <button
              v-if="Number(da.amount) > 0"
              :key="da.id"
              @click.prevent="
                $router.push(`/${medium.slug}/podpri?${queryString(da.amount)}`)
              "
            >
              <div v-if="da.name">
                {{ da.name }}
              </div>
              <div class="amount">
                {{ Number(da.amount) }}&nbsp;€
              </div>
            </button>
            <div
              v-else-if="Number(da.amount) === -1"
              :key="`custom-${da.id}`"
              class="button"
              @click.prevent="focusInput"
            >
              <div>{{ da.name || 'Poljubni znesek' }}</div>
              <form class="amount" @submit.prevent="continueWithCustomAmount">
                <input v-model="customAmount" type="number" />&nbsp;€
              </form>
            </div>
          </template>
        </div>
        <div class="disclaimer">
          Neposredna finančna podpora omogoča neodvisno delovanje in prinaša
          avtorju motivacijo za nadaljne ustvarjanje vsebin ter pomaga pri
          pokrivanju stroškov programske in druge opreme. Za spletno doniranje
          skrbi
          <a
            href="https://danesjenovdan.si"
            target="_blank"
            rel="noopener noreferrer"
          >Danes je nov dan</a>, ves izkupiček gre avtorju.
        </div>
        <div class="continue-button">
          <button
            :disabled="!customAmount || customAmount <= 0"
            @click.prevent="continueWithCustomAmount"
          >
            Nadaljuj
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SectionPaymentChooser',
  props: {
    medium: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      default: 'recurring'
    }
  },
  data() {
    return {
      customAmount: ''
    }
  },
  computed: {
    donationAmounts() {
      return this.medium.donation_amounts.filter(da => da[this.type]).sort(
        (a, b) => {
          if (Number(a.amount) === -1) { return 1 }
          if (Number(b.amount) === -1) { return -1 }
          return Number(a.amount) - Number(b.amount)
        }
      )
    }
  },
  methods: {
    queryString(amount) {
      const params = new URLSearchParams()
      if (this.type === 'one_time') {
        params.append('enkratno', 'true')
      }
      params.append('znesek', amount)
      return params.toString()
    },
    focusInput() {
      const input = this.$el.querySelector('.amount-buttons .button input')
      if (input) {
        input.focus()
      }
    },
    continueWithCustomAmount() {
      if (this.customAmount && this.customAmount > 0) {
        this.$router.push(
          `/${this.medium.slug}/podpri?${this.queryString(this.customAmount)}`
        )
      }
    }
  }
}
</script>

<style scoped lang="scss">
.chooser {
  padding-inline: 1rem;
  padding-block: 2rem;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue',
    'Noto Sans', 'Liberation Sans', Arial, sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  color: #fff;

  a {
    color: inherit;
  }

  .headline {
    text-align: center;
    font-size: 1.25rem;

    @media (min-width: 768px) {
      font-size: 1.75rem;
    }

    h2,
    p {
      margin: 0;
    }
  }

  .amount-buttons {
    margin-block: 3rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-content: center;
    gap: 1rem;

    @media (min-width: 768px) {
      display: flex;
      justify-content: center;
      gap: 1rem;
    }

    button,
    .button {
      flex: 1;
      background-color: #fff;
      border: none;
      border-radius: 0.5rem;
      color: #000;
      font: inherit;
      font-size: 1.25rem;
      font-weight: 700;
      text-align: center;
      padding: 0.75rem 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease;

      @media (min-width: 768px) {
        padding: 1.75rem 1.5rem;
        font-size: 1.5rem;
      }

      &:hover {
        background-color: #e0e0e0;
      }

      .amount {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 800;

        @media (min-width: 768px) {
          font-size: 3rem;
        }

        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
          -webkit-appearance: none;
          margin: 0;
        }

        input[type='number'] {
          -moz-appearance: textfield;
        }

        input {
          flex: 1;
          width: 100%;
          margin-top: 0.5rem;
          padding: 0.25rem;
          font: inherit;
          font-size: inherit;
          font-weight: 700;
          border: 1px solid #000;
          border-radius: 0.5rem;
          text-align: center;

          &:focus-visible {
            outline: 4px solid #ffd700;
          }
        }
      }
    }
  }

  .continue-button {
    margin-top: 2rem;
    text-align: center;

    button {
      flex: 1;
      background-color: #fff;
      border: none;
      border-radius: 0.5rem;
      color: #000;
      font: inherit;
      font-size: 1.5rem;
      font-weight: 700;
      text-align: center;
      padding: 0.75rem 2.5rem;
      cursor: pointer;
      transition: background-color 0.3s ease;

      &:hover {
        background-color: #e0e0e0;
      }

      &:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
      }
    }
  }

  .disclaimer {
    max-width: 800px;
    margin-inline: auto;
    font-size: 1rem;
    text-align: center;

    @media (min-width: 768px) {
      font-size: 1.125rem;
    }
  }
}
</style>
