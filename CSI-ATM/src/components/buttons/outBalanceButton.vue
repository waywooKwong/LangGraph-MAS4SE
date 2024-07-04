<!-- 取款功能按钮，挂在HomeView.vue中 -->
<template>
  <div class="out">
    <router-link to="/outBalanceView">
      <button class="button">取款</button>
    </router-link>
  </div>
</template>
<script></script>
<style scoped>
.button {
  background-color: #007bff;
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
