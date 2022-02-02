<template>
  <section class="background-gif headline" @mousemove="tiltTiles">
    <div class="container">
      <div class="title">
        <h1>
          n<img class="sun" src="~assets/images/sun.png" alt="sun icon" />v dan
        </h1>
        <p>Neposredno podpiraj neodvisne medije!</p>
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

  @media (min-width: 992px) {
    padding: 3rem 0 6rem 0;
  }

  .container:nth-of-type(1) {
    position: relative;
    z-index: 2;
  }

  .title {
    margin: 2rem 0;
    h1 {
      font-weight: 700;
      font-size: 4.5rem;
      line-height: 0.75;
      text-align: center;
      margin: 0;
    }
    p {
      font-size: 1.5rem;
      font-weight: 700;
      text-align: center;
      margin: 0.5rem 0;
    }
    @media (min-width: 1200px) {
      margin: 2rem 0;
      h1 {
        font-size: 12rem;
      }
      p {
        font-size: 2rem;
      }
    }
  }

  .sun {
    height: 2rem;
    width: 2rem;
    @media (min-width: 1200px) {
      height: 6rem;
      width: 6rem;
    }
  }
}
</style>
