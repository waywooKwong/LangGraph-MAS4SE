<template>
    <div class="custom-agent">
      <h3>自定义智能体</h3>
      <el-button
      class="delete-button"
      type="danger"
      icon="el-icon-close"
      circle
      size="mini"
      @click="handleDelete"
    ></el-button>
      <el-form :model="form" label-width="120px">
        <el-form-item label="智能体名称">
          <el-input v-model="form.name" placeholder="请输入智能体名称"></el-input>
        </el-form-item>
        <el-form-item label="智能体描述">
          <el-input type="textarea" v-model="form.description" placeholder="请输入智能体描述"></el-input>
        </el-form-item>
      </el-form>
      <div class="text-display">
        <!-- 文字显示框，内容待后端数据填充 -->
        <p>这里显示从后端传来的文字</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CustomAgent',
    data() {
      return {
        form: {
          name: '',
          description: ''
        }
      };
    },
  };
  </script>
  
  <style scoped>
  .custom-agent {
    padding: 20px;
    border: 1px solid #dcdfe6;
    border-radius: 5px;
    background-color: #f9f9f9;
  }
  
  .delete-button {
  position: absolute;
  top: 5px;
  right: 5px;
}

  .text-display {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #dcdfe6;
    border-radius: 5px;
    background-color: #ffffff;
  }
  </style>
  