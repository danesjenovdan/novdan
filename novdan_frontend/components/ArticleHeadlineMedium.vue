<template>
  <section class="background-gif headline">
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
        <div class="tile">
          <div class="tile-with-bg">
            <img class="tile-bg" src="~assets/images/tile-bg.svg" alt="" />
            <img class="tile-icon" :src="medium.icon_url" alt="" />
          </div>
        </div>
        <div class="description">
          <div class="name">
            {{ medium.name }}
          </div>
          <p v-for="line in descriptionLines" :key="line">
            {{ line }}
          </p>
          <div v-for="link in medium.description_links" :key="link.url" class="link">
            <a :href="link.url" target="_blank">{{ link.url }}</a><br />
          </div>
          <!-- <p><strong>XX Podpornikov</strong></p> -->
        </div>
      </div>
      <div v-if="showButtons" class="donate-buttons">
        <a class="button" @click.prevent="$router.push(`/${medium.slug}/podpri-izbira`)">
          <div class="support">Postani podpornik</div>
          <div class="star">
            <img src="~assets/images/star.png" alt="pink spinning star" />
          </div>
        </a>
        <a class="button" @click.prevent="$router.push(`/${medium.slug}/podpri-izbira?enkratno=true`)">
          <div class="support">Doniraj enkratno</div>
          <div class="star">
            <img src="~assets/images/star.png" alt="pink spinning star" />
          </div>
        </a>
        <a class="link" href="#" @click.prevent="cancelSupport">Prekini podporo</a>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    medium: {
      type: Object,
      required: true
    },
    showButtons: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {}
  },
  computed: {
    descriptionLines() {
      return this.medium.description.replace(/\r\n/g, '\n').split('\n')
    }
  },
  methods: {
    cancelSupport() {
      prompt('Prosimo kontaktirajte nas na e-naslovu:', 'novdan@djnd.si')
    }
  }
}
</script>

<style scoped lang="scss">
.headline {
  padding: 1rem;
  padding-bottom: 0;

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

    .tile {
      .tile-with-bg {
        display: grid;
        place-items: center;
        width: 150px;
        height: 150px;
        margin-bottom: 1.5rem;

        @media (min-width: 576px) {
          width: 200px;
          height: 200px;
        }

        @media (min-width: 992px) {
          margin-right: 2rem;
          margin-bottom: 0;
        }

        img {
          grid-area: 1 / 1;
          width: 100%;
          height: 100%;
          object-fit: contain;

          &.tile-bg {
            z-index: 1;
          }

          &.tile-icon {
            z-index: 2;
            width: 88%;
            height: 88%;
            margin-top: 4%;
            margin-right: 4%;
          }
        }
      }
    }

    .description {
      flex: 1;

      @media (min-width: 992px) {
        margin-right: 2rem;
      }

      .name {
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 1rem;
      }

      p {
        font-size: 1.25rem;
        margin: 0;
      }

      p + p {
        margin-top: 1.25rem;
      }

      p + div.link {
        margin-top: 1.25rem;
      }

      a {
        color: inherit;
        text-decoration: underline;
      }
    }
  }

  .donate-buttons {
    display: flex;
    gap: 5rem;
    margin-top: 5rem;
    margin-bottom: 4rem;

    @media (max-width: 767px) {
      flex-direction: column;
      gap: 2rem;
    }

    @keyframes rotate360 {
      to {
        transform: rotate(360deg);
      }
    }

    .link {
      margin-left: auto;
      align-self: flex-end;
      color: inherit;
    }

    .button {
      text-decoration: none;
      color: black;
      position: relative;
      display: inline-flex;
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
        @media (max-width: 767px) {
          width: calc(100% - 12rem);
        }
        @media (min-width: 1200px) {
          font-size: 1.75rem;
        }
      }
      .star {
        position: absolute;
        z-index: 3;
        right: -4rem;
        @media (max-width: 767px) {
          right: 1rem;
        }
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
  }
}
</style>
