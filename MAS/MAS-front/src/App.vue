<template>
  <div id="app">
    <el-container style="height: 100vh">
      <!-- 头部区域，显示标题和侧边栏切换按钮 -->
      <el-header class="header">
        <el-button type="primary" class="toggle-button" @click="toggleDrawer"> open </el-button>
        多智能体客服
      </el-header>
      <el-container>
        <!-- 主内容区域 -->
        <el-main class="main">
          <!-- 路由视图，用于显示路由对应的组件 -->
          <router-view />
        </el-main>
        <!-- 侧边栏组件 -->
        <el-drawer
          :model-value="drawerVisible"
          title="I am the title"
          :with-header="false"
          @update:model-value="drawerVisible = $event"
        >
          <span>Hi there!</span>

          <Sidebar />
        </el-drawer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Sidebar from '@/components/MainSidebar.vue' // 导入侧边栏组件

export default {
  components: {
    Sidebar // 注册侧边栏组件
  },
  data() {
    return {
      drawerVisible: false // 控制侧边栏显示的变量
    }
  },
  methods: {
    toggleDrawer() {
      this.drawerVisible = !this.drawerVisible // 切换侧边栏显示状态
    }
  }
}
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
  background-color: #409eff; /* 背景颜色#409EFF */
  color: white; /* 字体颜色 */
  display: flex; /* 使用弹性盒子布局 */
  justify-content: center; /* 水平方向居中 */
  align-items: center; /* 垂直方向居中 */
  height: 60px; /* 设置固定高度 */
  font-size: 20px; /* 更改字体大小 */
  font-weight: 700; /* 更改字体粗细 */
  font-family: 'Arial', sans-serif; /* 更改字体族 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  position: relative; /* 使按钮可以绝对定位 */
}

/* 控制侧边栏显示的按钮样式 */
.toggle-button {
  position: absolute; /* 绝对定位 */
  left: 20px; /* 左边距 */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 垂直居中 */
}

/* 主内容区域的样式 */
.main {
  flex: 1; /* 使主内容区域占满剩余空间 */
  display: flex; /* 使用弹性盒子布局 */
  flex-direction: column; /* 垂直方向排列 */
  overflow: hidden; /* 隐藏超出区域的内容 */
}
</style>
