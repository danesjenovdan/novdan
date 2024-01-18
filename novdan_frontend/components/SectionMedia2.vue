<template>
  <section class="background-gradient-orange-pink media" @mousemove="tiltTiles">
    <div class="container">
      <h2>
        Sodelujoči
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
                  src="~assets/images/imr.svg"
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
</style>
