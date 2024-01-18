<template>
  <section class="background-gif headline">
    <div class="container">
      <div class="title">
        <h1>
          <a href="/">
            n<img class="sun" src="~assets/images/sun.png" alt="sun icon" />v
            dan
          </a>
        </h1>
        <p>
          Neposredna podpora <br />
          neodvisnim medijskim ustvarjalcem
        </p>
        <nav>
          <ul>
            <li><a href="/za-ustvarjalce">Za ustvarjalce</a></li>
            <li><a href="/dash/register">Za podpornike</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </section>
</template>

<script>
export default {}
</script>

<style scoped lang="scss">
.headline {
  padding: 1rem;

  .container:nth-of-type(1) {
    position: relative;
    z-index: 2;
  }

  .title {
    margin: 1rem 0;

    @media (min-width: 768px) {
      display: flex;
      align-items: flex-end;
    }

    h1 {
      font-weight: 700;
      font-size: 5rem;
      line-height: 0.75;
      text-align: center;
      margin: 0;

      a {
        color: inherit;
        text-decoration: none;
      }
    }

    p {
      font-size: 1.25rem;
      line-height: 1;
      font-weight: 700;
      text-align: center;
      margin: 1rem 0;
    }

    nav {
      align-self: stretch;

      ul,
      li {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      ul {
        display: flex;
        flex-wrap: wrap;
        gap: 0.25rem 1.5rem;
        justify-content: center;

        li {
          a {
            color: inherit;
            font-weight: 500;
          }
        }
      }
    }

    @media (min-width: 768px) {
      h1 {
        text-align: right;
        padding-right: 1.5rem;
      }

      p {
        text-align: left;
        font-size: 1.5rem;
        margin: 0;
        flex: 1;
      }

      nav {
        padding-left: 1.5rem;

        ul {
          justify-content: flex-end;
        }
      }
    }
  }

  .sun {
    height: 2.5rem;
    width: 2.5rem;
  }
}
</style>
