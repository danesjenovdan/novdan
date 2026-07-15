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
          <p>K sodelovanju vabimo vse, ki se v tem opisu prepoznate.</p>
          <p>
            <a href="mailto:novdan@danesjenovdan.si" class="btn contact-us">
              Pišite nam
            </a>
          </p>
        </div>
      </div>
    </section>
    <SectionMedia2 />
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

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
