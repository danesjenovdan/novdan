<template>
  <section class="background-gif headline" @mousemove="tiltTiles">
    <div class="container">
      <div class="title">
        <h1>
          n<span style="position: absolute; z-index: -2; display: none">o</span
          ><span style="opacity: 0">o</span>v dan
        </h1>
        <p>Neposredna podpora neodvisnemu novinarstvu</p>
      </div>
      <div class="plates">
        <div
          class="plate-wrapper"
          :style="`transform: rotate(${tilted * 0.5}deg)`"
        >
          <YellowPlate text="Agrument" bg="bottom" />
        </div>
        <div
          class="plate-wrapper"
          :style="`transform: rotate(${tilted * 0.25}deg)`"
        >
          <YellowPlate text="Oštro" bg="bottom" />
        </div>
        <div
          class="plate-wrapper"
          :style="`transform: rotate(${tilted * 0.8}deg)`"
        >
          <YellowPlate text="Boris Vezjak - In Media Res" bg="top" />
        </div>
        <div
          class="plate-wrapper"
          :style="`transform: rotate(${tilted * 0.2}deg)`"
        >
          <YellowPlate text="Mešanec.si" bg="bottom" />
        </div>
        <div
          class="plate-wrapper"
          :style="`transform: rotate(${tilted * 0.4}deg)`"
        >
          <YellowPlate text="Domen Savič - Državljan D" bg="top" />
        </div>
      </div>
    </div>
    <div class="container">
      <div class="circle-animation">
        <div class="sun">
          <img src="~/assets/images/sun.png" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// import { gsap } from 'gsap'
export default {
  data() {
    return {
      tilted: 0
    }
  },
  methods: {
    tiltTiles(event) {
      const positionX = event.pageX
      const windowWidth = window.innerWidth
      const windowCenter = windowWidth / 2
      const tilted = ((windowCenter - positionX) / windowCenter) * -45
      this.tilted = tilted / 10
    }
  }
}
</script>

<style scoped lang="scss">
.headline {
  padding: 3rem 0 8rem 0;
  overflow-x: hidden;
  overflow-y: visible;

  @media (min-width: 1200px) {
    padding: 3rem 0 6rem 0;
  }

  .container:nth-of-type(1) {
    position: relative;
    z-index: 2;
  }

  .title {
    margin: 2rem 0;
    h1 {
      font-weight: 700;
      font-size: 4.5rem;
      line-height: 0.75;
      text-align: center;
      margin: 0;
    }
    p {
      font-size: 1.5rem;
      font-weight: 700;
      text-align: center;
      margin: 0.5rem 0;
    }
    @media (min-width: 1200px) {
      margin: 2rem 0;
      h1 {
        font-size: 12rem;
      }
      p {
        font-size: 2rem;
      }
    }
  }

  .plates {
    text-align: center;
    .plate-wrapper {
      will-change: transform;
      .yellow-plate {
        display: inline-block;
        position: relative;
        background-color: #ffd700;
        border: 1px solid #000000;
        padding: 0.5rem 1rem 0 1rem;
        text-transform: uppercase;
        font-weight: 700;
        font-size: 2rem;
        margin: 0.5rem 0;
        line-height: 1;
      }
      &:nth-child(odd) {
        .yellow-plate {
          font-size: 2rem;
          font-family: 'Le Murmure', serif;
          padding: 1rem 0.75rem 0 0.75rem;
          line-height: 0.75;
        }
      }
    }
    @media (min-width: 992px) {
      .plate-wrapper {
        .yellow-plate {
          padding: 0.5rem 1rem 0 1rem;
          font-size: 3rem;
        }
        &:nth-child(odd) {
          .yellow-plate {
            font-size: 3.5rem;
            padding: 1.5rem 0.75rem 0 0.75rem;
          }
        }
      }
    }
    @media (min-width: 1200px) {
      .plate-wrapper {
        .yellow-plate {
          padding: 0.5rem 1rem 0 1rem;
          font-size: 4rem;
        }
        &:nth-child(odd) {
          .yellow-plate {
            font-size: 5rem;
            padding: 1.5rem 0.75rem 0 0.75rem;
          }
        }
      }
    }
  }

  .container:nth-of-type(2) {
    position: absolute;
    display: flex;
    justify-content: center;
    top: 6rem;
    width: unset;
    @media (min-width: 1400px) {
      width: 100%;
      top: 5rem;
    }
  }

  .circle-animation {
    height: 500px;
    width: 500px;
    border: 2px solid black;
    border-radius: 50%;
    position: relative;
    @media (min-width: 1200px) {
      height: 700px;
      width: 700px;
    }
    .sun {
      /*
       * Make the initial position to be the center of the circle you want this
       * object follow.
       */
      position: absolute;
      left: 225px;
      top: 225px;
      display: inline-block;
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
      img {
        width: 50px;
      }
      @media (min-width: 1200px) {
        left: 300px;
        top: 300px;
        img {
          width: 100px;
        }
      }
    }
  }
}

/*
 * Set up the keyframes to actually describe the begining and end states of
 * the animation.  The browser will interpolate all the frames between these
 * points.  Again, remember your vendor-specific prefixes for now!
 */
@-webkit-keyframes myOrbit {
  from {
    -webkit-transform: rotate(0deg) translateX(250px) rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg) translateX(250px) rotate(-360deg);
  }
}

@-moz-keyframes myOrbit {
  from {
    -moz-transform: rotate(0deg) translateX(250px) rotate(0deg);
  }
  to {
    -moz-transform: rotate(360deg) translateX(250px) rotate(-360deg);
  }
}

@-o-keyframes myOrbit {
  from {
    -o-transform: rotate(0deg) translateX(250px) rotate(0deg);
  }
  to {
    -o-transform: rotate(360deg) translateX(250px) rotate(-360deg);
  }
}

@keyframes myOrbit {
  from {
    transform: rotate(250deg) translateX(250px) rotate(-250deg);
  }
  to {
    transform: rotate(610deg) translateX(250px) rotate(-610deg);
  }
}

@media (min-width: 1200px) {
  @-webkit-keyframes myOrbit {
    from {
      -webkit-transform: rotate(0deg) translateX(350px) rotate(0deg);
    }
    to {
      -webkit-transform: rotate(360deg) translateX(350px) rotate(-360deg);
    }
  }

  @-moz-keyframes myOrbit {
    from {
      -moz-transform: rotate(0deg) translateX(350px) rotate(0deg);
    }
    to {
      -moz-transform: rotate(360deg) translateX(350px) rotate(-360deg);
    }
  }

  @-o-keyframes myOrbit {
    from {
      -o-transform: rotate(0deg) translateX(350px) rotate(0deg);
    }
    to {
      -o-transform: rotate(360deg) translateX(350px) rotate(-360deg);
    }
  }

  @keyframes myOrbit {
    from {
      transform: rotate(230deg) translateX(350px) rotate(-230deg);
    }
    to {
      transform: rotate(590deg) translateX(350px) rotate(-590deg);
    }
  }
}
</style>
