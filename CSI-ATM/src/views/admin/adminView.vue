<template>
  <div class="log-wrapper">
    <log />
  </div>
</template>
<script>
import log from "@/components/log.vue";

export default {
  components: {
    log,
  },
  setup() {},
};
</script>
<style scoped>
.log-wrapper {
  position: absolute; /* 或使用fixed */
  top: 0;
  left: 0;
  width: 100vw; /* 视口宽度的100% */
  height: 100vh; /* 视口高度的100% */
  min-width: 100%; /* 确保至少覆盖整个宽度 */
  min-height: 100%; /* 确保至少覆盖整个高度 */
  display: flex; /* 设置为Flex容器 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
</style>
