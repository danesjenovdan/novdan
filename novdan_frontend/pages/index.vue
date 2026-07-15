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
    <ArticleHeadline />
    <SectionArticlesAll :articles="articles" @load-more="onLoadMore" />
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import ArticleHeadline from "../components/ArticleHeadline.vue";
import SectionArticlesAll from "../components/SectionArticlesAll.vue";
import ArticlesFooter from "../components/ArticlesFooter.vue";

const config = useRuntimeConfig();
const apiBase = config.public?.apiBase || config.apiBase;
const windowWidth = ref(0);

const { data: initialArticles } = await useFetch("/articles/", {
  baseURL: apiBase,
});

const articles = ref(initialArticles.value);

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

async function onLoadMore() {
  if (!articles.value?.next) {
    return;
  }

  const url = new URL(articles.value.next, apiBase);
  const nextArticles = await $fetch(url.toString());

  articles.value = {
    ...nextArticles,
    results: articles.value.results.concat(nextArticles.results),
  };
}
</script>
