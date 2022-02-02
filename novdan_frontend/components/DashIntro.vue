<template>
  <section class="background-white what">
    <div class="container">
      <div class="content-narrow">
        <p class="text-big">
          <span>Pozdravljen_a!</span>
        </p>
        <p class="text-small">
          Tukaj je tvoja nadzorna plošča. V prihodnosti se bo še razvijala in če
          bo projekt uspešen kmalu pridobila nove funkcionalnosti. Če imaš
          kakršno koli vprašanje, pripombe, težave, ali komentarje
          <a href="mailto:novdan@danesjenovdan.si">nam piši</a>.
        </p>
        <div class="yellow-bg" />
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
  padding: 0 1rem;
  @media (min-width: 992px) {
    padding: 0;
  }
  .container {
    position: relative;
  }
  p {
    @media (min-width: 1200px) {
    }
  }
  .text-big {
    font-weight: 500;
    font-size: 1.5rem;
    line-height: 1.75rem;
    margin-top: 4rem;
    margin-bottom: 2rem;
    text-transform: uppercase;
    span {
      font-weight: 800;
    }
    @media (min-width: 992px) {
      font-size: 3rem;
      line-height: 4rem;
      margin-top: 8rem;
    }
  }

  .text-small {
    font-size: 1.5rem;
    line-height: 1.75rem;
    margin: 0 0 4rem 0;
    @media (min-width: 992px) {
      margin: 0 9rem 8rem 9rem;
      font-size: 2rem;
      line-height: 2.5rem;
    }
  }

  .yellow-bg {
    position: absolute;
    left: 50%;
    top: 90%;
    width: 300px;
    height: 300px;
    background-image: radial-gradient(
      circle 150px at center,
      #ffd700 0%,
      rgba(255, 215, 0, 0) 100%
    );
    opacity: 0.4;
    z-index: -1;
    @media (min-width: 1200px) {
      top: 1rem;
      left: 2rem;
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
</style>
