<template>
  <section class="sticky-badge-container">
    <div class="container">
      <div class="preamble">
        <div class="badge">
          <a href="/podpri" class="support-wrapper">
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
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {}
  }
}
</script>

<style scoped lang="scss">
.sticky-badge-container {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999999;
  padding: 1rem;
  padding-bottom: 0;

  @media (min-width: 992px) {
    margin-bottom: 3rem;
  }

  .preamble {
    display: none;
    flex-direction: column;
    align-items: flex-end;

    @media (min-width: 992px) {
      display: flex;
    }

    .badge {
      --badge-size: 180px;

      margin-top: 1.5rem;
      width: var(--badge-size);
      height: calc(var(--badge-size) / 1.5);
      position: relative;

      @media (min-width: 992px) {
        margin-top: 0;
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
}
</style>
