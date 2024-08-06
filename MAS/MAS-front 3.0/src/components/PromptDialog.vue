<template>
  <div class="box-container">
    <div class="box"></div>
  </div>
</template>

<style scoped>
/* 父容器 */
.box-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 全屏高度 */
}

/* Message Box */
.box {
  --border-size: 3px;
  --border-angle: 0turn;
  /* 调整框的大小 */
  width: 100vmin;
  height: 60vmin;
  background-image: conic-gradient(from var(--border-angle), #213, #112 50%, #213), conic-gradient(from var(--border-angle), transparent 20%, #08f, #f03);
  background-size: calc(100% - (var(--border-size) * 2)) calc(100% - (var(--border-size) * 2)), cover;
  background-position: center center;
  background-repeat: no-repeat;
  -webkit-animation: bg-spin 3s linear infinite;
  animation: bg-spin 3s linear infinite;
}

@-webkit-keyframes bg-spin {
  to {
    --border-angle: 1turn;
  }
}

@keyframes bg-spin {
  to {
    --border-angle: 1turn;
  }
}

.box:hover {
  -webkit-animation-play-state: paused;
  animation-play-state: paused;
}

@property --border-angle {
  syntax: "<angle>";
  inherits: true;
  initial-value: 0turn;
}
</style>
