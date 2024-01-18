<template>
  <div class="content">
    <SectionTerms />
    <Footer :window-width="windowWidth" />
  </div>
</template>

<script>
import SectionTerms from '../../components/SectionTerms.vue'
import Footer from '../../components/Footer.vue'

export default {
  components: {
    SectionTerms,
    Footer
  },
  data() {
    return {
      windowWidth: 0
    }
  },
  mounted() {
    this.windowWidth = window.innerWidth
    window.addEventListener('resize', () => {
      this.windowWidth = window.innerWidth
    })
  }
}
</script>

<style lang="scss">
html {
  scroll-behavior: smooth;
}
body {
  margin: 0;
  font-family: 'wf-syne', sans-serif;
}
#bgvid {
  object-fit: cover;
  width: 100vw;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
}
section {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}
.container {
  width: 100%;
  @media (min-width: 576px) {
    max-width: 540px;
  }
  @media (min-width: 768px) {
    max-width: 720px;
  }
  @media (min-width: 992px) {
    max-width: 960px;
  }
  @media (min-width: 1200px) {
    max-width: 1140px;
  }
  @media (min-width: 1400px) {
    max-width: 1320px;
  }
}
.background-white {
  background-color: white;
}
.background-gradient-orange-pink {
  background-image: linear-gradient(-99deg, #ff5ccb 0%, #ffd700 100%);
}
.background-gradient-white-yellow {
  background-color: white;
  background-image: linear-gradient(
    to top,
    rgba(255, 215, 0, 0.4) 0%,
    white 100%
  );
}
.background-black {
  background-color: black;
}
.row {
  display: flex;
}

// animations
@keyframes rotate360 {
  to {
    transform: rotate(360deg);
  }
}
</style>
