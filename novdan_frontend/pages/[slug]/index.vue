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
    <ArticleHeadlineMedium
      :medium="medium"
      :supporter-amount="supporterAmount"
    />
    <SectionArticlesAll :articles="articles" @load-more="onLoadMore" />
    <ArticlesFooter :window-width="windowWidth" />
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import ArticleHeadlineMedium from "../../components/ArticleHeadlineMedium.vue";
import SectionArticlesAll from "../../components/SectionArticlesAll.vue";
import ArticlesFooter from "../../components/ArticlesFooter.vue";

const config = useRuntimeConfig();
const apiBase = config.public?.apiBase || config.apiBase;
const route = useRoute();
const windowWidth = ref(0);

const slug = encodeURIComponent(String(route.params.slug || ""));

const { data: medium, error: mediumError } = await useFetch(
  `/articles/medium/${slug}/`,
  {
    baseURL: apiBase,
  },
);

const { data: initialArticles, error: articlesError } = await useFetch(
  "/articles/",
  {
    baseURL: apiBase,
    query: {
      medium__slug: route.params.slug,
    },
  },
);

if (
  mediumError.value ||
  articlesError.value ||
  !medium.value ||
  !medium.value.donation_campaign_slug
) {
  throw createError({ statusCode: 404, message: "Medium not found" });
}

const articles = ref(initialArticles.value);

const supporterAmount = ref(0);
try {
  const podpriData = await $fetch(
    `https://podpri.djnd.si/api/donation-campaign/${medium.value.donation_campaign_slug}/`,
  );
  supporterAmount.value = podpriData?.active_monthly_subscriptions || 0;
} catch {
  // ignore errors
}

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
