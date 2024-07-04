<!-- 存款功能按钮，挂在HomeView.vue中 -->
<template>
  <div class="in">
    <router-link to="/inBalanceView">
      <button class="button">存款</button>
    </router-link>
  </div>
</template>
<script>
export default {
  setup() {},
};
</script>
<style scoped>
.button {
  background-color:#007bff;
  border: none;
  border-radius: 4px;
  color: white;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}

</style>
