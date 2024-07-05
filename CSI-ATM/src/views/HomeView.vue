<script setup>
import inBalanceButton from "@/components/buttons/inBalanceButton.vue";
import outBalanceButton from "@/components/buttons/outBalanceButton.vue";
import transBalanceButton from "@/components/buttons/transBalanceButton.vue";
import adminButton from "@/components/buttons/adminButton.vue";
components: {
  inBalanceButton, outBalanceButton, transBalanceButton, adminButton;
}

import { onMounted } from 'vue'; //设置图标
onMounted(() => {
  setFavicon('/icons/favicon-home.ico');
});
function setFavicon(href) {
  let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
  link.type = 'image/x-icon';
  link.rel = 'shortcut icon';
  link.href = href;
  document.getElementsByTagName('head')[0].appendChild(link);
}
</script>

<template>
  <div class="container">
    <div class="title">
      ATM简易系统
    </div>
    <!-- 用户按钮组 -->
    <div class="user-container">
      <div class="button-group">
        <inBalanceButton class="button" />
        <outBalanceButton class="button" />
        <transBalanceButton class="button" />
      </div>
    </div>

    <!-- 管理员按钮 -->
    <div class="admin-container">
      <adminButton class="admin-button" />
    </div>
  </div>
</template>

<style scoped>
.container {
  position: relative;
  height: 600px;
  width: 1024px;
  /* 设置容器高度和宽度 */
  border: 2px solid #151414;
  /* 外框样式，可以根据需要调整颜色和粗细 */
  padding: 20px;
  /* 外框与内容之间的间距 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-size: 200%;
  text-align: center;
  margin-bottom: 40px;
  /* 与按钮组之间的间距 */
}

.user-container {
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  height: 400px;
  /* 占满父容器的高度 */
}

.button-group {
  display: flex;
}

.button {
  margin: 0 10px;
  /* 按钮之间的间距 */
}

.admin-container {
  position: absolute;
  bottom: 80px;
  /* 距离底部 80 像素 */
  right: 200px;
  /* 距离右侧 200 像素 */
}
</style>
