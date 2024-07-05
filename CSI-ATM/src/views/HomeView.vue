<script setup>
import inBalanceButton from "@/components/buttons/inBalanceButton.vue";
import outBalanceButton from "@/components/buttons/outBalanceButton.vue";
import transBalanceButton from "@/components/buttons/transBalanceButton.vue";
import adminButton from "@/components/buttons/adminButton.vue";
components: {
  inBalanceButton, outBalanceButton, transBalanceButton, adminButton;
}
</script>

<template>
  <div class="container">
    <div class="home-title">
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
  border: 2px solid #151414;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.home-title {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-size: 200%;
  text-align: center;
  margin-top: 30px; /* 调整顶部间距 */
  margin-bottom: 40px;
}

.user-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px; /* 调整按钮组容器的高度 */
}

.button-group {
  display: flex;
}

.button {
  margin: 0 15px; /* 调整按钮之间的间距 */
  padding: 10px 20px; /* 调整按钮的内边距 */
  font-size: 18px; /* 调整按钮字体大小 */
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.button:hover {
  background-color:  #007bff;
}

.admin-container {
  background-color: #4481c3;
  position: absolute;
  bottom: 80px;
  right: 200px; /* 调整管理员按钮的右侧距离 */
}
</style>
