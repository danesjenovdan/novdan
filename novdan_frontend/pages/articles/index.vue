<template>
  <div class="content">
    <SectionArticles :articles-by-medium="articlesByMedium" />
    <Footer :window-width="windowWidth" />
  </div>
</template>

<script>
import SectionArticles from '../../components/SectionArticles.vue'
import Footer from '../../components/Footer.vue'

export default {
  components: {
    SectionArticles,
    Footer
  },
  async asyncData({ $axios, $config }) {
    const api = $axios.create({ baseURL: $config.apiBase })
    const articlesByMedium = await api.$get('/articles/latest/')

    return {
      articlesByMedium
    }
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
  font-family: 'Syne', sans-serif;
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
</style>
