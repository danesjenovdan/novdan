<template>
  <section class="background-white what">
    <div class="container">
      <h1 data-aos="fade-up">
        Kvalitetno novinarstvo <br>NE M<img class="sun" src="~assets/images/sun.png" alt="sun icon">RE<br> biti zastonj!
      </h1>
      <p data-aos="fade-up">
        Nov dan je nova eksperimentalna platforma za podporo neodvisnemu novinarstvu, ki deluje s pomočjo novega odprtega standarda za spletno monetizacijo (web monetization standard - WMS).
      </p>
      <div class="support-wrapper">
        <div class="star">
          <img src="~assets/images/star.png" alt="pink spinning star">
          <div>
            <span>5</span>
            <span>eur/<br>mes</span>
          </div>
        </div>
        <div class="support">
          Podpri
        </div>
        <div class="yellow-bg" />
      </div>
    </div>
    <div class="spinners">
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

<style lang="scss" scoped>
.what {
  height: 64rem;
  position: relative;
  .container {
    position: relative;
  }
  h1 {
    font-weight: 800;
    font-size: 7rem;
    line-height: 0.8;
    margin-top: 8rem;
  }
  p {
    font-size: 1.75rem;
    width: 50%;
    margin-left: 12rem;
  }
  .sun {
    height: 5rem;
    width: 5rem;
  }
}

.support-wrapper {
  position: absolute;
  right: 8rem;
  cursor: pointer;
  transform: rotate(-10deg);
  .star {
    img {
      animation: rotate360 3s linear infinite;  /* animation set */
      animation-play-state: paused;
      height: 10rem;
    }
    position: absolute;
    bottom: 3rem;
    right: 2rem;
    z-index: 2;
    div {
      position: absolute;
      top: 3rem;
      left: 3rem;
      z-index: 2;
      display: flex;
      align-items: flex-end;
      span:first-child {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
      }
      span:last-child {
        font-style: italic;
        display: inline-block;
        font-family: 'Syne Tactile', cursive;
      }
    }
  }
  .support {
    font-size: 3rem;
    font-weight: 700;
    padding: 0.5rem 2rem;
    border: 3px solid #000000;
    border-radius: 1.25rem;
    background-color: white;
    position: relative;
    z-index: 3;
    transition: all 0.25s ease;
    transform:rotate(0) scale(1);
  }
  &:hover {
    .support {
      background-color: #ffd700;
      transform:rotate(0) scale(1.2);

    }
    .star img {
      animation-play-state: running;
    }
  }
  .yellow-bg {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
    width: 622px;
    height: 622px;
    background-image: radial-gradient(circle 311px at center, #ffd700 0%, rgba(255, 215, 0, 0) 100%);
    opacity: 0.4;
    z-index: 1;
  }
}

.spinners {
  width: 64rem;
  transform: translateX(50%) translateY(-50%) rotate(90deg) translateY(50%) translateX(50%);
  position: absolute;
  right: 0;
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
      -moz-animation: spinning-banner 32s linear infinite;
      -webkit-animation: spinning-banner 32s linear infinite;
      animation: spinning-banner 32s linear infinite;
      &:last-child {
        animation-delay: -16s;
      }
    }
  }
  &:nth-of-type(2) {
    background-color: #ffd700;
    color: #ff5ccb;
    .spinning-text {
      -moz-animation: spinning-banner 36s reverse linear infinite;
      -webkit-animation: spinning-banner 36s reverse linear infinite;
      animation: spinning-banner 36s reverse linear infinite;
      &:last-child {
        animation-delay: -18s;
      }
    }
  }
  &:nth-of-type(3) {
    background-color: #ff5ccb;
    color: #1103b1;
    .spinning-text {
      -moz-animation: spinning-banner 22s linear infinite;
      -webkit-animation: spinning-banner 22s linear infinite;
      animation: spinning-banner 22s linear infinite;
      &:last-child {
        animation-delay: -11s;
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
