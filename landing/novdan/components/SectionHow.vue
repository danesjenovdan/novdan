<template>
  <section class="background-gradient-white-yellow how">
    <div class="container">
      <h1>Kako?</h1>
      <div class="row">
        <p>
          Inštaliraj si <span>Nov<br> Dan vtičnik</span> za<br> Chrome ali Firefox.
        </p>
        <div class="button-firefox">
          <img src="~assets/images/mozilla.png" alt="pink spinning star">
        </div>
        <div class="button-chrome">
          <img src="~assets/images/chrome.png" alt="pink spinning star">
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
  .button-firefox, .button-chrome {
    background-image: url("assets/images/circle-background.png");
    background-size: 100% 100%;
    //border: 1px solid #000000;
    //border-radius: 50%;
    height: 7rem;
    width: 7rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: 3rem;
    transition: all 0.25s ease;
    transform: rotate(0) scale(1);
    img {
      height: 4rem;
    }
    &:hover {
      cursor: pointer;
      transform:rotate(0) scale(1.2);
    }
  }
  .button-firefox {
    margin-top: 4rem;
  }
  .button-chrome {
    margin-top: 5rem;
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
        width: 44rem;
        height: auto;
        top: 50%;
        left: 50%;
        position: absolute;
        transition: all 0.25s ease;
        transform: translateY(-50%) translateX(-50%) scale(1);
      }
      &:hover {
        .effect {
          transform: translateY(-50%) translateX(-50%) scale(1.2);
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
}
</style>
