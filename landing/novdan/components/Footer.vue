<template>
  <section class="footer">
    <video
      id="bgvidfooter"
      playsinline
      autoplay
      muted
      loop
      poster="~assets/images/gif.png"
    >
      <source src="~assets/video/back_v2_1.mp4" type="video/mp4">
    </video>
    <div class="background-gradient-pink">
      <div class="container">
        <div>
          <p>
            Projekt razvija <a href="https://danesjenovdan.si/" target="_blank">Danes je nov dan</a> <br>
            ob podpori fundacije <a href="https://www.grantfortheweb.org/" target="_blank">Grant for the Web</a>.
          </p>
          <p>
            <a href="mailto:novdan@djnd.si" target="_blank">novdan@djnd.si</a>
          </p>
        </div>
      </div>
      <img src="~/assets/images/novdan.png" alt="novdan big text" />
    </div>
  </section>
</template>

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
    margin: 6rem 0;
  }
  p {
    text-align: center;
    font-size: 2rem;
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
  video {
    object-fit: cover;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    position: absolute;
    z-index: -1;
  }
}
</style>
