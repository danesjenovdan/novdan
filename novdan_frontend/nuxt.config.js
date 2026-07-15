const OG_TITLE = "Nov dan – podpiraj neodvisne medijske ustvarjalce";
const OG_DESCRIPTION =
  "Najnovejše objave neodvisnih medijskih ustvarjalcev na enem mestu. Spremljaj, podpiraj in izboljšaj svojo medijsko dieto.";
const OG_IMAGE = "https://novdan.si/nov-dan-og2.jpg";

export default defineNuxtConfig({
  compatibilityDate: "2026-07-15",
  app: {
    head: {
      htmlAttrs: {
        lang: "sl",
      },
      title: OG_TITLE,
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "format-detection", content: "telephone=no" },

        { property: "og:site_name", content: OG_TITLE },
        { property: "og:type", content: "website" },
        { name: "author", content: "Danes je nov dan" },
        { name: "twitter:creator", content: "@danesjenovdan" },
        { name: "twitter:card", content: "summary_large_image" },
        {
          hid: "og-title",
          property: "og:title",
          content: OG_TITLE,
        },
        {
          hid: "twitter-title",
          name: "twitter:title",
          content: OG_TITLE,
        },
        {
          hid: "description",
          name: "description",
          content: OG_DESCRIPTION,
        },
        {
          hid: "og-description",
          property: "og:description",
          content: OG_DESCRIPTION,
        },
        {
          hid: "twitter-description",
          name: "twitter:description",
          content: OG_DESCRIPTION,
        },
        {
          hid: "og-image",
          property: "og:image",
          content: OG_IMAGE,
        },
        {
          hid: "twitter-image",
          name: "twitter:image",
          content: OG_IMAGE,
        },
      ],
      link: [
        { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
        { rel: "alternate icon", href: "/favicon.ico" },
        { rel: "stylesheet", href: "/fonts/selfhosted.css" },
        {
          rel: "alternate",
          type: "application/rss+xml",
          title: "RSS feed",
          href: "https://denarnica.novdan.si/articles/feed/rss/",
        },
        {
          rel: "alternate",
          type: "application/atom+xml",
          title: "Atom feed",
          href: "https://denarnica.novdan.si/articles/feed/atom/",
        },
      ],
      script: [
        {
          src: "https://plausible.lb.djnd.si/js/plausible.js",
          async: true,
          defer: true,
          "data-domain": "novdan.si",
        },
      ],
    },
  },
  css: ["~/assets/main.scss"],
  modules: ["@nuxt/eslint"],
  runtimeConfig: {
    apiBase: process.env.NUXT_API_BASE,
    public: {
      apiClientId: process.env.NUXT_API_CLIENT_ID,
      apiBase: process.env.NUXT_API_BASE_BROWSER || process.env.NUXT_API_BASE,
    },
  },
});
