<template>
  转账界面
  <TransBalance />
</template>
<script>
import transBalance from "@/components/transBalance.vue";
import { onMounted } from 'vue'; 

export default {
  components: {
    transBalance,
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
