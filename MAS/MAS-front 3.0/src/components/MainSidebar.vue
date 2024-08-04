<template>
  <div id="menu" ref="menu" :class="{ expanded: menuExpanded }">
    <!-- 汉堡按钮 -->
    <div class="hamburger" ref="hamburger">
      <div class="line"></div>
      <div class="line"></div>
      <div class="line"></div>
    </div>
    <!-- 菜单内容 -->
    <div class="menu-inner" ref="menuInner">
      <button @click="navigateTo('/chat')"style="color: #f9f9f9;">对话</button>
      <button @click="navigateTo('/agent-map')"style="color: #f9f9f9;">定制</button>
    </div>
    <!-- SVG 背景 -->
    <svg version="1.1" id="blob" ref="blob" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <path id="blob-path" ref="blobPath" d="M60,500H0V0h60c0,0,20,172,20,250S60,900,60,500z"/>
    </svg>
  </div>
</template>

<script>
export default {
  data() {
    return {
      height: window.innerHeight,
      x: 0,
      y: window.innerHeight / 2,
      curveX: 10,
      curveY: 0,
      targetX: 0,
      xitteration: 0,
      yitteration: 0,
      menuExpanded: false,
      hoverZone: 150,
      expandAmount: 20
    };
  },
  mounted() {
    this.initializeAnimation();
  },
  methods: {
    initializeAnimation() {
      window.addEventListener('mousemove', this.handleMouseMove);

      // 获取 DOM 元素
      this.$refs.menu.addEventListener('mouseenter', () => this.menuExpanded = true);
      this.$refs.menu.addEventListener('mouseleave', () => this.menuExpanded = false);

      // 启动动画
      this.svgCurve();
    },
    handleMouseMove(e) {
      this.x = e.pageX;
      this.y = e.pageY;
    },
    svgCurve() {
      if (!this.$refs.blobPath) return; // 确保 blobPath 存在

      if ((this.curveX > this.x - 1) && (this.curveX < this.x + 1)) {
        this.xitteration = 0;
      } else {
        if (this.menuExpanded) {
          this.targetX = 0;
        } else {
          this.xitteration = 0;
          this.targetX = (this.x > this.hoverZone) ? 0 : -((60 + this.expandAmount) / 100) * (this.x - this.hoverZone);
        }
        this.xitteration++;
      }

      if ((this.curveY > this.y - 1) && (this.curveY < this.y + 1)) {
        this.yitteration = 0;
      } else {
        this.yitteration = 0;
        this.yitteration++;
      }

      this.curveX = this.easeOutExpo(this.xitteration, this.curveX, this.targetX - this.curveX, 100);
      this.curveY = this.easeOutExpo(this.yitteration, this.curveY, this.y - this.curveY, 100);

      const anchorDistance = 200;
      const curviness = anchorDistance - 40;

      const newCurve2 = `M60,${this.height}H0V0h60v${this.curveY - anchorDistance}c0,${curviness},${this.curveX},${curviness},${this.curveX},${anchorDistance}S60,${this.curveY},60,${this.curveY + anchorDistance * 2}V${this.height}z`;

      this.$refs.blobPath.setAttribute('d', newCurve2);
      this.$refs.blob.style.width = `${this.curveX + 60}px`;
      this.$refs.hamburger.style.transform = `translate(${this.curveX}px, ${this.curveY}px)`;

      window.requestAnimationFrame(this.svgCurve);
    },
    easeOutExpo(currentIteration, startValue, changeInValue, totalIterations) {
      return changeInValue * (-Math.pow(2, -10 * currentIteration / totalIterations) + 1) + startValue;
    },
    navigateTo(path) {
      this.$router.push(path); // 使用 Vue Router 跳转
    }
  }
};
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #26394E;
}

#menu {
  height: 100%;
  position: fixed;
  background-color: #222222;
  width: 200px;
  transition: 1000ms all cubic-bezier(0.19, 1, 0.22, 1);
  transform: translateX(-100%);
  left: 110px;
}

#menu.expanded {
  transform: translateX(0%);
  left: 0;
}

.menu-inner {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 从上到下排列 */
}

.menu-inner button {
  background-color: transparent; /* 透明背景 */
  color: #26394E;
  border: none;
  padding: 15px 30px;
  margin: 10px 0; /* 上下间距 */
  font-size: 18px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

.menu-inner button:hover {
  background-color: rgba(0, 0, 0, 0.1); /* 鼠标悬停时的背景色 */
  color: #000;
}

#blob {
  top: 0;
  z-index: -1;
  right: 60px;
  transform: translateX(100%);
  height: 100%;
  position: absolute;
}

#blob-path {
  height: 100%;
  fill: #222222;
}

.hamburger {
  right: 20px;
  position: absolute;
  width: 15px;
  height: 20px;
  margin-top: -10px;
}

.hamburger .line {
  width: 100%;
  height: 4px;
  background-color: #fff;
  position: absolute;
}

.hamburger .line:nth-child(2) {
  top: 50%;
  margin-top: -2px;
}

.hamburger .line:nth-child(3) {
  bottom: 0;
}
</style>
