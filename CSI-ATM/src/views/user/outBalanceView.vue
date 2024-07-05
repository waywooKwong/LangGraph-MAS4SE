<template>
 <div class="container">

  <div class="deposit-title">
     取款界面
  </div>
  
  <main>
    <OutBalance />
  </main>
  </div>
  
</template>

<script>
import outBalance from "@/components/outBalance.vue";

export default {
  components: {
    outBalance,
  },
  setup() {},
};
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