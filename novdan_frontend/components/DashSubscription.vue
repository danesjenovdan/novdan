<template>
  <section id="how-section" class="background-gradient-yellow-white subscription">
    <div class="container">
      <div class="content-narrow">
        <h3>Naročnina</h3>
        <div class="row">
          <div class="subscribe">
            <div class="moneybill" :class="{'disabled': !isSubscribed}">
              <img src="~assets/images/5-eur.svg" alt="pink spinning star">
              <div class="effect">
                <img src="~assets/images/zarki-roza.svg" alt="pink spinning star">
              </div>
            </div>
            <div v-if="isSubscribed">
              <h6>Tvoja <span>naročnina</span> je aktivna.</h6>
              <p>Obračunamo jo vsakega 1. v mesecu.</p>
            </div>
            <div v-if="!isSubscribed">
              <h6>Tvoja <span>naročnina</span> še ni aktivna.</h6>
              <p>Obračunamo jo vsakega 1. v mesecu.</p>
            </div>
          </div>
          <div class="support-wrapper">
            <a v-if="!isSubscribed" class="button" @click="activate">
              <div class="support">
                Aktiviraj
              </div>
              <div class="star">
                <img src="~assets/images/star.png" alt="pink spinning star">
              </div>
            </a>
            <div v-if="isSubscribed" class="payment-method">
              <button>Zamenjaj plačilno sredstvo</button>
              <span @click="cancelSubscription">Prekini naročnino</span>
            </div>
            <div v-if="extensionNotInstalled" class="no-extension">
              <p>Vtičnik še ni inštaliran.</p>
              <div class="browsers">
                <div class="button-browser-wrapper">
                  <div class="support">
                    Chrome
                  </div>
                  <div class="button">
                    <img src="~assets/images/chrome.png" class="browser" alt="pink spinning star">
                    <img src="~assets/images/modra-zvezda.svg" class="spinning-star" alt="pink spinning star">
                  </div>
                </div>
                <div class="button-browser-wrapper">
                  <div class="support">
                    Firefox
                  </div>
                  <div class="button">
                    <img src="~assets/images/mozilla.png" class="browser" alt="pink spinning star">
                    <img src="~assets/images/modra-zvezda.svg" class="spinning-star" alt="pink spinning star">
                  </div>
                </div>
              </div>
            </div>
            <div v-if="extensionError" class="warning">
              <p>Prijava v vtičnik ni uspela.</p>
            </div>
          </div>
        </div>

        <hr />

        <div class="user-settings">
          <h3>Uporabniški račun</h3>
          <nuxt-link to="/dash/login?logout=true" class="logout-button">
            Odjavi se
          </nuxt-link>
        </div>
        <h2>Sprememba gesla</h2>
        <form @submit.prevent="changePassword">
          <!-- <div class="input-group">
            <label for="username">Uporabniški račun</label>
            <input id="username" type="text" name="username" /><span>Spremeni</span>
          </div> -->
          <div class="input-group">
            <label for="password-old">Staro geslo</label>
            <input id="password-old" type="password" name="password-old" v-model="oldPassword" />
          </div>
          <div class="input-group">
            <label for="password-new">Novo geslo</label>
            <input id="password-new" type="password" name="password-new" v-model="newPassword" />
          </div>
          <div class="input-group">
            <label for="password-confirm">Potrdi novo geslo</label>
            <input id="password-confirm" type="password" name="password-confirm" v-model="confirmNewPassword" />
          </div>
          <button id="password-submit" type="submit" class="logout-button">Pošlji</button>
        </form>

        <hr v-if="isSubscribed" />

        <div v-if="isSubscribed" style="position:relative;">
          <h3>Tvoja razporeditev</h3>
          <p class="text-small">
            Ta mesec si medijem doniral <span>{{ status.monetized_time }} sekund</span> svoje pozornosti
          </p>
          <pie-chart :section-data="status.monetized_split" class="pie-chart"></pie-chart>
          <div class="pink-bg" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import PieChart from './PieChart.vue'
import api from '~/mixins/api.js'

