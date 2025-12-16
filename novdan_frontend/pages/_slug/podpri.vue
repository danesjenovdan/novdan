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
    <ArticleHeadlineMedium :medium="medium" :show-buttons="false" />
    <SectionPaymentEmbed :campaign-slug="medium.donation_campaign_slug" :type="paymentType" />
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script>
import ArticleHeadlineMedium from '../../components/ArticleHeadlineMedium.vue'
import SectionPaymentEmbed from '../../components/SectionPaymentEmbed.vue'
import ArticlesFooter from '../../components/ArticlesFooter.vue'

export default {
  components: {
    ArticleHeadlineMedium,
    SectionPaymentEmbed,
    ArticlesFooter
  },
  async asyncData({ $axios, $config, params, query, error }) {
    const api = $axios.create({ baseURL: $config.apiBase })
    let medium = null
    try {
      medium = await api.$get(`/articles/medium/${encodeURIComponent(params.slug)}/`)
    } catch (e) {
      return error({ statusCode: 404, message: 'Medium not found' })
    }
    if (!medium || !medium.donation_campaign_slug) {
      return error({ statusCode: 404, message: 'Medium not found' })
    }

    return {
      medium,
      paymentType: query.enkratno === 'true' ? 'one_time' : 'recurring'
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
