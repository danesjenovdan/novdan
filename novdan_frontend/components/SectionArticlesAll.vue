<template>
  <section class="background-black articles">
    <div class="container">
      <div>
        <div class="preamble">
          <div class="description">
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Optio
              amet harum obcaecati hic perspiciatis, voluptatem ut. Commodi esse
              nostrum vitae quo deserunt vel molestiae nobis explicabo, fugit
              nihil ut expedita.
            </p>
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Optio
              amet harum obcaecati hic perspiciatis, voluptatem ut.
            </p>
          </div>
          <div class="badge">
            <a href="#" class="support-wrapper">
              <div class="star">
                <img src="~assets/images/star.png" alt="pink spinning star" />
                <div>
                  <span>5</span>
                  <span>eur/<br />mes</span>
                </div>
              </div>
              <div class="support">Podpri</div>
              <div class="yellow-bg" />
            </a>
          </div>
        </div>
        <div>
          <div
            v-for="(dayArticles, date) in articlesByDate"
            :key="date"
            class="date-articles"
          >
            <div class="date-line">
              <span class="date">{{ formatLongDate(date) }}</span>
              <hr />
            </div>
            <div class="article-list">
              <a
                v-for="article in dayArticles"
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
  computed: {
    articlesByDate() {
      return this.articles.results.reduce((acc, article) => {
        const date = new Date(article.published_at).toISOString().split('T')[0]
        acc[date] = acc[date] || []
        acc[date].push(article)
        return acc
      }, {})
    }
  },
  methods: {
    formatDate(date) {
      return Intl.DateTimeFormat('sl-SI', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(new Date(date))
    },
    formatLongDate(date) {
      return Intl.DateTimeFormat('sl-SI', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      }).format(new Date(date))
    }
  }
}
</script>

<style scoped lang="scss">
.articles {
  padding: 2rem 30px;

  @media (min-width: 1200px) {
    padding-inline: 0;
  }

  .preamble {
    display: flex;
    flex-direction: column;

    @media (min-width: 992px) {
      flex-direction: row;
    }

    .description {
      flex: 1;
      color: #fff;

      @media (min-width: 992px) {
        margin-right: 2rem;
      }

      p {
        font-size: 1rem;
        margin: 0;
      }

      p + p {
        margin-top: 1.25rem;
      }
    }

    .badge {
      --badge-size: 180px;

      // flex: 0 0 0%;
      margin-top: 1.5rem;
      width: var(--badge-size);
      height: calc(var(--badge-size) / 1.5);
      position: relative;

      @media (min-width: 992px) {
        margin-top: -1rem;
        margin-bottom: -0.75rem;
      }

      @keyframes rotate360 {
        to {
          transform: rotate(360deg);
        }
      }

      .support-wrapper {
        position: absolute;
        inset: 0;
        display: block;
        color: #000;
        text-decoration: none;
        cursor: pointer;
        transform-origin: center;
        transform: rotate(-10deg);

        &:hover {
          .support {
            background-color: #ffd700;
            @media (min-width: 992px) {
              transform: translateX(-50%) rotate(0) scale(1.2);
            }
          }

          .star > img {
            animation-play-state: running;
          }
        }

        .yellow-bg {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translateX(-50%) translateY(-50%);
          width: var(--badge-size);
          height: var(--badge-size);
          background-image: radial-gradient(
            circle calc(var(--badge-size) / 2) at center,
            #ffd700 0%,
            rgba(255, 215, 0, 0) 100%
          );
          opacity: 0.4;
          z-index: 1;
        }

        .star {
          width: calc(var(--badge-size) / 2);
          height: calc(var(--badge-size) / 2);
          position: absolute;
          z-index: 5;
          top: 0;
          left: 50%;
          transform: translateX(-50%);

          > img,
          > div {
            position: absolute;
            inset: 0;
            display: block;
            width: 100%;
            height: 100%;
          }

          > img {
            animation: rotate360 3s linear infinite;
          }

          > div {
            display: flex;
            align-items: center;
            justify-content: center;

            span:first-child {
              margin-top: -0.2em;
              font-size: calc(var(--badge-size) / 7);
              font-weight: 700;
              line-height: 1;
            }

            span:last-child {
              font-family: 'Syne Tactile', cursive;
              font-size: calc(var(--badge-size) / 18);
              font-style: italic;
              line-height: 1;
            }
          }

          @media (min-width: 992px) {
            img {
              animation-play-state: paused;
            }
          }
        }

        .support {
          position: absolute;
          top: calc(var(--badge-size) / 2.5);
          left: 50%;
          transform: translateX(-50%) rotate(0) scale(1);
          z-index: 6;
          width: fit-content;
          padding: 0.2em 0.75em;
          background-color: #fff;
          border: 3px solid #000;
          border-radius: 0.4em;
          text-align: center;
          font-size: calc(var(--badge-size) / 8);
          font-weight: 700;
          transition: all 0.25s ease;
        }
      }
    }
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

  .date-articles {
    margin-top: 2rem;
  }

  .date-line {
    display: flex;
    gap: 1rem;
    align-items: center;
    color: #ffd700;

    .date {
      font-size: 1.25rem;
      font-weight: 500;
    }

    hr {
      flex: 1;
    }
  }

  .article-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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
        font-weight: 500;
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
