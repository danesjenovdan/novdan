<template>
  <section class="footer">
    <div class="background-gradient-pink">
      <div class="container">
        <div>
          <p>
            Projekt razvija <br v-if="windowWidth <= 576"> <a href="https://danesjenovdan.si/" target="_blank">Danes je nov dan</a> <br>
            ob podpori fundacije <br v-if="windowWidth <= 576"><a href="https://www.grantfortheweb.org/" target="_blank">Grant for the Web</a>.
          </p>
          <p>
            <a href="mailto:novdan@djnd.si" target="_blank">novdan@djnd.si</a>
          </p>
        </div>
      </div>
      <img src="~/assets/images/novdan.png" alt="novdan big text">
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

<style scoped lang="scss">
.background-gradient-pink {
  background-image: linear-gradient(to bottom, rgba(255, 215, 0, 0) 0%, #ff5ccb 100%);
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.footer {
  padding-bottom: 0;
  .container>div {
    margin: 3rem 30px;
    @media (min-width: 1200px) {
      margin: 6rem 0;
    }
  }
  p {
    text-align: center;
    font-size: 1.25rem;
    line-height: 1.5;
    @media (min-width: 1200px) {
      font-size: 2rem;
      line-height: 1;
    }
    a {
      color: #1103b1;
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }
    &:first-child {
      a {
        font-weight: 700;
      }
    }
    &:last-child {
      a {
        font-weight: 800;
      }
    }
  }
  img {
    width: 100%;
    z-index: 2;
  }
}
</style>
