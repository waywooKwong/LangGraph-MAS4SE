<template>
  <div class="main">
    <AnimationBackground />
    <div class="main-case-window">
      <el-button @click="goToChatView" class="go-chat-button">MAS4SE HomePage</el-button>
      <h1>MAS<sup>4</sup>SE</h1>

      <div class="container">
        <div class="carousel" :data-slide="currentSlide">
          <div class="carousel__slide" @click="goToCase01">
            案例一-balabala
          </div>
          <div class="carousel__slide" @click="goToCase02">
            案例二-代码监管软件
          </div>
          <div class="carousel__slide" @click="goToCase03">
            案例三-英文单词学习软件
          </div>
          <div class="carousel__slide" @click="goToCase04">
            案例四-成绩管理
          </div>
        </div>
        <div class="next" @click="nextSlide">next</div>
        <div class="prev" @click="prevSlide">previous</div>
      </div>
    </div>
  </div>
</template>

<script>
import AnimationBackground from '@/components/AnimationBackground.vue'

export default {
  components: {
    AnimationBackground
  },
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
        // 获取当前页面的参数 aaa
      const userId = 'balabala';  // 假设当前页面有一个属性 

      // 跳转并传递参数
      this.$router.push({ path: `/case-show` ,query: { id: userId }});

    },
    goToCase02() {
        // 获取当前页面的参数 aaa
      const userId = '代码监管软件';  // 假设当前页面有一个属性 

      // 跳转并传递参数
      this.$router.push({ path: `/case-show` ,query: { id: userId }});

    },
    goToCase03() {
       // 获取当前页面的参数 aaa
      const userId = '英文单词学习软件';  // 假设当前页面有一个属性 

      // 跳转并传递参数
      this.$router.push({ path: `/case-show` ,query: { id: userId }});

    },
    goToCase04() {
        // 获取当前页面的参数 aaa
      const userId = '成绩管理';  // 假设当前页面有一个属性 

      // 跳转并传递参数
      this.$router.push({ path: `/case-show` ,query: { id: userId }});

    },
  }
};
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css?family=Lato:300|Oswald');

$primary-color: hsl(289, 100%, 50%);
.main{
  height: 100vh;
  position: relative; /* 使子元素能够相对定位 */
  overflow: hidden; /* 防止背景溢出 */
}

.main-case-window {
  position: relative; /* 使 content 可以使用 z-index */
  height: 100%;
  background-color: transparent;
  z-index: 2; /* 设置一个较高的 z-index 值 */
}

.go-chat-button {
  margin-top: 20px;
  margin-left: 20px;
  padding: 10px 40px;
  background-color: #dce2fa;;
  border-color: #000000;
  color: #394398;
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
  color: #27273c;
  font-weight: bold;
  // background: white;
  background-image: url('@/assets/history_case/case_cover/with_3QA.png');

  background-size: cover; /* Ensures the background image covers the entire element */
  background-position: center; /* Centers the background image */

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
  // color: linear-gradient(-225deg, #231557 0%, #44107A 29%, #FF1361 67%, #FFF800 100%);
  background: linear-gradient(-225deg, #231557 0%, #44107A 29%, #FF1361 67%, #FFF800 100%);
  background-clip: text; /* 标准属性 */
  -webkit-background-clip: text; /* WebKit 前缀 */
  -webkit-text-fill-color: transparent;
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