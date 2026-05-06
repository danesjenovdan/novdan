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
            <!-- <li><a href="/dash/register">Za podpornike</a></li> -->
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
          <div v-if="supporterAmount > 0" class="supporter-amount">
            <span>{{ supporterAmount }}</span> PODPORNIKOV
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
        </div>
      </div>
      <SectionPaymentChooser v-if="showButtons" :medium="medium" :type="paymentType" />
    </div>
  </section>
</template>

<script>
import SectionPaymentChooser from './SectionPaymentChooser.vue'

export default {
  components: {
    SectionPaymentChooser
  },
  props: {
    medium: {
      type: Object,
      required: true
    },
    showButtons: {
      type: Boolean,
      default: true
    },
    supporterAmount: {
      type: Number,
      default: 0
    }
  },
  data() {
    const query = this.$route.query

    return {
      paymentType: query.enkratno === 'true' ? 'one_time' : 'recurring'
    }
  },
  computed: {
    descriptionLines() {
      return this.medium.description.replace(/\r\n/g, '\n').split('\n')
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

    .supporter-amount {
      margin-top: 1rem;
      font-size: 1.125rem;
      font-weight: 700;
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
}
</style>
