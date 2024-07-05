<template>
  取款界面
  <OutBalance />
</template>
<script>
import outBalance from "@/components/outBalance.vue";
import { onMounted } from 'vue'; 

export default {
  components: {
    outBalance
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
<style scoped></style>
