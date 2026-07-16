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
          <h2>Pozdravljeni</h2>
          <p>
            Julija 2026 smo na platformi uvedli spremembo donacijskega sistema,
            ki ne bo več temeljil na vtičniku (browser extension) in samodejnem
            prerazporejanju sredstev med medijske projekte.
          </p>
          <p>
            Vaše mesečne donacije s tem prekinjamo in vas vabimo, da avtorje
            podprete neposredno:
          </p>
          <ul>
            <li>
              Oštro:
              <a href="https://ostro.si/donacije/" target="_blank"
                >https://ostro.si/donacije/</a
              >
            </li>
            <li>
              Državljan D:
              <a
                href="https://www.drzavljand.si/kako-podpreti-drzavljan-d/"
                target="_blank"
                >https://www.drzavljand.si/kako-podpreti-drzavljan-d/</a
              >
            </li>
            <li>
              Danes je nov dan:
              <a href="https://danesjenovdan.si/podpri-nas/" target="_blank"
                >https://danesjenovdan.si/podpri-nas/</a
              >
            </li>
          </ul>
          <p>
            Na platformi Nov dan pa lahko trenutno prek novega donacijskega
            sistema podprete projekt Jaše Jenulla – Petkova propagandna
            poročila:
            <NuxtLink to="/ppporocila">https://novdan.si/ppporocila</NuxtLink>.
          </p>
          <p>Ostali avtorji bodo predvidoma sledili v prihodnje.</p>
          <p>
            V imenu avtorjev projektov se vam iz srca zahvaljujemo za podporo,
            ki ste jo namenili v teh letih. Razvoj neodvisnih medijev je
            izjemnega pomena za demokracijo – še posebej v časih, ko se zdi, da
            je ta znova ogrožena.
          </p>
          <p>
            Upamo, da boste projekte in njihove avtorje tako ali drugače podprli
            tudi v prihodnje.
          </p>
          <p>
            Hvala in lep pozdrav,<br />
            Ekipa Danes je nov dan
          </p>
        </div>
      </div>
    </section>
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import SupportHeadline from "../../components/SupportHeadline.vue";
import ArticlesFooter from "../../components/ArticlesFooter.vue";

const windowWidth = ref(0);

function updateWindowWidth() {
  windowWidth.value = window.innerWidth;
}

onMounted(() => {
  updateWindowWidth();
  window.addEventListener("resize", updateWindowWidth);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateWindowWidth);
});
</script>

<style scoped lang="scss">
.main-text {
  padding: 4rem 0;
  color: #fff;

  .main-text-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  h2 {
    font-size: 1.75rem;
  }

  p,
  ul {
    font-size: 1.25rem;
    line-height: 1.5;
  }

  a {
    color: #fff;
    text-decoration: underline;
  }
}
</style>
