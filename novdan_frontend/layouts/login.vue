<template>
  <div class="login-layout">
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
    <DashHeadline />
    <section class="background-gradient-yellow-white">
      <div class="container">
        <div class="content-narrow">
          <Nuxt />
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss">
body {
  margin: 0;
  font-family: 'wf-syne', sans-serif;
}
#bgvid {
  object-fit: cover;
  width: 100vw;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
}
.login-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  section {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    z-index: 1;
  }
  .background-gradient-yellow-white {
    background-color: white;
    background-image: linear-gradient(
      to bottom,
      rgba(255, 215, 0, 0.4) 0%,
      rgba(255, 215, 0, 0) 67%
    );
    flex-grow: 1;
  }
  .container {
    width: 100%;
    @media (min-width: 576px) {
      max-width: 540px;
    }
    @media (min-width: 768px) {
      max-width: 720px;
    }
    @media (min-width: 992px) {
      max-width: 960px;
    }
    @media (min-width: 1200px) {
      max-width: 1140px;
    }
    @media (min-width: 1400px) {
      max-width: 1320px;
    }
  }
  .content-narrow {
    padding: 2rem 1rem;
    @media (min-width: 576px) {
      padding: 4rem 2rem;
    }
    @media (min-width: 992px) {
      padding: 4rem 8rem;
    }
  }
  h3 {
    font-size: 3rem;
    font-weight: 400;
    font-family: 'wf-le-murmure', serif;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 0;
    margin-bottom: 2rem;
  }
  form {
    .input-group {
      margin-bottom: 20px;
    }
    label {
      display: block;
      color: #1103b1;
      font-family: 'wf-syne-tactile', cursive;
      font-size: 20px;
      line-height: 0.8;
      letter-spacing: 1px;
      margin-bottom: 10px;
    }
    .form-input-error {
      color: red;
      margin: 6px 0 6px 16px;
    }
    span {
      margin-left: 16px;
      text-decoration: underline;
    }
    input[type='text'],
    input[type='email'],
    input[type='password'] {
      border-radius: 10px;
      border: 2px solid #1103b1;
      padding: 8px 16px;
      font-size: 20px;
      width: 90%;
      @media (min-width: 576px) {
        width: 480px;
      }
      @media (min-width: 992px) {
        width: 480px;
      }
    }
    input[type='submit'] {
      border: 2px solid #000000;
      border-radius: 10px;
      background-color: #ffffff;
      font-family: 'wf-syne', sans-serif;
      font-size: 25px;
      font-weight: 700;
      padding: 8px 24px;
      margin: 10px 0;
      cursor: pointer;
      &:hover {
        background-color: #1103b1;
        border-color: #1103b1;
        color: white;
      }
    }
    a {
      margin-left: 10px;
    }
  }
  .error {
    color: red;
  }
}
</style>
