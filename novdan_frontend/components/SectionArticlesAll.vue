<template>
  <section class="background-black articles">
    <div class="container">
      <div>
        <h1>Članki</h1>
        <div>
          <div class="article-list">
            <a
              v-for="article in articles.results"
              :key="article.id"
              :href="article.url"
              target="_blank"
              class="article"
            >
              <img
                :src="article.image_url"
                :alt="`Image for ${article.title}`"
              />
              <div class="medium-and-date">
                <small>{{ formatDate(article.published_at) }}</small>
                <p>{{ article.medium.name }}</p>
              </div>
              <h5>{{ article.title }}</h5>
              <hr />
              <p class="line-clamp-4">
                {{ article.description }}
              </p>
            </a>
          </div>
          <div v-if="articles.next" class="more-articles">
            <button type="button" @click="$emit('load-more')">
              <span>Več →</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SectionArticlesAll',
  props: {
    articles: {
      type: Object,
      required: true
    }
  },
  data() {
    return {}
  },
  methods: {
    formatDate(date) {
      return Intl.DateTimeFormat('sl-SI', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(new Date(date))
    }
  }
}
</script>

<style scoped lang="scss">
.articles {
  padding: 3rem 30px;

  @media (min-width: 1200px) {
    padding: 6rem 0;
  }

  h1 {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 2rem;
    margin-bottom: 2rem;
    color: #ff5ccb;

    @media (min-width: 992px) {
      font-size: 6rem;
    }

    @media (min-width: 1200px) {
      font-size: 8rem;
    }
  }

  h4 {
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: 800;
    color: #fff;

    @media (min-width: 992px) {
      font-size: 2rem;
    }

    a {
      color: inherit;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  hr {
    background-color: #ffd700;
    border-color: #ffd700;
    width: 8rem;
    margin: 0;
  }

  .article-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem 1.5rem;
    margin-top: 2rem;

    .article {
      display: block;
      text-decoration: none;
      color: #fff;

      &:hover {
        h5 {
          text-decoration: underline;
        }
      }

      img {
        aspect-ratio: 16/9;
        width: 100%;
        height: auto;
        object-fit: cover;
        background-color: #fff;
        border: 1px solid #ffd700;
        border-radius: 4px;
      }

      small {
        display: block;
        font-size: 0.8rem;
        font-style: italic;
        opacity: 0.8;
        margin-block: 0.5em;
      }

      h5 {
        font-size: 1.2rem;
        font-weight: 800;
        margin-block: 0.75em;
      }

      p {
        font-size: 1rem;
        margin-block: 1em;
      }

      .line-clamp-4 {
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .medium-and-date {
        display: flex;
        align-items: center;
        justify-content: space-between;

        p {
          margin: 0;
        }
      }
    }
  }

  .more-articles {
    margin-top: 2rem;
    text-align: center;

    button {
      background-color: #ffd700;
      border: none;
      border-radius: 4px;
      padding: 0.5rem 2rem;
      font-size: 1.25rem;
      font-weight: 600;
      color: #000;
      cursor: pointer;
      transition: background-color 0.2s ease-in-out;

      &:hover {
        background-color: #ff5ccb;
      }
    }
  }
}
</style>
