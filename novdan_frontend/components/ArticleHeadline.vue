<template>
  <section class="background-gif headline" @mousemove="tiltTiles">
    <div class="container">
      <div class="title">
        <h1>
          <a href="/">
            n<img class="sun" src="~assets/images/sun.png" alt="sun icon" />v
            dan
          </a>
        </h1>
        <p>
          Neposredna podpora <br />
          neodvisnim medijskim ustvarjalcem
        </p>
        <nav>
          <ul>
            <li><a href="/za-ustvarjalce">Za ustvarjalce</a></li>
            <li><a href="/dash/register">Za podpornike</a></li>
          </ul>
        </nav>
      </div>
    </div>
    <div class="container">
      <div class="preamble">
        <div class="description">
          <p>
            Nov dan je eksperimentalna platforma za podporo neodvisnim medijem
            in medijskim ustvarjalcem.
          </p>
          <p>
            Na enem mestu zbiramo ustvarjene vsebine in spodbujamo bralce, da
            podprete njihovo ustvarjanje s pomočjo našega donacijskega sistema,
            ki temelji na odprtem standardu za spletno monetizacijo (WMS) in
            omogoča pravično distribucijo podpornih sredstev.
          </p>
          <p>Sodelujoči:</p>
          <p class="logos">
            <a href="https://www.ostro.si/" target="_blank">
              <img
                src="~assets/images/ostro.svg"
                alt="Oštro logo"
                :style="`transform: rotate(${tilted * 0.6}deg)`"
              />
            </a>
            <a href="https://vezjak.com/" target="_blank">
              <img
                src="~assets/images/imr.svg"
                alt="Boris Vezjak - In Media Res logo"
                :style="`transform: rotate(${tilted * 0.8}deg)`"
              />
            </a>
            <a href="https://mesanec.si/" target="_blank">
              <img
                src="~assets/images/mesanec.svg"
                alt="Mešanec.si logo"
                :style="`transform: rotate(${tilted * 0.2}deg)`"
              />
            </a>
            <a href="https://www.dsavic.net/" target="_blank">
              <img
                src="~assets/images/drzavljan-d.svg"
                alt="Domen Savič - Državljan D logo"
                :style="`transform: rotate(${tilted * 0.4}deg)`"
              />
            </a>
            <a href="https://danesjenovdan.si/agrument/" target="_blank">
              <img
                src="~assets/images/djnd.svg"
                alt="Agrument logo"
                :style="`transform: rotate(${tilted * 0.5}deg)`"
              />
            </a>
          </p>
        </div>
        <div class="badge">
          <a href="/podpri" class="support-wrapper">
            <div class="star">
              <img src="~assets/images/star.png" alt="pink spinning star" />
              <div>
                <span>5</span>
                <span>eur/<br />mes</span>
              </div>
            </div>
            <div class="support">Podpri</div>
            <div class="yellow-bg" />
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// import { gsap } from 'gsap'
export default {
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
      this.tilted = tilted / 10
    }
  }
}
</script>

<style scoped lang="scss">
.headline {
  padding: 1rem;
  padding-bottom: 0;

  @media (min-width: 992px) {
    // for sticky badge
    margin-bottom: -10.5rem;
  }

  .container:nth-of-type(1) {
    position: relative;
    z-index: 2;
  }

  .title {
    margin: 1rem 0;

    @media (min-width: 768px) {
      display: flex;
      align-items: flex-end;
    }

    h1 {
      font-weight: 700;
      font-size: 5rem;
      line-height: 0.75;
      text-align: center;
      margin: 0;

      a {
        color: inherit;
        text-decoration: none;
      }
    }

    p {
      font-size: 1.25rem;
      line-height: 1;
      font-weight: 700;
      text-align: center;
      margin: 1rem 0;
    }

    nav {
      align-self: stretch;

      ul,
      li {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      ul {
        display: flex;
        flex-wrap: wrap;
        gap: 0.25rem 1.5rem;
        justify-content: center;

        li {
          a {
            color: inherit;
            font-weight: 500;
          }
        }
      }
    }

    @media (min-width: 768px) {
      h1 {
        text-align: right;
        padding-right: 1.5rem;
      }

      p {
        text-align: left;
        font-size: 1.5rem;
        margin: 0;
        flex: 1;
      }

      nav {
        padding-left: 1.5rem;

        ul {
          justify-content: flex-end;
        }
      }
    }
  }

  .sun {
    height: 2.5rem;
    width: 2.5rem;
  }

  .preamble {
    display: flex;
    flex-direction: column;
    margin-block: 2rem;

    @media (min-width: 992px) {
      flex-direction: row;
    }

    .description {
      flex: 1;

      @media (min-width: 992px) {
        margin-right: 2rem;
      }

      p {
        font-size: 1.25rem;
        margin: 0;
      }

      p + p {
        margin-top: 1.25rem;
      }

      a {
        color: inherit;
        text-decoration: underline;
      }

      .logos {
        a {
          img {
            width: 3rem;
          }
        }

        a + a {
          margin-left: 1rem;
        }
      }
    }

    .badge {
      --badge-size: 180px;

      margin-top: 1.5rem;
      width: var(--badge-size);
      height: calc(var(--badge-size) / 1.5);
      position: relative;

      @media (min-width: 992px) {
        margin-top: 0;
        visibility: hidden;
      }

      @keyframes rotate360 {
        to {
          transform: rotate(360deg);
        }
      }

      .support-wrapper {
        position: absolute;
        inset: 0;
        display: block;
        color: #000;
        text-decoration: none;
        cursor: pointer;
        transform-origin: center;
        transform: rotate(-10deg);

        &:hover {
          .support {
            background-color: #ffd700;
            @media (min-width: 992px) {
              transform: translateX(-50%) rotate(0) scale(1.2);
            }
          }

          .star > img {
            animation-play-state: running;
          }
        }

        .yellow-bg {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translateX(-50%) translateY(-50%);
          width: var(--badge-size);
          height: var(--badge-size);
          background-image: radial-gradient(
            circle calc(var(--badge-size) / 2) at center,
            #ffd700 0%,
            rgba(255, 215, 0, 0) 100%
          );
          opacity: 0.4;
          z-index: 1;
        }

        .star {
          width: calc(var(--badge-size) / 2);
          height: calc(var(--badge-size) / 2);
          position: absolute;
          z-index: 5;
          top: 0;
          left: 50%;
          transform: translateX(-50%);

          > img,
          > div {
            position: absolute;
            inset: 0;
            display: block;
            width: 100%;
            height: 100%;
          }

          > img {
            animation: rotate360 3s linear infinite;
          }

          > div {
            display: flex;
            align-items: center;
            justify-content: center;

            span:first-child {
              margin-top: -0.2em;
              font-size: calc(var(--badge-size) / 7);
              font-weight: 700;
              line-height: 1;
            }

            span:last-child {
              font-family: 'Syne Tactile', cursive;
              font-size: calc(var(--badge-size) / 18);
              font-style: italic;
              line-height: 1;
            }
          }

          @media (min-width: 992px) {
            img {
              animation-play-state: paused;
            }
          }
        }

        .support {
          position: absolute;
          top: calc(var(--badge-size) / 2.5);
          left: 50%;
          transform: translateX(-50%) rotate(0) scale(1);
          z-index: 6;
          width: fit-content;
          padding: 0.2em 0.75em;
          background-color: #fff;
          border: 3px solid #000;
          border-radius: 0.4em;
          text-align: center;
          font-size: calc(var(--badge-size) / 8);
          font-weight: 700;
          transition: all 0.25s ease;
        }
      }
    }
  }
}
</style>
