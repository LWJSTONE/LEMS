<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">LEMS</h2>
      <p class="login-subtitle">实验设备管理系统</p>
      <el-tabs v-model="activeTab" class="login-tabs">
        <el-tab-pane label="登录" name="login">
          <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="0">
            <el-form-item prop="username">
              <el-input v-model="loginForm.username" prefix-icon="User" placeholder="请输入用户名" size="large" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="loginForm.password" prefix-icon="Lock" placeholder="请输入密码"
                type="password" show-password size="large" @keyup.enter="handleLogin" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" style="width:100%" :loading="loading" @click="handleLogin">
                登 录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="0">
            <el-form-item prop="username">
              <el-input v-model="registerForm.username" prefix-icon="User" placeholder="用户名（学号/工号）" size="large" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="registerForm.password" prefix-icon="Lock" placeholder="密码" type="password" show-password size="large" />
            </el-form-item>
            <el-form-item prop="realName">
              <el-input v-model="registerForm.realName" prefix-icon="UserFilled" placeholder="真实姓名" size="large" />
            </el-form-item>
            <el-form-item prop="roleType">
              <el-select v-model="registerForm.roleType" placeholder="角色" size="large" style="width:100%">
                <el-option label="学生" value="STUDENT" />
                <el-option label="教师" value="TEACHER" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="success" size="large" style="width:100%" :loading="loading" @click="handleRegister">
                注 册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <div v-if="import.meta.env.DEV" class="demo-accounts">
        <p>演示账号: admin/admin123 | teacher01/admin123 | student01/admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { login, register } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const activeTab = ref('login')
const loading = ref(false)

const loginForm = ref({ username: '', password: '' })
const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const registerForm = ref({ username: '', password: '', realName: '', roleType: 'STUDENT' })
const registerRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  realName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  roleType: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await login(loginForm.value)
    if (res.code === 200) {
      userStore.setToken(res.data.token)
      userStore.setUserInfo(res.data)
      ElMessage.success('登录成功')
      router.push('/dashboard')
    }
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  loading.value = true
  try {
    const res = await register(registerForm.value)
    if (res.code === 200) {
      ElMessage.success('注册成功，请登录')
      activeTab.value = 'login'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 420px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,.3);
}
.login-title {
  text-align: center;
  font-size: 32px;
  color: #303133;
  letter-spacing: 6px;
  margin-bottom: 4px;
}
.login-subtitle {
  text-align: center;
  font-size: 14px;
  color: #909399;
  margin-bottom: 20px;
}
.demo-accounts {
  margin-top: 16px;
  text-align: center;
  font-size: 12px;
  color: #909399;
}
</style>
