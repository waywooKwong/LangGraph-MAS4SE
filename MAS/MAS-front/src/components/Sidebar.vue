<template>
  <el-aside width="200px" class="sidebar">
    <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" @select="handleSelect">
      <el-menu-item
        index="chat"
        :class="{'active-menu-item': activeMenu === 'chat', 'menu-item': true}"
      >
        <i class="el-icon-chat-line-round"></i>
        <span>对话</span>
      </el-menu-item>
      <el-menu-item
        index="agent-map"
        :class="{'active-menu-item': activeMenu === 'agent-map', 'menu-item': true}"
      >
        <i class="el-icon-s-help"></i>
        <span>自定义智能体</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  data() {
    return {
      activeMenu: this.$route.name,
    };
  },
  watch: {
    $route(to) {
      this.activeMenu = to.name;
    },
  },
  methods: {
    handleSelect(key) {
      if (key === 'chat') {
        this.activeMenu = 'chat';
        this.$router.push({ name: 'ChatView' });
      } else if (key === 'agent-map') {
        this.activeMenu = 'agent-map';
        this.$router.push({ name: 'AgentMap' });
      }
    },
  },
};
</script>

<style scoped>
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
