<template>
  <section id="how-section" class="background-gradient-white-yellow how">
    <div class="container">
      <h1>Kako?</h1>
      <div v-if="windowWidth > 992">
        <div class="row first">
          <p>
            Inštaliraj si
            <span
              >Nov<br />
              Dan vtičnik</span
            >.
          </p>
          <div class="browsers">
            <a
              target="_blank"
              href="https://chrome.google.com/webstore/detail/nov-dan/lioeapnoibjfgmeicjnghkoaoalnggik?hl=sl"
              class="button-browser-wrapper"
            >
              <div class="support">Chrome</div>
              <div class="button">
                <img
                  src="~assets/images/chrome.png"
                  class="browser"
                  alt="pink spinning star"
                />
                <img
                  src="~assets/images/modra-zvezda.svg"
                  class="spinning-star"
                  alt="pink spinning star"
                />
              </div>
            </a>
            <a
              target="_blank"
              href="https://addons.mozilla.org/sl-SI/firefox/addon/nov-dan/"
              class="button-browser-wrapper"
            >
              <div class="support">Firefox</div>
              <div class="button">
                <img
                  src="~assets/images/mozilla.png"
                  class="browser"
                  alt="pink spinning star"
                />
                <img
                  src="~assets/images/modra-zvezda.svg"
                  class="spinning-star"
                  alt="pink spinning star"
                />
              </div>
            </a>
          </div>
        </div>
        <div class="row">
          <div class="subscribe">
            <p>Plačaj <br />naročnino.</p>
            <div class="moneybill">
              <img src="~assets/images/5-eur.svg" alt="pink spinning star" />
              <div class="effect">
                <img
                  src="~assets/images/zarki-roza.svg"
                  alt="pink spinning star"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="read">
            <p>
              Beri <br /><span>neodvisne</span><br />
              medije.
            </p>
            <div>
              <img
                src="~assets/images/vesoljcek.png"
                alt="pink spinning star"
              />
            </div>
          </div>
        </div>
        <div class="row forth" style="justify-content: end">
          <div>
            <p style="text-align: end">
              <span>Tvoj prispevek bo</span><br />
              <span>med njih razdeljen</span><br />
              <span>glede na tvoj</span><br />
              <span>čas branja.</span>
            </p>
          </div>
        </div>
      </div>
      <div v-if="windowWidth <= 992" class="how-mobile">
        <div class="row">
          <p>
            Nov dan je eksperimentalna platforma, ki zaenkrat podpira samo
            Firefox in Chrome računalniške brskalnike.
          </p>
          <div class="subscribe">
            <div class="moneybill">
              <div>
                <span>obišči</span><br />
                <span><a href="/">novdan.si</a></span
                ><br />
                <span>na računalniku</span>
              </div>
              <div class="effect">
                <img
                  src="~assets/images/zarki-rumeni.svg"
                  alt="pink spinning star"
                />
              </div>
            </div>
            <div>
              <p>Spomni se kasneje</p>
              <a
                href="mailto:?subject=Se%20spomni%C5%A1%20platforme%20Nov%20dan%3F&body=Nov%20dan%20je%20eksperimentalna%20platforma%20za%20podporo%20neodvisnim%20medijem%20in%20medijskim%20ustvarjalcem%2C%20ki%20deluje%20s%20pomo%C4%8Djo%20novega%20odprtega%20standarda%20za%20spletno%20monetizacijo%20(web%20monetization%20standard%20%E2%80%93%20WMS).%20Povezavo%20do%20vti%C4%8Dnika%20za%20brskalnik%20dobi%C5%A1%20na%20https%3A%2F%2Fnovdan.si"
                class="support"
                >pošlji si e-mail!</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    windowWidth: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style scoped lang="scss">
