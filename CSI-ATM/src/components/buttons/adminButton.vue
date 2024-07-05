<template>
  <div class="admin">
    <el-button plain @click="showDialog = true">
      管理员登录
    </el-button>

    <el-dialog
      v-model="showDialog"
      title="管理员登录"
      width="30%"
      :before-close="handleClose"
    >
      <form @submit.prevent="adminLogin">
        <el-form label-width="80px">
          <el-form-item label="账号：" required>
            <el-input v-model="adminData.account"></el-input>
          </el-form-item>
          <el-form-item label="密码：" required>
            <el-input type="password" v-model="adminData.password"></el-input>
          </el-form-item>
        </el-form>
      </form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDialog = false">取消</el-button>
          <el-button type="primary" @click="adminLogin">登录</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { ElMessageBox } from 'element-plus';
import router from '@/router';

const showDialog = ref(false);
const adminData = ref({
  account: '',
  password: ''
});

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('确定关闭对话框？')
    .then(() => {
      done();
    })
    .catch(() => {
      // 捕获错误
    });
};

const adminLogin = () => {
  const params = new URLSearchParams();
  params.append('account', adminData.value.account);
  params.append('password', adminData.value.password);

  axios.get('http://localhost:3000/AdminLogin', { params })
    .then(response => {
      if (response.data === 'true') {
        // 登录成功的处理
        alert('登录成功');
        // 使用 Vue Router 进行路由跳转
        router.push('/adminView'); // 假设 router 是你的 Vue Router 实例
      } else {
        alert('管理员账号或密码错误');
      }
    })
    .catch(error => {
      console.error(error);
      alert('登录失败，请重试');
    });
};

</script>

<style scoped>
.el-button{
     color: #000;
      border: none;
      border-radius: 16px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 18px;
}

</style>
