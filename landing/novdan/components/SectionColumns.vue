<template>
  <section class="background-gif columns">
    <div class="container">
      <div class="row">
        <div class="yellow-column">
          <h3>
            Podpiraj medije, <br> ki jih bereš
          </h3>
          <p>
            Tvoja podpora bo med neodvisne medije razdeljena proporcionalno, glede na količino časa, ki si ga porabil_a za branje posameznega medija.
          </p>
        </div>
        <div class="yellow-column">
          <h3>
            Nov odprtokodni spletni standard
          </h3>
          <p>
            Obstoječi načini monetizacije spletnih vsebin so problematični in nevzdržni. Ustvarjalci vsebin se morajo zatekati k oglaševanju in prodaji podatkov svojih obiskovalcev, ker boljše rešitve ne obstajajo. WMS je nov standard, ki omogoča hiter, varen in učinkovit način za obdelavo mikotransakcij.
          </p>
        </div>
        <div class="yellow-column">
          <h3>
            Sodeluj pri <br> spremembi
          </h3>
          <p>
            Pridruži se pilotskemu projektu in pomagaj pri izgradnji spleta, v katerem je kvalitetna vsebina pravično nagrajena.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.columns {
  .container {
    margin: 6rem 0;
  }
}
.yellow-column {
  background-color: #ffd700;
  border: 1px solid #000000;
  border-radius: 1.25rem;
  padding: 2rem;
  margin: 1.5rem;
  flex-grow: 1;
  flex-basis: 0;
  h3 {
    text-transform: uppercase;
    font-size: 3.5rem;
    font-family: "Le Murmure", serif;
    margin: 0;
  }
  p {
    font-size: 1.75rem;
    margin-top: 0.5rem;
  }
}
</style>
