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
    <SupportHeadline />
    <section class="background-black main-text">
      <div class="container">
        <div class="main-text-wrapper">
          <h2>Se želite pridružiti kot medij?</h2>
          <p>
            Platforma Nov dan zbira vsebine kakovostnih in kredibilnih medijskih
            ustvarjalcev, ki javnost informirajo o širših družbenopolitičnih
            temah in problematikah.
          </p>
          <p>
            Izbrani mediji in medijski ustvarjalci delujejo neodvisno in
            objektivno.
          </p>
          <p>K sodelovanju vabimo vse ki se v tem opisu prepoznate.</p>
          <p>
            <a href="mailto:novdan@djnd.si" class="btn contact-us">
              Pišite sem.
              <!-- <br><small>novdan@djnd.si</small> -->
            </a>
          </p>
        </div>
      </div>
    </section>
    <SectionMedia2 />
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script>
export default {
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

<style lang="scss" scoped>
.main-text {
  padding: 4rem 0;
  color: #fff;
  text-align: center;

  .main-text-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  h2 {
    font-size: 1.75rem;
  }

  p {
    font-size: 1.25rem;
  }

  .btn.contact-us {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.75em 2em;
    background: #fff;
    border: 3px solid #000;
    border-radius: 0.5em;
    text-decoration: none;
    color: #000;
    font-size: 1.25rem;
    line-height: 1;
    transition: all 0.25s ease;

    &:hover {
      background-color: #ffd700;

      @media (min-width: 992px) {
        transform: scale(1.2);
      }
    }

    small {
      font-size: 0.75em;
    }
  }
}
</style>

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
