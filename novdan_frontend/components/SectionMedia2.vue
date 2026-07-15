<template>
  <section class="background-gradient-orange-pink media" @mousemove="tiltTiles">
    <div class="container">
      <h2>Sodelujoči</h2>
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
              <router-link to="/ppporocila">
                <span>Petkova Propagandna Poročila</span>
                <img
                  src="~assets/images/jenull.png"
                  alt="Petkova Propagandna Poročila logo"
                  :style="`transform: rotate(${tilted * 0.5}deg)`"
                />
              </router-link>
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
      default: 0,
    },
  },
  data() {
    return {
      tilted: 0,
    };
  },
  methods: {
    tiltTiles(event) {
      const positionX = event.pageX;
      const windowWidth = window.innerWidth;
      const windowCenter = windowWidth / 2;
      const tilted = ((windowCenter - positionX) / windowCenter) * -45;
      this.tilted = tilted / 2;
    },
  },
};
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
      justify-content: center;
    }
  }

  h2 {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin: 0;
    text-align: center;

    @media (min-width: 992px) {
      font-size: 4rem;
    }
  }

  ul {
    list-style-type: none;
    padding-left: 0;
    margin-bottom: 0;

    li {
      margin: 2rem 0;

      &:last-child {
        margin-bottom: 0;
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

        &:hover {
          text-decoration: underline;
        }
      }

      span {
        padding-left: 1.5rem;
      }

      img {
        height: 3rem;
      }
    }
  }
}
</style>
