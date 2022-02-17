<template>
  <section class="background-gif headline" @mousemove="tiltTiles">
    <div class="container">
      <div class="title">
        <h1>
          n<img class="sun" src="~assets/images/sun.png" alt="sun icon" />v dan
        </h1>
        <p>
          Neposredna podpora <br />
          neodvisnim medijskim ustvarjalcem
        </p>
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

  // @media (min-width: 992px) {
  //   padding: 3rem 0 6rem 0;
  // }

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
    }
    p {
      font-size: 1.25rem;
      line-height: 1;
      font-weight: 700;
      text-align: center;
      margin: 1rem 0;
    }
    @media (min-width: 768px) {
      h1 {
        text-align: right;
        width: 50%;
        padding-right: 1.5rem;
      }
      p {
        text-align: left;
        font-size: 1.5rem;
        width: 50%;
        margin: 0;
      }
    }
  }

  .sun {
    height: 2.5rem;
    width: 2.5rem;
  }
}
</style>
