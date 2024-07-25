<template>
  <div id="app">
    <!-- 使用 Element UI 的容器布局组件 -->
    <el-container style="height: 100vh;">
      <!-- 侧边栏组件 -->
      <Sidebar />
      <el-container>
        <!-- 头部区域，显示标题“多智能体客服” -->
        <el-header class="header">多智能体客服</el-header>
        <!-- 主内容区域 -->
        <el-main class="main">
          <!-- 路由视图，用于显示路由对应的组件 -->
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Sidebar from '@/components/MainSidebar.vue'; // 导入侧边栏组件

export default {
  components: {
    Sidebar, // 注册侧边栏组件
  },
};
</script>

<style>
/* 根元素的样式 */
#app {
  font-family: 'Roboto', sans-serif; /* 更改字体族为 Roboto */
  -webkit-font-smoothing: antialiased; /* Webkit 引擎的抗锯齿效果 */
  -moz-osx-font-smoothing: grayscale; /* Mozilla 引擎的抗锯齿效果 */
  text-align: center; /* 文本居中 */
  color: #2c3e50; /* 字体颜色 */
}

/* 头部区域的样式 */
.header {
  background-color: #1b6cbe; /* 背景颜色 */
  color: white; /* 字体颜色 */
  text-align: center; /* 文本居中 */
  padding: 15px; /* 内边距 */
  font-size: 20px; /* 更改字体大小 */
  font-weight: 700; /* 更改字体粗细 */
  font-family: 'Arial', sans-serif; /* 更改字体族 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}

/* 主内容区域的样式 */
.main {
  flex: 1; /* 使主内容区域占满剩余空间 */
  display: flex; /* 使用弹性盒子布局 */
  flex-direction: column; /* 垂直方向排列 */
  overflow: hidden; /* 隐藏超出区域的内容 */
}
</style>
