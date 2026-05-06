<template>
  <section class="chooser">
    <div class="container">
      <div>
        <div class="headline">
          <h2>POSTANI PODPORNIK</h2>
          <div class="right">
            <a v-if="type === 'recurring'" class="link" href="?enkratno=true">Želim donirati enkraten znesek</a>
            <a v-else class="link" href="?">Želim donirati mesečno</a>
            <a class="link" href="#" @click.prevent="cancelSupport">Prekini podporo</a>
          </div>
        </div>
        <div class="subheadline">
          <p v-if="type === 'recurring'">
            Pomagaj zagotoviti neodvisno ustvarjanje z mesečno donacijo.
          </p>
          <p v-else>
            Izberi višino enkratne podpore.
          </p>
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
              <div v-if="da.image">
                <img
                  :src="da.image"
                  alt=""
                  style="max-width: 100%; max-height: 120px; object-fit: contain;"
                />
              </div>
              <div v-if="da.name">
                {{ da.name }}
              </div>
              <div class="amount">
                {{ Number(da.amount) }}&nbsp;€
              </div>
              <div v-if="type === 'recurring'" class="period">
                /mesec
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
        <div v-if="customAmount && customAmount > 0" class="continue-button">
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
    },
    cancelSupport() {
      prompt('Prosimo kontaktirajte nas na e-naslovu:', 'novdan@djnd.si')
    }
  }
}
</script>

<style scoped lang="scss">
.chooser {
  padding-top: 1.75rem;
  margin-bottom: 2rem;
  border-top: 2px solid #000;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue',
    'Noto Sans', 'Liberation Sans', Arial, sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';

  a {
    color: inherit;
  }

  .headline {
    display: flex;
    flex-direction: column;
    text-align: center;
    font-size: 1.25rem;

    @media (min-width: 768px) {
      font-size: 1.5rem;
      flex-direction: row;
      text-align: left;
    }

    h2 {
      flex: 1;
      margin: 0;
    }

    .right {
      flex: 1;
      margin-block: 0.25rem;
      display: flex;
      gap: 0.25rem;
      flex-direction: column;
      align-items: center;
      text-align: center;
      font-size: 1.125rem;

      @media (min-width: 768px) {
        align-items: flex-end;
        text-align: right;
      }
    }
  }

  .subheadline {
    font-size: 1.25rem;
    text-align: center;

    @media (min-width: 768px) {
      font-size: 1.5rem;
      text-align: left;
    }

    p {
      margin-block: 1rem;
    }
  }

  .amount-buttons {
    margin-block: 1rem 2rem;
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

      .period {
        font-size: 1rem;
        line-height: 1;
        font-weight: 600;
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
