<template>
  <el-aside width="200px" class="sidebar">
    <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" @select="handleSelect">
      <el-menu-item
        index="ChatView"
        :class="{'active-menu-item': activeMenu === 'ChatView', 'menu-item': true}"
      >
        <span>对话</span>
      </el-menu-item>
      <el-menu-item
        index="AgentMap"
        :class="{'active-menu-item': activeMenu === 'AgentMap', 'menu-item': true}"
      >
        <span>自定义智能体</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  name: 'MainSidebar',
  data() {
    return {
      activeMenu: this.$route.name, // 初始化为当前路由的名称
    };
  },
  watch: {
    $route(to) {
      this.activeMenu = to.name; // 路由变化时更新 activeMenu
    },
  },
  methods: {
    handleSelect(key) {
      if (this.activeMenu === key) {
        // 当前已经在该路由，避免重复导航
        return;
      }

      this.activeMenu = key;

      this.$router.push({ name: key }).catch(err => {
        if (err.name !== 'NavigationDuplicated') {
          console.error(err); // 处理其他导航错误
        }
      });
    },
  },
};
</script>

<style scoped>
.sidebar {
  background-color: #b3b0b0;
  border-right: 1px solid #dcdfe6;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.el-menu {
  border-right: none;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  margin: 5px 10px;
  border-radius: 5px;
  background: linear-gradient(145deg, #ffffff, #e6e6e6);
  box-shadow: 4px 4px 8px #d1d1d1, -4px -4px 8px #ffffff;
  transition: all 0.2s ease-in-out;
}

.active-menu-item {
  background: linear-gradient(145deg, #d1d1d1, #bfbfbf);
  box-shadow: 4px 4px 8px #a0a0a0, -4px -4px 8px #d0d0d0;
}

.menu-item:hover {
  background: linear-gradient(145deg, #e6e6e6, #ffffff);
  box-shadow: 4px 4px 8px #c0c0c0, -4px -4px 8px #f0f0f0;
}

.menu-item span {
  font-weight: bold;
  text-align: center;
}
</style>
