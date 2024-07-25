<template>
  
  <router-view />
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



/* 主内容区域的样式 */

</style>
