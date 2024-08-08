<template>
  <div class="main">
    <AnimationBackground />
    <div class="main-case-window">
      <el-button @click="goToChatView" class="go-chat-button">
        MAS4SE HomePage
      </el-button>
      <h1>MAS<sup>4</sup>SE</h1>
      <div class="external-link">
        <el-button @click="goToExternalLink" class="external-link-button">
          Go to AI drawing Page
        </el-button>
      </div>

      <div class="container">
        <div class="carousel" :data-slide="currentSlide">
          <div 
            class="carousel__slide" 
            @click="goToCase01"
            @mouseover="hoverSlide(1)"
            @mouseleave="leaveSlide"
          >
            <template v-if="hoveredSlide === 1">
              <img src="@/assets/history_case/case_cover/UI01.png" alt="Case 1 Image">
            </template>
            <template v-else>
              案例一-游戏定制
            </template>
          </div>
          <div 
            class="carousel__slide" 
            @click="goToCase02"
            @mouseover="hoverSlide(2)"
            @mouseleave="leaveSlide"
          >
            <template v-if="hoveredSlide === 2">
              <img src="@/assets/history_case/case_cover/UI02.png" alt="Case 2 Image">
            </template>
            <template v-else>
              案例二-代码监管软件
            </template>
          </div>
          <div 
            class="carousel__slide" 
            @click="goToCase03"
            @mouseover="hoverSlide(3)"
            @mouseleave="leaveSlide"
          >
            <template v-if="hoveredSlide === 3">
              <img src="@/assets/history_case/case_cover/UI03.png" alt="Case 3 Image">
            </template>
            <template v-else>
              案例三-英文单词学习软件
            </template>
          </div>
          <div 
            class="carousel__slide" 
            @click="goToCase04"
            @mouseover="hoverSlide(4)"
            @mouseleave="leaveSlide"
          >
            <template v-if="hoveredSlide === 4">
              <img src="@/assets/history_case/case_cover/UI04.png" alt="Case 4 Image">
            </template>
            <template v-else>
              案例四-成绩管理
            </template>
          </div>
        </div>
        <div class="next" @click="nextSlide">next</div>
        <div class="prev" @click="prevSlide">previous</div>
      </div>
    </div>
  </div>
</template>

<script>
import AnimationBackground from "@/components/AnimationBackground.vue";

export default {
  components: {
    AnimationBackground,
  },
  data() {
    return {
      currentSlide: 1,
      hoveredSlide: null,
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
      this.$router.push({ name: "ChatView" });
    },
    goToCase01() {
      const userId = "balabala";
      this.$router.push({ path: `/case-show`, query: { id: userId } });
    },
    goToCase02() {
      const userId = "代码监管软件";
      this.$router.push({ path: `/case-show`, query: { id: userId } });
    },
    goToCase03() {
      const userId = "英文单词学习软件";
      this.$router.push({ path: `/case-show`, query: { id: userId } });
    },
    goToCase04() {
      const userId = "成绩管理";
      this.$router.push({ path: `/case-show`, query: { id: userId } });
    },
    goToExternalLink() {
      window.open("http://127.0.0.1:7860", "_blank");
    },
    hoverSlide(index) {
      this.hoveredSlide = index;
    },
    leaveSlide() {
      this.hoveredSlide = null;
    },
  },
};
</script>

<style scoped lang="scss">
@import url("https://fonts.googleapis.com/css?family=Lato:300|Oswald");

$primary-color: hsl(289, 100%, 50%);
.main {
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.main-case-window {
  position: relative;
  height: 100%;
  background-color: transparent;
  z-index: 2;
}

.go-chat-button {
  margin-top: 20px;
  margin-left: 20px;
  padding: 10px 40px;
  background-color: #dce2fa;
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
  background-image: url("@/assets/history_case/case_cover/with_3QA.png");
  background-size: cover;
  background-position: center;

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
  right: 15%;
}

.prev {
  left: 15%;
}

*,
*:before,
*:after {
  box-sizing: border-box;
}

h1 {
  margin: 0;
  padding: 0.5em;
  font-family: "Oswald", sans-serif;
  font-size: 4em;
  text-transform: uppercase;
  text-align: center;
  background: linear-gradient(
    -225deg,
    #231557 0%,
    #44107a 29%,
    #ff1361 67%,
    #fff800 100%
  );
  background-clip: text;
  -webkit-background-clip: text;
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

.external-link {
  text-align: center;
  margin-top: 20px;
}

.external-link-button {
  padding: 10px 20px;
  background-color: #9212dc;
  color: #ffffff;
  border: none;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

.external-link-button:hover {
  background-color: darken(#9613e2, 10%);
}
</style>
