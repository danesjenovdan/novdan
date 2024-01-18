<template>
  <div class="content">
    <video
      id="bgvid"
      playsinline
      autoplay
      muted
      loop
      poster="~assets/images/gif.png"
    >
      <source src="~assets/video/back_v1_1.mp4" type="video/mp4" />
    </video>
    <ArticleHeadline />
    <ArticleStickyBadge />
    <SectionArticlesAll :articles="articles" @load-more="onLoadMore" />
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script>
import ArticleStickyBadge from '../../components/ArticleStickyBadge.vue'
import ArticleHeadline from '../../components/ArticleHeadline.vue'
import SectionArticlesAll from '../../components/SectionArticlesAll.vue'
import ArticlesFooter from '../../components/ArticlesFooter.vue'

export default {
  components: {
    ArticleStickyBadge,
    ArticleHeadline,
    SectionArticlesAll,
    ArticlesFooter
  },
  async asyncData({ $axios, $config }) {
    const api = $axios.create({ baseURL: $config.apiBase })
    const articles = await api.$get('/articles/')

    return {
      articles
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
  },
  methods: {
    async onLoadMore() {
      const api = this.$axios.create({ baseURL: this.$config.apiBase })

      if (this.articles.next) {
        const { pathname, search } = new URL(this.articles.next)
        const articles = await api.$get(`${pathname}${search}`)

        this.articles = {
          ...articles,
          results: this.articles.results.concat(articles.results)
        }
      }
    }
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
