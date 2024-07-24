<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <Sidebar />
      <el-container>
        <el-header class="header">主页面标题</el-header>
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
</style>