.how {
  padding: 6rem 30px;
  overflow-x: hidden;
  .row {
    display: block;
    @media (min-width: 992px) {
      display: flex;
    }
  }
  h1 {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 0;
    margin-bottom: 2rem;
    @media (min-width: 992px) {
      font-size: 5rem;
      text-align: center;
    }
    @media (min-width: 1200px) {
      font-size: 7rem;
    }
  }
  p {
    text-transform: uppercase;
    font-size: 1.5rem;
    font-weight: 700;
    position: relative;
    z-index: 2;
    margin: 5rem 0;
    span {
      font-weight: 800;
    }
    @media (min-width: 1200px) {
      font-size: 2.5rem;
    }
  }
  .first {
    margin-top: 4rem;
    margin-bottom: 6rem;
  }
  .browsers {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    @media (min-width: 992px) {
      align-items: center;
      justify-content: center;
    }
  }
  .support {
    display: block;
    text-decoration: none;
    font-size: 2.5rem;
    font-weight: 700;
    padding: 0.25rem 6rem 0.25rem 1rem;
    border: 3px solid #000000;
    border-radius: 1.25rem;
    background-color: white;
    position: relative;
    z-index: 3;
    transition: all 0.25s ease;
    transform: rotate(0) scale(1);
    cursor: pointer;
    @media (min-width: 1200px) {
      font-size: 3rem;
    }
  }
  .button-browser-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    margin: 2rem 0;
    text-decoration: none;
    color: #000000;
    @media (min-width: 992px) {
      &:first-child {
        margin-left: 8rem;
      }
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
        height: 4rem;
      }
      .spinning-star {
        width: 10rem;
        animation: rotate360 3s linear infinite;
        animation-play-state: paused;
      }
    }
    &:hover {
      .support {
        background-color: #ffd700;
        @media (min-width: 992px) {
          transform: rotate(0) scale(1.2);
        }
      }
      .spinning-star {
        animation-play-state: running;
      }
    }
  }

  .subscribe {
    @media (min-width: 992px) {
      display: flex;
      align-items: center;
      margin-left: 8rem;
    }
    .moneybill {
      margin-left: 5rem;
      position: relative;
      & > img {
        z-index: 2;
        position: relative;
        width: 16rem;
        @media (min-width: 1200px) {
          width: 24rem;
        }
      }
      .effect {
        width: 16rem;
        height: auto;
        top: 50%;
        left: 50%;
        position: absolute;
        transition: all 0.25s ease;
        transform: translateY(-50%) translateX(-50%) scale(1);
      }
      &:hover {
        .effect {
          transform: translateY(-50%) translateX(-50%) scale(3);
        }
      }
    }
  }
  .read {
    display: flex;
    @media (min-width: 992px) {
      margin-left: 16rem;
    }
    & > div {
      margin-top: 5rem;
      margin-left: 3rem;
      transition: all 0.25s ease;
      transform: rotate(0) scale(1);
      img {
        width: 18rem;
      }
      &:hover {
        transform: rotate(0) scale(1.2);
      }
    }
  }
  .forth {
    p {
      span {
        font-weight: 700;
        background-color: white;
        margin: 0.5rem 0;
        padding: 0 0.25rem;
        display: inline-block;
        &:last-child {
          font-weight: 800;
        }
      }
    }
  }
  .how-mobile {
    p {
      text-transform: none;
      font-weight: 500;
      margin: 2rem 0;
    }
    .moneybill {
      margin-left: 0;
      div:first-child {
        text-align: center;
        position: relative;
        z-index: 5;
        margin: 5rem 0;
        span:first-child,
        span:last-child {
          text-transform: uppercase;
          font-weight: 700;
        }
        span:first-child {
          font-size: 2.25rem;
        }
        span:nth-of-type(2) {
          font-size: 2.5rem;
          font-weight: 900;
          line-height: 0.75;
          a {
            color: #1103b1;
            text-decoration: none;
          }
        }
        span:last-child {
          font-size: 1.75rem;
          line-height: 1.5;
        }
      }
      .effect {
        transform: translateY(-50%) translateX(-50%) scale(2) rotate(-5deg);
        img {
          width: unset;
        }
      }
      &:hover {
        .effect {
          transform: translateY(-50%) translateX(-50%) scale(2) rotate(-5deg);
        }
      }
    }
    .subscribe {
      div:last-child {
        text-align: center;
        p {
          font-weight: 700;
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }
        .support {
          font-family: 'wf-syne-tactile', cursive;
          font-weight: 400;
          font-size: 2rem;
          color: #1103b1;
          padding: 0.5rem;
        }
      }
    }
  }
}
</style>
