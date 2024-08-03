<template>
    <div class="container">
      <img
        class="squares"
        src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/169963/squares.png"
        alt="Squares"
      />
      <div class="boxes">
        <div class="box" ref="boxOne"></div>
        <div class="box" ref="boxTwo"></div>
        <div class="box" ref="boxThree"></div>
        <div class="box">
          <div class="progress">
            <div class="bar">
              <div class="bar__fill" ref="barFill"></div>
            </div>
            <div
              class="point"
              v-for="(point, index) in points"
              :key="index"
              :class="{ 'point--active': activeIndex === index, 'point--complete': activeIndex > index }"
              @click="handlePointClick(index)"
            >
              <div class="bullet"></div>
              <label class="label">{{ point }}</label>
            </div>
          </div>
        </div>
      </div>
      <button class="radius-toggle" @click="toggleClickRadius">
        Toggle Click Radius
      </button>
    </div>
  </template>
  
  <script>
  import { TweenMax, TimelineMax, Back } from 'gsap';
  
  export default {
    name: 'LoadPage',
    data() {
      return {
        points: ['Select', 'Review', 'Payment', 'Success'],
        activeIndex: 0,
        progressAnimationInterval: null
      };
    },
    methods: {
      handlePointClick(index) {
        const totalPoints = this.points.length;
        const barFill = this.$refs.barFill;
  
        TweenMax.to(barFill, 0.6, {
          width: ((index - 1) / (totalPoints - 1)) * 100 + '%'
        });
  
        if (index >= this.activeIndex) {
          this.activeIndex = index;
        }
      },
      toggleClickRadius() {
        document.body.classList.toggle('show-radius');
      },
      startProgressAnimation() {
        this.progressAnimationInterval = setInterval(() => {
          const totalPoints = this.points.length;
          const randomIndex = Math.floor(Math.random() * totalPoints);
  
          TweenMax.to(this.$refs.barFill, 0.6, {
            width: ((randomIndex - 1) / (totalPoints - 1)) * 100 + '%'
          });
  
          if (randomIndex >= this.activeIndex) {
            this.activeIndex = randomIndex;
          }
        }, 1200);
      }
    },
    mounted() {
      const boxOne = new TimelineMax();
      const boxTwo = new TimelineMax();
      const boxThree = new TimelineMax();
  
      boxOne.to(this.$refs.boxOne, 0.6, {
        opacity: 0.25,
        scale: 1,
        ease: Back.easeOut
      }).to(this.$refs.boxOne, 0.6, {
        rotation: 4,
        ease: Back.easeOut
      }, 2);
  
      boxTwo.to(this.$refs.boxTwo, 0.6, {
        opacity: 0.5,
        scale: 1,
        ease: Back.easeOut
      }, 0.6).to(this.$refs.boxTwo, 0.6, {
        rotation: -4,
        ease: Back.easeOut
      }, 1.8);
  
      boxThree.to(this.$refs.boxThree, 0.6, {
        opacity: 1,
        scale: 1,
        ease: Back.easeOut
      }, 1.2);
  
      this.startProgressAnimation();
    },
    beforeDestroy() {
      if (this.progressAnimationInterval) {
        clearInterval(this.progressAnimationInterval);
      }
    }
  };
  </script>
  
  <style scoped>
  body {
    background: #E8DFD9;
  }
  
  .squares {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .boxes {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 90%;
    max-width: 790px;
    height: 180px;
    font-family: "Open Sans", sans-serif;
    transform: translate(-50%, -50%);
  }
  
  .box {
    position: relative;
    display: flex;
    align-items: center;
    flex-direction: row;
    background: #FFF;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    box-shadow: 40px 0 65px rgba(212, 197, 186, 0.4);
    padding: 0 80px;
    box-sizing: border-box;
    opacity: 0;
    transform-origin: center;
    transform: scale(1.2, 1.2);
  }
  
  .box:nth-child(1) {
    position: absolute;
    left: 3%;
    width: 94%;
  }
  
  .box:nth-child(2) {
    position: absolute;
    left: 2%;
    width: 96%;
  }
  
  .progress {
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
  }
  
  .bar {
    position: absolute;
    top: 50%;
    left: 50%;
    background: #E8DFD8;
    width: 100%;
    height: 3px;
    border-radius: 10px;
    transform: translate(-50%, -50%);
    overflow: hidden;
  }
  
  .bar__fill {
    display: block;
    background: #BD8044;
    height: 100%;
  }
  
  .point {
    position: relative;
    color: #AC9585;
    cursor: pointer;
  }
  
  .point:before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 120px;
    height: 120px;
    border-radius: 100%;
    transform: translate(-50%, -50%);
    transition: 0.3s ease;
  }
  
  .show-radius .point:before {
    background: rgba(0, 0, 0, 0.1);
  }
  
  .point--complete,
  .point--active {
    color: #BA7C3F;
  }
  
  .bullet {
    z-index: 1;
    position: relative;
    background: #AC9585;
    width: 8px;
    height: 8px;
    border-radius: 100%;
    transition: 0.3s ease;
  }
  
  .point--complete .bullet,
  .point--active .bullet {
    background: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2),
                0 0 0 6px #BD8044;
  }
  
  .point--active .bullet {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2),
                0 0 0 10px #BD8044;
  }
  
  .label {
    position: absolute;
    top: 100%;
    left: 50%;
    margin: 20px 0 0 0;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    transform: translate(-50%, 0);
  }
  
  .radius-toggle {
    position: absolute;
    top: 20px;
    left: 20px;
    display: block;
    background: #FFF;
    border: 0;
    border-radius: 4px;
    box-shadow: 40px 0 65px rgba(212, 197, 186, 0.4);
    padding: 10px;
    color: #BA7C3F;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
  }
  </style>
  