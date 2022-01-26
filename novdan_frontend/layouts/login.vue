<template>
  <div class="login-layout">
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
  font-family: 'Syne', sans-serif;
}
.login-layout {
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
      padding: 2rem 2rem;
    }
    @media (min-width: 992px) {
      padding: 4rem 8rem;
    }
  }
  h3 {
    font-size: 3rem;
    font-weight: 400;
    font-family: 'Le Murmure';
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
      font-family: 'Syne Tactile', cursive;
      font-size: 20px;
      line-height: 0.8;
      letter-spacing: 1px;
      margin-bottom: 10px;
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
      font-family: 'Syne', sans-serif;
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
  }
}
</style>
