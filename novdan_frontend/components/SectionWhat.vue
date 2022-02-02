<template>
  <section class="background-white what">
    <div class="container">
      <h1>
        Kakovostne vsebine <br />NE M<img
          class="sun"
          src="~assets/images/sun.png"
          alt="sun icon"
        />REJO<br />
        biti zastonj!
      </h1>
      <p>
        Nov dan je nova eksperimentalna platforma za podporo neodvisnemu
        novinarstvu, ki deluje s pomočjo novega odprtega standarda za spletno
        monetizacijo (web monetization standard - WMS).
      </p>
      <a href="#how-section" class="support-wrapper">
        <div class="star">
          <img src="~assets/images/star.png" alt="pink spinning star" />
          <div>
            <span>5</span>
            <span>eur/<br />mes</span>
          </div>
        </div>
        <div class="support">Podpri</div>
        <div class="yellow-bg" />
      </a>
    </div>
    <div v-if="windowWidth > 1400" class="spinners">
      <div class="spinning-banner">
        <SpinningBanner class="spinning-text" />
        <SpinningBanner class="spinning-text" />
      </div>
      <div class="spinning-banner">
        <SpinningBanner class="spinning-text" />
        <SpinningBanner class="spinning-text" />
      </div>
      <div class="spinning-banner">
        <SpinningBanner class="spinning-text" />
        <SpinningBanner class="spinning-text" />
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    windowWidth: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style lang="scss" scoped>
.what {
  position: relative;
  overflow: hidden;
  padding: 0 30px;
  @media (min-width: 1200px) {
    padding: 0;
  }
  .container {
    position: relative;
  }
  @media (min-width: 1200px) {
    min-height: 60rem;
  }
  h1 {
    font-weight: 800;
    font-size: 2.25rem;
    line-height: 0.8;
    margin-top: 4rem;
    margin-bottom: 3rem;
    @media (min-width: 992px) {
      font-size: 4.5rem;
      margin-top: 4rem;
    }
    @media (min-width: 1200px) {
      font-size: 7rem;
      margin-top: 8rem;
    }
  }
  p {
    font-size: 1.5rem;
    @media (min-width: 1200px) {
      width: 50%;
      margin-left: 12rem;
      font-size: 1.75rem;
    }
  }
  .sun {
    height: 2rem;
    width: 2rem;
    @media (min-width: 1200px) {
      height: 5rem;
      width: 5rem;
    }
  }
}

.support-wrapper {
  cursor: pointer;
  display: flex;
  align-items: center;
  margin: 3rem 0;
  text-decoration: none;
  color: black;
  @media (min-width: 1200px) {
    position: absolute;
    right: 8rem;
    transform: rotate(-10deg);
    margin: 0;
  }
  .star {
    position: absolute;
    z-index: 5;
    right: -3rem;
    img {
      animation: rotate360 3s linear infinite; /* animation set */
      height: 9rem;
    }
    div {
      position: absolute;
      top: 2.75rem;
      left: 2.5rem;
      z-index: 2;
      display: flex;
      align-items: flex-end;
      span:first-child {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
      }
      span:last-child {
        font-size: 1rem;
        font-style: italic;
        display: inline-block;
        font-family: 'Syne Tactile', cursive;
      }
    }
    @media (min-width: 1200px) {
      bottom: 3rem;
      right: 2rem;
      img {
        height: 10rem;
        animation-play-state: paused;
      }
      div {
        top: 3rem;
        left: 3rem;
      }
    }
  }
  .support {
    font-size: 2rem;
    font-weight: 700;
    padding: 0.5rem;
    width: 100%;
    text-align: center;
    border: 3px solid #000000;
    border-radius: 1.25rem;
    background-color: white;
    position: relative;
    z-index: 2;
    @media (min-width: 1200px) {
      text-align: start;
      width: unset;
      transition: all 0.25s ease;
      transform: rotate(0) scale(1);
      padding: 0.5rem 2rem;
      font-size: 3rem;
      z-index: 6;
    }
  }
  &:hover {
    .support {
      background-color: #ffd700;
      @media (min-width: 1200px) {
        transform: rotate(0) scale(1.2);
      }
    }
    .star img {
      animation-play-state: running;
    }
  }
  .yellow-bg {
    position: absolute;
    left: 50%;
    top: 90%;
    transform: translateX(-50%) translateY(-50%);
    width: 300px;
    height: 300px;
    background-image: radial-gradient(
      circle 150px at center,
      #ffd700 0%,
      rgba(255, 215, 0, 0) 100%
    );
    opacity: 0.4;
    z-index: 1;
    @media (min-width: 1200px) {
      top: 50%;
      width: 622px;
      height: 622px;
      background-image: radial-gradient(
        circle 311px at center,
        #ffd700 0%,
        rgba(255, 215, 0, 0) 100%
      );
    }
  }
}

.spinners {
  width: 100%;
  transform: rotate(60deg);
  position: absolute;
  right: -40%;
  top: 50%;
  @media (min-width: 1400px) {
    right: -50%;
  }
  @media (min-width: 1600px) {
    right: -40%;
  }
}
.spinning-banner {
  width: 100%;
  height: 3rem;
  padding: 0.25rem 0;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  .spinning-text {
    white-space: nowrap;
    display: flex;
    align-items: center;
    position: absolute;
    font-size: 1.25rem;
    h2 {
      margin: 0;
    }
    &:last-child {
      transform: translateX(100%);
    }
  }
  &:nth-of-type(1) {
    background-color: #1103b1;
    color: #ffd700;
    .spinning-text {
      -moz-animation: spinning-banner 36s linear infinite;
      -webkit-animation: spinning-banner 36s linear infinite;
      animation: spinning-banner 36s linear infinite;
      &:last-child {
        animation-delay: -18s;
      }
    }
  }
  &:nth-of-type(2) {
    background-color: #ffd700;
    color: #ff5ccb;
    .spinning-text {
      -moz-animation: spinning-banner 42s reverse linear infinite;
      -webkit-animation: spinning-banner 42s reverse linear infinite;
      animation: spinning-banner 42s reverse linear infinite;
      &:last-child {
        animation-delay: -21s;
      }
    }
  }
  &:nth-of-type(3) {
    background-color: #ff5ccb;
    color: #1103b1;
    .spinning-text {
      -moz-animation: spinning-banner 32s linear infinite;
      -webkit-animation: spinning-banner 32s linear infinite;
      animation: spinning-banner 32s linear infinite;
      &:last-child {
        animation-delay: -16s;
      }
    }
  }
}

/* Move it (define the animation) */
@-moz-keyframes spinning-banner {
  0% {
    -moz-transform: translateX(100%);
  }
  100% {
    -moz-transform: translateX(-100%);
  }
}
@-webkit-keyframes spinning-banner {
  0% {
    -webkit-transform: translateX(100%);
  }
  100% {
    -webkit-transform: translateX(-100%);
  }
}
@keyframes spinning-banner {
  0% {
    -moz-transform: translateX(100%); /* Firefox bug fix */
    -webkit-transform: translateX(100%); /* Firefox bug fix */
    transform: translateX(100%);
  }
  100% {
    -moz-transform: translateX(-100%); /* Firefox bug fix */
    -webkit-transform: translateX(-100%); /* Firefox bug fix */
    transform: translateX(-100%);
  }
}
</style>
