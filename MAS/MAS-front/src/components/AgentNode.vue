<template>
    <div class="agent-node">
      <input v-model="name" placeholder="智能体名称" />
    </div>
  </template>
  
  <script>
  export default {
    name: 'AgentNode',
    props: {
      nodeId: String,
      graph: Object,
    },
    data() {
      return {
        name: '',
      };
    },
  };
  </script>
  
  <style scoped>
  .agent-node {
    width: 100%;
    height: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: white;
    box-sizing: border-box;
    z-index: 10;
  }
  
  input {
    width: calc(100% - 20px);
    margin: 10px 0;
    padding: 5px;
    box-sizing: border-box;
  }
  </style>
  