export default {
  components: { PieChart },
  mixins: [api],
  props: {
    windowWidth: {
      type: Number,
      default: 0
    },
    status: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmNewPassword: ''
    }
  },
  computed: {
    isSubscribed() {
      if (this.status && this.status.active_subscription) {
        return true
      }
      return false
    },
    extensionNotInstalled() {
      return true
    },
    extensionError() {
      return false
    }
  },
  methods: {
    // async logout() {
    //   try {
    //     await this.$api.logout()
    //     this.$router.push('/dash/login')
    //   } catch (error) {
    //     // TODO: show error
    //   }
    // },
    activate() {
      this.$router.push('/payment')
    },
    async cancelSubscription() {
      if (window.confirm('Ste prepričani, da želite preklicati naročnino?')) {
        try {
          const response = await this.$api.cancelSubscription()
          console.log(response)
        } catch (error) {
          console.log(error)
        }
      }
    },
    async changePassword() {
      if (this.oldPassword.length > 0 && this.newPassword.length > 0 && this.confirmNewPassword.length > 0) {
        if (this.newPassword === this.confirmNewPassword) {
          try {
            const response = await this.$api.changePassword(this.oldPassword, this.newPassword)
            console.log(response)
          } catch (error) {
            console.log(error)
          }
        }
      }
    }
  }
}
</script>

