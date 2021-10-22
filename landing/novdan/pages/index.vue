<template>
  <div class="content">
    <Headline />
    <SectionWhat />
    <SectionColumns />
    <SectionMedia />
    <SectionHow />
    <SectionFaq />
    <Footer />
  </div>
</template>

<script>
export default {}
</script>

<style lang="scss">
body {
  margin: 0;
  font-family: 'Syne', sans-serif;
}
section {
  display: flex;
  flex-direction: column;
  align-items: center;
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
.background-gif {
  background-image: url("assets/images/gif.png");
  background-size: cover;
}
.background-white {
  background-color: white;
}
.background-gradient-orange-pink {
  background-image: linear-gradient(-99deg, #ff5ccb 0%, #ffd700 100%);
}
.background-gradient-white-yellow {
  background-image: linear-gradient(to top, rgba(255, 215, 0, 0.4) 0%, rgba(255, 215, 0, 0) 100%);
}
.background-black {
  background-color: black;
}
.background-gradient-pink {
  background-image: linear-gradient(to bottom, rgba(255, 215, 0, 0) 0%, #ff5ccb 100%);
}
.row {
  display: flex;
}

// animations
@keyframes rotate360 {
  to { transform: rotate(360deg); }
}
</style>
