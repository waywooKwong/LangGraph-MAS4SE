<template>
  <div class="main-case-window">
    <el-button @click="goToChatView" class="go-chat-button">返回</el-button>
    <h1>MAS<sup>4</sup>SE</h1>

    <div class="container">
      <div class="carousel" :data-slide="currentSlide">
        <div class="carousel__slide" @click="goToCase01">
          案例一
        </div>
        <div class="carousel__slide" @click="goToCase02">
          案例二
        </div>
        <div class="carousel__slide" @click="goToCase03">
          案例三
        </div>
        <div class="carousel__slide" @click="goToCase04">
          案例四
        </div>
      </div>
      <div class="next" @click="nextSlide">next</div>
      <div class="prev" @click="prevSlide">previous</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentSlide: 1
    };
  },
  methods: {
    nextSlide() {
      this.currentSlide = this.currentSlide === 4 ? 1 : this.currentSlide + 1;
    },
    prevSlide() {
      this.currentSlide = this.currentSlide === 1 ? 4 : this.currentSlide - 1;
    },
    goToChatView() {
        this.$router.push({ name: 'ChatView' });
    },
    goToCase01() {
        this.$router.push({ name: 'CaseShow01' }); 
    },
    goToCase02() {
        this.$router.push({ name: 'CaseShow02' }); 
    },
    goToCase03() {
        this.$router.push({ name: 'CaseShow03' }); 
    },
    goToCase04() {
        this.$router.push({ name: 'CaseShow01' }); 
    },
  }
};
</script>

<style scoped lang="scss" >
@import url('https://fonts.googleapis.com/css?family=Lato:300|Oswald');

$primary-color: hsl(289, 100%, 50%);
.main-case-window{
  height: 100%;
  background-color: $primary-color;
}

.go-chat-button{
  margin-top: 20px;
  margin-left: 20px;
  padding: 10px 40px;
  background-color: #7debf8;
}

.container {
  width: 90%;
  max-width: 60em;
  margin: 0 auto;
  padding-bottom: 5em;
  perspective: 100em;
}

.carousel {
  position: relative;
  width: 15em;
  height: 15em;
  margin: 0 auto;
  transform-style: preserve-3d;
  transition: transform 0.5s ease;

  &[data-slide="1"] {
    transform: rotateY(0deg);
  }

  &[data-slide="2"] {
    transform: rotateY(-90deg);
  }

  &[data-slide="3"] {
    transform: rotateY(-180deg);
  }

  &[data-slide="4"] {
    transform: rotateY(-270deg);
  }
}

.carousel__slide {
  margin-top: 50%;
  position: absolute;
  width: 15em;
  height: 15em;
  background: white;

  display: flex; 
  justify-content: center; 
  align-items: center; 
  cursor: pointer;

  img {
    width: 100%;
  }
}

.back,
.carousel__slide:nth-child(3) {
  transform: translateZ(-7.5em) rotateY(180deg);
}

.right,
.carousel__slide:nth-child(2) {
  transform: rotateY(-270deg) translateX(7.5em);
  transform-origin: top right;
}

.left,
.carousel__slide:nth-child(4) {
  transform: rotateY(270deg) translateX(-7.5em);
  transform-origin: center left;
}

.front,
.carousel__slide:nth-child(1) {
  transform: translateZ(7.5em);
}

.next,
.prev {
  position: absolute;
  top: 50%;
  right: 0;
  width: 7em;
  margin-top: 7%;
  border-radius: 3px;
  background: darken($primary-color, 30%);
  text-align: center;
  line-height: 3;
  color: white;
  transform: translateY(-50%);
  cursor: pointer;
}

.next {
  right: 15%; // 调整这个值来向中心靠拢
}

.prev {
  left: 15%; // 调整这个值来向中心靠拢
}



*,
*:before,
*:after {
  box-sizing: border-box;
}

// html,
// body {
//   width: 100%;
//   height: 100%;
// }

// html {
//   font-size: 62.5%;
// }

// body {
//   background: $primary-color;
//   font-family: 'Lato', sans-serif;
//   font-size: 2em;
//   line-height: 1.5;
// }

.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin: 0;
  padding: 0.5em;
  font-family: 'Oswald', sans-serif;
  font-size: 4em;
  text-transform: uppercase;
  text-align: center;
  color: darken($primary-color, 40%);
}

.cf:before,
.cf:after {
  content: " ";
  display: table;
}

.cf:after {
  clear: both;
}

.cf {
  *zoom: 1;
}
</style>