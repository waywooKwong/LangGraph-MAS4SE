<template>
  <div class="container">

  <div class="deposit-title">
    存款界面
  </div>
  
  <main>
    <inBalance />
  </main>
  </div>
</template>
<script>
import inBalance from "@/components/inBalance.vue";
import { onMounted } from 'vue'; 

export default {
  components: {
    inBalance
  },
  setup() {
    // 设置图标
    onMounted(() => {
      setFavicon('/icons/favicon-balance.ico');
    });
  },
};
function setFavicon(href) {
  let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
  link.type = 'image/x-icon';
  link.rel = 'shortcut icon';
  link.href = href;
  document.getElementsByTagName('head')[0].appendChild(link);
}
</script>
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
.deposit-title{
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
 font-size: 200%;
  margin-right: 200px;
  margin-bottom: 50px;
}
</style>
