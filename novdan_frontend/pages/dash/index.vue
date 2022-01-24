<template>
  <div>
    <!-- <h1>DASH</h1>
    <div>api base: {{ $config.apiBase }}</div>
    <div>{{ status }}</div>
    <nuxt-link to="/dash/login?logout=true"> Logout </nuxt-link> -->
    <div class="content">
      <video
        id="bgvid"
        playsinline
        autoplay
        muted
        loop
        poster="~assets/images/gif.png"
      >
        <source src="~assets/video/back_v1_1.mp4" type="video/mp4">
      </video>
      <DashHeadline />
      <DashIntro :window-width="windowWidth" />
      <DashSubscription :window-width="windowWidth" :status="status" />
      <Footer :window-width="windowWidth" />
    </div>
  </div>
</template>

<script>
import api from '~/mixins/api.js'

export default {
  mixins: [api],
  data() {
    return {
      status: null,
      windowWidth: 0
    }
  },
  async mounted() {
    if (!this.$api.hasToken()) {
      this.$router.replace('/dash/login')
    }
    this.status = await this.$api.getStatus()

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
  background-image: linear-gradient(to top, rgba(255, 215, 0, 0.4) 0%, white 100%);
}
.background-gradient-yellow-white {
  background-color: white;
  background-image: linear-gradient(to bottom, rgba(255, 215, 0, 0.4) 0%, rgba(255, 215, 0, 0) 67%);
}
.background-black {
  background-color: black;
}
.content-narrow {
  margin: 0 1rem;
  @media (min-width: 992px) {
    margin: 0 8rem;
  }
}
.row {
  display: flex;
}

// animations
@keyframes rotate360 {
  to { transform: rotate(360deg); }
}
</style>
