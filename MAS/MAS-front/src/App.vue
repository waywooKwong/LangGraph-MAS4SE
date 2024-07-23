<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <Sidebar />
      <el-container>
        <el-header class="header">ChatGPT UI</el-header>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Sidebar from '@/components/MainSidebar.vue';

export default {
  components: {
    Sidebar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.el-container {
  height: 100vh;
}

.header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  padding: 15px;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar {
  background-color: #f4f4f4;
  border-right: 1px solid #dcdfe6;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.el-menu {
  border-right: none;
}

.el-menu-item {
  display: flex;
  align-items: center;
  padding: 10px;
}

.el-menu-item i {
  margin-right: 10px;
}
</style>
