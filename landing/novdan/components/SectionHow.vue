<template>
  <section class="background-gradient-white-yellow how">
    <div class="container">
      <h1>Kako?</h1>
      <div class="row first">
        <p>
          Inštaliraj si <span>Nov<br> Dan vtičnik</span>.
        </p>
        <div class="browsers">
          <div class="button-browser-wrapper">
            <div class="support">
              Chrome
            </div>
            <div class="button">
              <img src="~assets/images/chrome.png" class="browser" alt="pink spinning star">
              <img src="~assets/images/modra-zvezda.svg" class="spinning-star" alt="pink spinning star">
            </div>
          </div>
          <div class="button-browser-wrapper">
            <div class="support">
              Firefox
            </div>
            <div class="button">
              <img src="~assets/images/mozilla.png" class="browser" alt="pink spinning star">
              <img src="~assets/images/modra-zvezda.svg" class="spinning-star" alt="pink spinning star">
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="subscribe">
          <p>
            Plačaj <br>naročnino.
          </p>
          <div class="moneybill">
            <img src="~assets/images/5-eur.svg" alt="pink spinning star">
            <div class="effect">
              <img src="~assets/images/zarki-roza.svg" alt="pink spinning star">
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="read">
          <p>
            Beri <br><span>neodvisne</span><br> medije.
          </p>
          <div>
            <img src="~assets/images/vesoljcek.png" alt="pink spinning star">
          </div>
        </div>
      </div>
      <div class="row forth" style="justify-content: end">
        <div>
          <p style="text-align: end">
            <span>Tvoj prispevek bo</span><br>
            <span>med njih razdeljen</span><br>
            <span>samodejno.</span>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.how {
  padding: 6rem 0;
  h1 {
    font-size: 7rem;
    font-weight: 800;
    margin-top: 0;
    margin-bottom: 2rem;
    text-align: center;
  }
  p {
    text-transform: uppercase;
    font-size: 2.5rem;
    font-weight: 700;
    position: relative;
    z-index: 2;
    margin: 5rem 0;
    span {
      font-weight: 800;
    }
  }
  .first {
    margin-top: 4rem;
    margin-bottom: 6rem;
  }
  .browsers {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .button-browser-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    margin: 2rem 0;
    &:first-child {
      margin-left: 8rem;
    }
    .support {
      font-size: 3rem;
      font-weight: 700;
      padding: 0.25rem 6rem 0.25rem 1rem;
      border: 3px solid #000000;
      border-radius: 1.25rem;
      background-color: white;
      position: relative;
      z-index: 3;
      transition: all 0.25s ease;
      transform: rotate(0) scale(1);
      cursor: pointer;
    }
    .button {
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 5;
      right: 0;
      transform: translateX(50%);
      cursor: pointer;
      .browser {
        position: absolute;
        z-index: 6;
        height: 4rem;
      }
      .spinning-star {
        width: 10rem;
        animation: rotate360 3s linear infinite;
        animation-play-state: paused;
      }
    }
    &:hover {
      .support {
        background-color: #ffd700;
        transform:rotate(0) scale(1.2);
      }
      .spinning-star {
        animation-play-state: running;
      }
    }
  }

  .subscribe {
    margin-left: 8rem;
    display: flex;
    align-items: center;
    .moneybill {
      margin-left: 5rem;
      position: relative;
      &>img {
        z-index: 2;
        position: relative;
        width: 24rem;
      }
      .effect {
        width: 16rem;
        height: auto;
        top: 50%;
        left: 50%;
        position: absolute;
        transition: all 0.25s ease;
        transform: translateY(-50%) translateX(-50%) scale(1);
      }
      &:hover {
        .effect {
          transform: translateY(-50%) translateX(-50%) scale(3);
        }
      }
    }
  }
  .read {
    margin-left: 16rem;
    display: flex;
    &>div {
      margin-top: 5rem;
      margin-left: 3rem;
      transition: all 0.25s ease;
      transform: rotate(0) scale(1);
      img {
        width: 18rem;
      }
      &:hover {
        transform: rotate(0) scale(1.2);
      }
    }
  }
  .forth {
    p {
      span {
        font-weight: 700;
        background-color: white;
        margin: 0.5rem 0;
        padding: 0 0.25rem;
        display: inline-block;
        &:last-child {
          font-weight: 800;
        }
      }
    }
  }
}

</style>
