<template>
  <section class="background-gradient-orange-pink media">
    <div class="container">
      <h2>Sodelujoči <br> mediji</h2>
      <div class="row">
        <div>
          <ul>
            <li>
              <a href="/" target="_blank">
                <span>Pod črto</span>
                <img src="~assets/images/pod-crto.svg" alt="Pod Črto logo">
              </a>
            </li>
            <li>
              <a href="/" target="_blank">
                <span>Boris Vezjak - In Media Res</span>
                <img src="~assets/images/imr.svg" alt="Boris Vezjak - In Media Res logo">
              </a>
            </li>
            <li>
              <a href="/" target="_blank">
                <span>Oštro</span>
                <img src="~assets/images/ostro.svg" alt="Oštro logo">
              </a>
            </li>
            <li>
              <a href="/" target="_blank">
                <span>Radio Študent</span>
                <img src="~assets/images/rs.svg" alt="Radio Študent logo">
              </a>
            </li>
            <li>
              <a href="/" target="_blank">
                <span>Domen Savič - Državljan D</span>
                <img src="~assets/images/drzavljan-d.svg" alt="Domen Savič - Državljan D logo">
              </a>
            </li>
          </ul>
        </div>
        <div class="support-section">
          <div class="support-wrapper">
            <div class="button">
              <div class="support">
                Pridruži se!
              </div>
              <div class="star">
                <img src="~assets/images/star.png" alt="pink spinning star">
                <div>
                  <span>5</span>
                  <span>eur/<br>mes</span>
                </div>
              </div>
            </div>
            <div class="subtitle">
              <p>Podpri <span>neodvisno</span> novinarstvo.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
.media {
  padding: 6rem 0;
  h2 {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
    margin: 0;
  }
  ul {
    list-style-type: none;
    padding-left: 0;
    li {
      margin: 3rem 0;
      a {
        text-decoration: none;
        text-transform: uppercase;
        color: black;
        font-size: 2rem;
        font-weight: 700;
        //padding: 0.5rem 0;
        display: inline-block;
        position: relative;
      }
      span {
        padding-right: 2rem;
      }
      img {
        height: 5rem;
        transition:all .3s cubic-bezier(.28,.05,.65,.97);
        position: absolute;
        top: -1.5rem;
      }
      &:hover {
        img {
          animation:shake .4s 1;
        }
      }
    }
  }
}

.support-section {
  display: flex;
  align-items: center;
  margin-left: 12rem;
}

.support-wrapper {
  .button {
    position: relative;
    display: flex;
    align-items: center;
    .support {
      font-size: 3rem;
      font-weight: 700;
      padding: 0.5rem 7rem 0.5rem 2rem;
      border: 3px solid #000000;
      border-radius: 1.25rem;
      background-color: white;
      position: relative;
      z-index: 1;
      transition: all 0.25s ease;
      transform:rotate(0) scale(1);
    }
    .star {
      position: absolute;
      z-index: 1;
      right: -4rem;
      img {
        height: 11rem;
        animation: rotate360 3s linear infinite;  /* animation set */
        animation-play-state: paused;
      }
      div {
        position: absolute;
        top: 4rem;
        left: 3.5rem;
        z-index: 2;
        span:first-child {
          font-size: 3rem;
          font-weight: 700;
          line-height: 1;
        }
        span:last-child {
          font-style: italic;
          display: inline-block;
        }
      }
    }
    &:hover {
      cursor: pointer;
      .star img {
        animation-play-state: running;
      }
      .support {
        background-color: #ffd700;
        transform:rotate(0) scale(1.1);
      }
    }
  }
  .subtitle {
    margin-top: 2rem;
    margin-left: 3rem;
    font-size: 1.5rem;
    font-weight: 700;
    span {
      font-style: italic;
      color: #1103b1;
      font-weight: 400;
    }
  }
}

@keyframes shake{
  0%{ transform:rotate(3deg) scale(1.2) }
  20%{ transform:rotate(-3deg) scale(1.2) }
  40%{ transform:rotate(3deg) scale(1.2) }
  60%{ transform:rotate(-3deg) scale(1.2) }
  80%{ transform:rotate(3deg) scale(1.2) }
  100%{ transform:rotate(0) scale(1.2) }
}
</style>
