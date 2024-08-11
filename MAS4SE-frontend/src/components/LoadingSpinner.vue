<template>
  <div class="spinner">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  </div>
</template>

<script>
export default {
  name: "LoadingSpinner",
};
</script>

<style scoped>
.spinner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 25px; /* 减小容器宽度以缩小圆点之间的距离 */
  height: 15px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #8210b3;
  animation: bounce 1s infinite; /* 设置动画总时间为1秒 */
}

/* 调整每个圆点的动画延迟时间 */
.dot:nth-child(2) {
  animation-delay: 0.1s;
}

.dot:nth-child(3) {
  animation-delay: 0.2s;
}

/* 定义 bounce 动画 */
@keyframes bounce {
  0% {
    transform: translateY(0);
  }
  10% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px); /* 跳动幅度 */
  }
  90% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(0); /* 跳回到原位 */
  }
}
</style>
