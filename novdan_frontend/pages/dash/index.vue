<template>
  <div>
    <!-- <h1>DASH</h1>
    <div>api base: {{ $config.apiBase }}</div>
    <div>{{ status }}</div> -->
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
      <SupportHeadline />
      <DashIntro :window-width="windowWidth" :status="status" />
      <DashSubscription :window-width="windowWidth" :status="status" />
      <ArticlesFooter :window-width="windowWidth" />
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
      this.$router.replace('/dash/register')
    }
    try {
      this.status = await this.$api.getStatus()
      console.log(this.status)
    } catch (e) {
      this.$router.replace('/dash/register')
    }

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
hr {
  border: none;
  border-bottom: 2px solid #ffd700;
  margin: 4rem 0;
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
.background-gradient-yellow-white {
  background-color: white;
  background-image: linear-gradient(
    to bottom,
    rgba(255, 215, 0, 0.4) 0%,
    rgba(255, 215, 0, 0) 67%
  );
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
h3 {
  font-size: 3rem;
  font-weight: 400;
  font-family: 'wf-le-murmure', serif;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin-top: 0;
  margin-bottom: 2rem;
}

// animations
@keyframes rotate360 {
  to {
    transform: rotate(360deg);
  }
}
</style>