<style scoped lang="scss">
.subscription {
  padding: 4rem 1rem;
  overflow: hidden;
  @media (min-width: 992px) {
    padding: 6rem 30px;
  }
  .row {
    display: block;
    @media (min-width: 992px) {
      display: flex;
    }
  }
  h3 {
    font-size: 3rem;
    font-weight: 400;
    font-family: "Le Murmure";
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 0;
    margin-bottom: 2rem;
  }
  .subscribe {
    margin: 4rem 0;
    text-align: center;
    @media (min-width: 992px) {
      padding-left: 5rem;
      margin: 1rem;
      margin-right: 12rem;
      transform: rotate(-5deg);
    }
    .moneybill {
      position: relative;
      &>img {
        z-index: 2;
        position: relative;
        width: 16rem;
        @media (min-width: 1200px) {
          width: 20rem;
        }
      }
      .effect {
        width: 16rem;
        height: auto;
        top: 50%;
        left: 50%;
        position: absolute;
        transition: all 0.25s ease;
        transform: translateY(-50%) translateX(-50%) scale(2.25);
      }
      &.disabled {
        opacity: 0.6;
        .effect {
          transform: translateY(-50%) translateX(-50%) scale(1.625);
        }
      }
      // &:hover {
      //   .effect {
      //     transform: translateY(-50%) translateX(-50%) scale(2.5);
      //   }
      // }
    }
    h6 {
      font-size: 24px;
      font-weight: 400;
      line-height: 0.6;
      margin-bottom: 0;
      text-align: center;
      span {
        font-family: 'Syne Tactile', cursive;
        color: #1103b1;
      }
    }
    p {
      margin-top: 0.5rem;
      font-size: 12px;
      text-align: center;
    }
  }

  .support-wrapper {
    z-index: 2;
    margin-top: 2rem;
    @media (min-width: 576px) {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    @media (min-width: 992px) {
      display: block;
    }
    .button {
      text-decoration: none;
      color: black;
      position: relative;
      display: flex;
      align-items: center;
      .support {
        font-size: 1.5rem;
        font-weight: 700;
        padding: 0.5rem 5rem 0.5rem 2rem;
        border: 3px solid #000000;
        border-radius: 1.25rem;
        background-color: white;
        position: relative;
        z-index: 3;
        transition: all 0.25s ease;
        transform: rotate(0) scale(1);
        @media (min-width: 1200px) {
          font-size: 2rem;
        }
        @media (min-width: 1400px) {
          font-size: 3rem;
          padding: 0.5rem 7rem 0.5rem 2rem;
        }
      }
      .star {
        position: absolute;
        z-index: 3;
        left: 10rem;
        img {
          height: 8rem;
          animation: rotate360 3s linear infinite;  /* animation set */
          @media (min-width: 992px) {
            animation-play-state: paused;
          }
        }
        div {
          position: absolute;
          top: 2.75rem;
          left: 2.5rem;
          z-index: 4;
          display: flex;
          align-items: flex-end;
          span:first-child {
            font-size: 2rem;
            font-weight: 700;
            line-height: 1;
          }
          span:last-child {
            font-size: 0.75rem;
            font-style: italic;
            display: inline-block;
            font-family: 'Syne Tactile', cursive;
          }
        }
        @media (min-width: 768px) {
          left: 10rem;
        }
        @media (min-width: 1200px) {
          left: 12rem;
        }
        @media (min-width: 1400px) {
          left: unset;
          right: -4rem;
          img {
            height: 11rem;
          }
          div {
            top: 3.5rem;
            left: 3.5rem;
            span:first-child {
              font-size: 3rem;
            }
            span:last-child {
              font-size: 1rem;
            }
          }
        }
      }
      &:hover {
        cursor: pointer;
        .star img {
          animation-play-state: running;
        }
        .support {
          background-color: #ffd700;
          @media (min-width: 1200px) {
            transform:rotate(0) scale(1.1);
          }
        }
      }
    }
    .subtitle {
      margin-top: 2rem;
      margin-left: 3rem;
      font-size: 1.5rem;
      font-weight: 700;
      span {
        color: #1103b1;
        font-weight: 400;
        font-family: 'Syne Tactile', cursive;
      }
    }
    .payment-method {
      button {
        background-color: white;
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 8px 20px;
        font-family: "Syne", sans-serif;
        font-size: 20px;
        font-weight: 500;
        display: block;
        margin: 10px 0;
        width: 100%;
        @media (min-width: 768px) {
          width: unset;
        }
        cursor: pointer;
        &:hover {
          background-color: #1103b1;
          border-color: #1103b1;
          color: white;
        }
      }
      span {
        text-decoration: underline;
        cursor: pointer;
        display: block;
        text-align: center;
        @media (min-width: 768px) {
          text-align: left;
          margin-left: 22px;
        }
        &:hover {
          color: #1103b1;
        }
      }
    }
    .warning {
      margin: 40px 0;
      p {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: red;
      }
    }
    .no-extension {
      margin: 40px 0;
      p {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 0.5rem;
      }
      .browsers {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        @media (min-width: 992px) {
          // align-items: center;
          justify-content: center;
        }
      }
      .support {
        text-decoration: none;
        font-size: 2.5rem;
        font-weight: 700;
        padding: 0.25rem 4rem 0.25rem 1rem;
        border: 3px solid #000000;
        border-radius: 1.25rem;
        background-color: white;
        position: relative;
        z-index: 3;
        transition: all 0.25s ease;
        transform: rotate(0) scale(1);
        cursor: pointer;
        @media (min-width: 1200px) {
          font-size: 2rem;
        }
      }
      .button-browser-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        margin: 1rem 0;
        @media (min-width: 992px) {
        }
        .button {
          position: absolute;
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 5;
          right: 0;
          transform: translateX(50%);
          cursor: pointer;
          .browser {
            position: absolute;
            z-index: 6;
            height: 2.5rem;
          }
          .spinning-star {
            width: 6rem;
            animation: rotate360 3s linear infinite;
            animation-play-state: paused;
          }
        }
        &:hover {
          .support {
            background-color: #ffd700;
            // @media (min-width: 992px) {
            //   transform: rotate(0) scale(1.2);
            // }
          }
          .spinning-star {
            animation-play-state: running;
          }
        }
      }
    }
  }
  .user-settings {
    display: flex;
    justify-content: space-between;
    align-items: center;
    h3 {
      margin-bottom: 0;
    }
  }
  hr {
    border: 1px solid #ffd700;
    margin: 4rem 0;
  }
  form {
    .input-group {
      margin-bottom: 30px;
      @media (min-width: 992px) {
        margin-bottom: 20px;
      }
    }
    label {
      display: block;
      color: #1103b1;
      font-family: 'Syne Tactile', cursive;
      font-size: 20px;
      line-height: 0.8;
      letter-spacing: 1px;
      margin-bottom: 10px;
    }
    span {
      text-decoration: underline;
      margin: 5px 0;
      display: block;
      cursor: pointer;
      @media (min-width: 992px) {
        margin: 0 0 0 16px;
        display: inline;
      }
      &:hover {
        color: #1103b1;
      }
    }
    input {
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
  }
  .logout-button {
    border: 2px solid #000000;
    border-radius: 10px;
    background-color: #ffffff;
    font-family: 'Syne', sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: black;
    padding: 8px 24px;
    margin: 10px 0;
    text-decoration: none;
    display: inline-block;
    cursor: pointer;
    &:hover {
      background-color: #1103b1;
      border-color: #1103b1;
      color: white;
    }
  }
  .text-small {
    font-size: 1.5rem;
    line-height: 1.75rem;
    span {
      font-weight: 800;
    }
    @media (min-width: 992px) {
      margin: 1rem 9rem 2rem 9rem;
      font-size: 2rem;
      line-height: 2.5rem;
    }
  }
  .pie-chart {
    height: 200px;
    float: right;
    margin-right: 10rem;
  }
  .pink-bg {
    position: absolute;
    left: 0;
    top: 0;
    width: 300px;
    height: 300px;
    background-image: radial-gradient(circle 150px at center, #ff5ccb 0%, rgba(255, 92, 203, 0) 100%);
    opacity: 0.4;
    z-index: -1;
    @media (min-width: 768px) {
      top: -10%;
      left: 40%;
    }
    @media (min-width: 992px) {
      top: -11rem;
      left: 31rem;
      width: 622px;
      height: 622px;
      background-image: radial-gradient(circle 311px at center, #ff5ccb 0%, rgba(255, 92, 203, 0) 100%);
    }
  }
}

</style>
