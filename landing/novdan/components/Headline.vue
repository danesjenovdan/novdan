<template>
  <section class="background-gif headline" @mousemove="tiltTiles">
    <div class="container">
      <div class="title">
        <h1>n<span style="position: absolute; z-index: -2; display: none">o</span><span style="opacity: 0">o</span>v dan</h1>
        <p>Neposredna podpora neodvisnemu novinarstvu</p>
      </div>
      <div class="plates">
        <div class="plate-wrapper" :style="`transform: rotate(${tilted * 0.5}deg)`">
          <YellowPlate text="Pod Črto" bg="bottom" />
        </div>
        <div class="plate-wrapper" :style="`transform: rotate(${tilted * 0.25}deg)`">
          <YellowPlate text="Oštro" bg="bottom" />
        </div>
        <div class="plate-wrapper" :style="`transform: rotate(${tilted * 0.8}deg)`">
          <YellowPlate text="Boris Vezjak - In Media Res" bg="top" />
        </div>
        <div class="plate-wrapper" :style="`transform: rotate(${tilted * 0.2}deg)`">
          <YellowPlate text="Radio Študent" bg="bottom" />
        </div>
        <div class="plate-wrapper" :style="`transform: rotate(${tilted * 0.4}deg)`">
          <YellowPlate text="Domen Savič - Državljan D" bg="top" />
        </div>
      </div>
    </div>
    <div class="container">
      <div class="circle-animation">
        <div class="sun">
          <img src="~/assets/images/sun.png">
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// import { gsap } from 'gsap'
export default {
  data () {
    return {
      tilted: 0
    }
  },
  methods: {
    tiltTiles (event) {
      const positionX = event.pageX
      const windowWidth = window.innerWidth
      const windowCenter = windowWidth / 2
      const tilted = (windowCenter - positionX) / windowCenter * -45
      this.tilted = tilted / 10
    }
  }
}
</script>

<style scoped lang="scss">
.headline {
  padding: 3rem 0 6rem 0;

  .title {
    margin: 2rem 0;
    h1 {
      font-weight: 700;
      font-size: 12rem;
      line-height: 0.75;
      text-align: center;
      margin: 0;
    }
    p {
      font-size: 2rem;
      font-weight: 700;
      text-align: center;
      margin: 0.5rem 0;
    }
  }

  .plates {
    text-align: center;
    .yellow-plate {
      display: inline-block;
      position: relative;
      background-color: #ffd700;
      border: 1px solid #000000;
      //background-image: url("assets/images/yellow-plate.png");
      //background-size: 100% 100%;
      padding: 0.5rem 1rem 0 1rem;
      text-transform: uppercase;
      font-weight: 700;
      font-size: 4rem;
      margin: 0.5rem 0;
      line-height: 1;
    }
    .plate-wrapper {
      transition: rotate 2s ease-out;
      will-change: transform;
    }
    .plate-wrapper:nth-child(odd) {
      .yellow-plate {
        font-size: 5rem;
        font-family: "Le Murmure", serif;
        padding: 1.5rem 0.75rem 0 0.75rem;
        line-height: 0.75;
      }
    }
  }

  .circle-animation {
    height: 700px;
    width: 700px;
    border: 2px solid black;
    border-radius: 50%;
    position: relative;
  }

  .container:nth-of-type(1) {
    position: relative;
    z-index: 2;
  }

  .container:nth-of-type(2) {
    position: absolute;
    display: flex;
    justify-content: center;
    top: 5rem;
  }
}

.sun {
  display: inline-block;

  /*
   * Make the initial position to be the center of the circle you want this
   * object follow.
   */
  position: absolute;
  left: 300px;
  top: 300px;

  /*
   * Sets up the animation duration, timing-function (or easing)
   * and iteration-count. Ensure you use the appropriate vendor-specific
   * prefixes as well as the official syntax for now. Remember, tools like
   * CSS Please are your friends!
   */
  -webkit-animation: myOrbit 9s ease-in-out infinite; /* Chrome, Safari 5 */
  -moz-animation: myOrbit 9s ease-in-out infinite; /* Firefox 5-15 */
  -o-animation: myOrbit 9s ease-in-out infinite; /* Opera 12+ */
  animation: myOrbit 9s ease-in-out infinite; /* Chrome, Firefox 16+, IE 10+, Safari 5 */
}

/*
 * Set up the keyframes to actually describe the begining and end states of
 * the animation.  The browser will interpolate all the frames between these
 * points.  Again, remember your vendor-specific prefixes for now!
 */
@-webkit-keyframes myOrbit {
  from { -webkit-transform: rotate(0deg) translateX(350px) rotate(0deg); }
  to   { -webkit-transform: rotate(360deg) translateX(350px) rotate(-360deg); }
}

@-moz-keyframes myOrbit {
  from { -moz-transform: rotate(0deg) translateX(350px) rotate(0deg); }
  to   { -moz-transform: rotate(360deg) translateX(350px) rotate(-360deg); }
}

@-o-keyframes myOrbit {
  from { -o-transform: rotate(0deg) translateX(350px) rotate(0deg); }
  to   { -o-transform: rotate(360deg) translateX(350px) rotate(-360deg); }
}

@keyframes myOrbit {
  from { transform: rotate(230deg) translateX(350px) rotate(-230deg); }
  to   { transform: rotate(590deg) translateX(350px) rotate(-590deg); }
}
</style>
