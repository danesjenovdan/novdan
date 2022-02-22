<template>
  <section class="background-gif columns">
    <div v-if="windowWidth > 1200" class="rotating-circle">
      <img src="~assets/images/krog-moder.svg" alt="" />
    </div>
    <video
      id="bgvidfooter"
      playsinline
      autoplay
      muted
      loop
      poster="~assets/images/gif.png"
    >
      <source src="~assets/video/back_v4.mp4" type="video/mp4" />
    </video>
    <div class="container">
      <div class="row">
        <div class="yellow-column-wrapper">
          <div class="yellow-column">
            <h3>
              Sodeluj pri <br v-if="windowWidth > 1200" />
              spremembi
            </h3>
            <p>
              Pridruži se pilotni izvedbi in pomagaj pri izgradnji spleta, v
              katerem so kakovostne vsebine pravično nagrajene.
            </p>
          </div>
        </div>
        <div class="yellow-column-wrapper">
          <div class="yellow-column">
            <h3>Nov odprtokodni spletni standard</h3>
            <p>
              Obstoječi načini monetizacije spletnih vsebin so problematični in
              nevzdržni. Ustvarjalci se morajo zatekati k oglaševanju in prodaji
              podatkov obiskovalcev, saj boljše rešitve ne obstajajo. WMS je nov
              standard, ki omogoča hiter, varen in učinkovit način za obdelavo
              mikrotransakcij.
            </p>
          </div>
        </div>
        <div class="yellow-column-wrapper">
          <div class="yellow-column">
            <h3>
              Podpiraj medije, <br v-if="windowWidth > 1200" />
              ki jih bereš
            </h3>
            <p>
              Tvoja podpora bo med neodvisne medije razdeljena proporcionalno,
              in sicer glede na količino časa, ki ga porabiš za branje
              posameznega medija.
            </p>
          </div>
        </div>
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
.columns {
  position: relative;
  overflow: visible;
  video {
    object-fit: cover;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    position: absolute;
    z-index: -1;
  }
  .container {
    margin: 2rem 0;
    .row {
      display: block;
    }
    @media (min-width: 992px) {
      margin: 6rem 0;
      .row {
        display: flex;
        align-items: center;
      }
    }
  }
  .rotating-circle {
    width: 12rem;
    position: absolute;
    left: 4rem;
    top: -2rem;
    animation: rotate360 6s linear infinite;
  }
}
.yellow-column-wrapper {
  margin: 1.5rem 30px;
  flex-grow: 1;
  flex-basis: 0;
  @media (min-width: 1200px) {
    margin: 1.5rem;
  }
  .yellow-column {
    background-color: #ffd700;
    border: 1px solid #000000;
    border-radius: 1.25rem;
    padding: 1.5rem;
    h3 {
      text-transform: uppercase;
      font-size: 2rem;
      font-family: 'Le Murmure', serif;
      margin: 0;
    }
    p {
      font-size: 1.25rem;
      margin-top: 0.5rem;
      margin-bottom: 0;
    }
    @media (min-width: 1200px) {
      padding: 2rem;
      h3 {
        font-size: 3.5rem;
      }
      p {
        font-size: 1.75rem;
        margin-bottom: 1.25rem;
      }
    }
  }
}
</style>
