<template>
  <section class="background-gradient-orange-pink media" @mousemove="tiltTiles">
    <div class="container">
      <h2>
        Sodelujoči <br />
        mediji
      </h2>
      <div class="row">
        <div>
          <ul>
            <li>
              <a href="https://www.ostro.si/" target="_blank">
                <span>Oštro</span>
                <img
                  src="~assets/images/ostro.svg"
                  alt="Oštro logo"
                  :style="`transform: rotate(${tilted * 0.6}deg)`"
                />
              </a>
            </li>
            <li>
              <a href="https://vezjak.com/" target="_blank">
                <span>Boris Vezjak - In Media Res</span>
                <img
                  src="~assets/images/vezjak-favicon.svg"
                  alt="Boris Vezjak - In Media Res logo"
                  :style="`transform: rotate(${tilted * 0.8}deg)`"
                />
              </a>
            </li>
            <li>
              <a href="https://mesanec.si/" target="_blank">
                <span>Mešanec</span>
                <img
                  src="~assets/images/mesanec.svg"
                  alt="Mešanec.si logo"
                  :style="`transform: rotate(${tilted * 0.2}deg)`"
                />
              </a>
            </li>
            <li>
              <a href="https://www.dsavic.net/" target="_blank">
                <span>Domen Savič - Državljan D</span>
                <img
                  src="~assets/images/drzavljan-d.svg"
                  alt="Domen Savič - Državljan D logo"
                  :style="`transform: rotate(${tilted * 0.4}deg)`"
                />
              </a>
            </li>
            <li>
              <a href="https://danesjenovdan.si/agrument/" target="_blank">
                <span>Agrument</span>
                <img
                  src="~assets/images/djnd.svg"
                  alt="Agrument logo"
                  :style="`transform: rotate(${tilted * 0.5}deg)`"
                />
              </a>
            </li>
          </ul>
        </div>
        <div class="support-section">
          <div class="support-wrapper">
            <a href="#how-section" class="button">
              <div class="support">Pridruži se!</div>
              <div class="star">
                <img src="~assets/images/star.png" alt="pink spinning star" />
                <div>
                  <span>5</span>
                  <span>eur/<br />mes</span>
                </div>
              </div>
            </a>
            <div class="subtitle">
              <p>Podpri <span>neodvisne</span> medije.</p>
            </div>
          </div>
          <div v-if="windowWidth > 1200" class="yellow-bg" />
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
  },
  data() {
    return {
      tilted: 0
    }
  },
  methods: {
    tiltTiles(event) {
      const positionX = event.pageX
      const windowWidth = window.innerWidth
      const windowCenter = windowWidth / 2
      const tilted = ((windowCenter - positionX) / windowCenter) * -45
      this.tilted = tilted / 2
    }
  }
}
</script>

<style scoped lang="scss">
.media {
  padding: 4rem 30px;
  overflow: hidden;
  @media (min-width: 1200px) {
    padding: 6rem 0;
  }
  .row {
    display: block;
    @media (min-width: 1200px) {
      display: flex;
    }
  }
  h2 {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin: 0;
    @media (min-width: 992px) {
      font-size: 4rem;
    }
  }
  ul {
    list-style-type: none;
    padding-left: 0;
    li {
      margin: 2rem 0;
      @media (min-width: 1400px) {
        margin: 0;
      }
      a {
        text-decoration: none;
        text-transform: uppercase;
        color: black;
        font-size: 1.5rem;
        font-weight: 700;
        position: relative;
        display: flex;
        align-items: center;
        flex-direction: row-reverse;
        justify-content: flex-end;
        @media (min-width: 1200px) {
          font-size: 1.75rem;
        }
        @media (min-width: 1400px) {
          display: inline-block;
          max-width: unset;
          font-size: 2rem;
        }
      }
      span {
        padding-left: 2rem;
        @media (min-width: 1400px) {
          padding-left: 0;
          padding-right: 2rem;
        }
      }
      img {
        height: 3rem;

        @media (min-width: 1400px) {
          height: 5rem;
          position: relative;
          bottom: -1.5rem;
        }
      }
    }
  }
}

.support-section {
  display: flex;
  align-items: center;
  @media (min-width: 1200px) {
    margin-left: 4rem;
  }
  @media (min-width: 1400px) {
    margin-left: 8rem;

    .yellow-bg {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translateY(-50%);
      width: 622px;
      height: 622px;
      background-image: radial-gradient(
        circle 311px at center,
        #ffd700 0%,
        rgba(255, 215, 0, 0) 100%
      );
      opacity: 0.4;
      z-index: 1;
    }
  }
}

.support-wrapper {
  z-index: 2;
  margin-top: 2rem;
  @media (min-width: 1200px) {
    margin-top: 0;
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
      left: 12rem;
      img {
        height: 8rem;
        animation: rotate360 3s linear infinite; /* animation set */
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
          font-family: 'wf-syne-tactile', cursive;
        }
      }
      @media (min-width: 1200px) {
        left: unset;
        right: 2rem;
      }
      @media (min-width: 1400px) {
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
          transform: rotate(0) scale(1.1);
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
      font-family: 'wf-syne-tactile', cursive;
    }
  }
}
</style>
