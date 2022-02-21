<template>
  <section class="background-white what">
    <div class="container">
      <div class="content-narrow">
        <p class="text-big">
          <span>ZDRAVO!</span>
        </p>
        <p class="text-small">
          Tukaj je tvoja nadzorna plošča. V prihodnosti se bo še razvijala, če
          bo projekt uspešen, pa bo kmalu pridobila tudi nove funkcionalnosti.
          Če imaš kakršno koli vprašanje, pripombe, težave ali komentarje,
          <a href="mailto:novdan@danesjenovdan.si" target="_blank">nam piši</a>.
        </p>
        <div class="yellow-bg" />
        <hr v-if="isSubscribed" />
        <div class="row">
          <div v-if="isSubscribed" style="position: relative">
            <h3>Tvoja razporeditev</h3>
            <p class="text-stats">
              Ta mesec si medijem prispeval_a
              <span>{{ status.monetized_time }} sekund</span> svoje pozornosti.
            </p>
            <div class="graph">
              <div class="legend">
                <div v-for="medium in media_with_colors" :key="medium.user.username" class="legend-item">
                  <span class="legend-ring" :style="{'backgroundColor': medium.color}"></span>
                  {{ medium.user.full_name }}
                </div>
              </div>
              <pie-chart
                :section-data="media_with_colors"
                :colors="colors"
                class="pie-chart"
              ></pie-chart>
            </div>
            <div class="pink-bg" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import PieChart from './PieChart.vue'

export default {
  components: { PieChart },
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
      colors: [
        '#d74dc7',
        '#ff946f',
        '#ffb537',
        '#ffcc12',
        '#ff7e94'
      ]
    }
  },
  computed: {
    isSubscribed() {
      if (this.status && this.status.active_subscription) {
        return true
      }
      return false
    },
    media_with_colors() {
      if (this.isSubscribed) {
        const media = []
        for (let i = 0; i < this.status.monetized_split.length; i++) {
          media.push({
            ...this.status.monetized_split[i],
            color: this.colors[i]
          })
        }
        return media
      }
      return []
    }
  }
}
</script>

<style lang="scss" scoped>
.what {
  position: relative;
  overflow: hidden;
  padding: 0 1rem;
  @media (min-width: 992px) {
    padding: 0;
  }

  .container {
    position: relative;
  }

  // h3 {
  //   font-size: 3rem;
  //   font-weight: 400;
  //   font-family: 'Le Murmure';
  //   text-transform: uppercase;
  //   letter-spacing: 3px;
  //   margin-top: 0;
  //   margin-bottom: 2rem;
  // }

  p {
    @media (min-width: 1200px) {
    }
  }

  hr {
    margin-bottom: 8rem;
  }

  .text-stats {
    font-size: 1.5rem;
    line-height: 1.75rem;
    span {
      font-weight: 800;
    }
    @media (min-width: 992px) {
      margin: 1rem 0 2rem 0;
      font-size: 2rem;
      line-height: 2.5rem;
    }
    @media (min-width: 1200px) {
      margin: 1rem 9rem 2rem 9rem;
    }
  }

  .graph {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-bottom: 4rem;
    @media (min-width: 992px) {
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
      font-size: 2rem;
      line-height: 2.5rem;
    }
    @media (min-width: 1200px) {
      margin: 1rem 9rem 4rem 9rem;
    }
  }

  .legend-item {
    font-family: "Syne Tactile", cursive;
    color: #1103b1;
    font-size: 32px;
    display: flex;
    align-items: center;
    margin: 20px 0;
    .legend-ring {
      min-height: 30px;
      min-width: 30px;
      border: 3px #1103b1 solid;
      border-radius: 50%;
      display: inline-block;
      margin-right: 15px;
    }
  }

  .pie-chart {
    height: 280px;
    // margin-right: 10rem;
  }

  .text-big {
    font-weight: 500;
    font-size: 1rem;
    line-height: 1.75rem;
    margin-top: 4rem;
    margin-bottom: 2rem;
    text-transform: uppercase;
    span {
      font-weight: 800;
    }
    @media (min-width: 992px) {
      font-size: 3rem;
      line-height: 4rem;
      margin-top: 8rem;
    }
  }

  .text-small {
    font-size: 1.5rem;
    line-height: 1.75rem;
    margin: 0 0 4rem 0;
    @media (min-width: 992px) {
      margin: 0 0 8rem 0;
      font-size: 2rem;
      line-height: 2.5rem;
    }
    @media (min-width: 1200px) {
      margin: 1rem 9rem 4rem 9rem;
    }
  }

  .yellow-bg {
    position: absolute;
    left: 50%;
    top: 90%;
    width: 300px;
    height: 300px;
    background-image: radial-gradient(
      circle 150px at center,
      #ffd700 0%,
      rgba(255, 215, 0, 0) 100%
    );
    opacity: 0.4;
    z-index: -1;
    @media (min-width: 1200px) {
      top: 0rem;
      left: 4rem;
      width: 400px;
      height: 400px;
      background-image: radial-gradient(
        circle 200px at center,
        #ffd700 0%,
        rgba(255, 215, 0, 0) 100%
      );
    }
  }

  .pink-bg {
    position: absolute;
    left: 0;
    top: 0;
    width: 300px;
    height: 300px;
    background-image: radial-gradient(
      circle 150px at center,
      #ff5ccb 0%,
      rgba(255, 92, 203, 0) 100%
    );
    opacity: 0.4;
    z-index: -1;
    @media (min-width: 768px) {
      top: -10%;
      left: 40%;
    }
    @media (min-width: 992px) {
      top: -8rem;
      width: 500px;
      height: 500px;
      background-image: radial-gradient(
        circle 250px at center,
        #ff5ccb 0%,
        rgba(255, 92, 203, 0) 100%
      );
    }
  }
}
</style>
