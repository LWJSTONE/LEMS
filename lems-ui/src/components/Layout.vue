<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="220px" class="aside">
      <div class="logo">
        <h2>LEMS</h2>
        <p>实验设备管理系统</p>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <template v-for="menu in filteredMenus" :key="menu.path">
          <el-menu-item :index="menu.path">
            <el-icon><component :is="menu.icon" /></el-icon>
            <span>{{ menu.title }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- 顶部栏 -->
      <el-header class="header">
        <div class="header-left">
          <span class="page-title">{{ $route.meta.title }}</span>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ userStore.realName }} ({{ roleLabel }})
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="password">修改密码</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>

    <!-- 个人信息对话框 -->
    <el-dialog v-model="profileDialogVisible" title="个人信息" width="500px">
      <el-form :model="profileForm" label-width="90px">
        <el-form-item label="用户名">
          <el-input :model-value="userStore.userInfo.username" disabled />
        </el-form-item>
        <el-form-item label="角色">
          <el-tag :type="roleTagType" size="large">{{ roleLabel }}</el-tag>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="profileForm.realName" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="所属实验室">
          <el-input :model-value="userStore.userInfo.labName || '未分配'" disabled />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="profileDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="profileSaving" @click="saveProfile">保存</el-button>
      </template>
    </el-dialog>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="450px">
      <el-form :model="passwordForm" label-width="90px" :rules="passwordRules" ref="passwordFormRef">
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入旧密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码（至少6位）" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="passwordSaving" @click="savePassword">确认修改</el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { logout as logoutApi } from '@/api/auth'
import { updateProfile, changePassword } from '@/api/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const roleLabel = computed(() => {
  const map = { ADMIN: '管理员', TEACHER: '教师', STUDENT: '学生' }
  return map[userStore.roleType] || userStore.roleType
})

const roleTagType = computed(() => {
  const map = { ADMIN: 'danger', TEACHER: 'warning', STUDENT: '' }
  return map[userStore.roleType] || 'info'
})

const menus = [
  { path: '/dashboard', title: '首页仪表盘', icon: 'Odometer', roles: [] },
  { path: '/device/category', title: '设备分类管理', icon: 'Menu', roles: ['ADMIN'] },
  { path: '/device/list', title: '设备台账管理', icon: 'Monitor', roles: [] },
  { path: '/borrow/apply', title: '设备预约', icon: 'Calendar', roles: [] },
  { path: '/borrow/my', title: '我的借用', icon: 'Document', roles: [] },
  { path: '/borrow/approval', title: '借用审批', icon: 'Checked', roles: ['ADMIN', 'TEACHER'] },
  { path: '/borrow/overdue', title: '逾期管理', icon: 'Warning', roles: ['ADMIN', 'TEACHER'] },
  { path: '/system/user', title: '用户管理', icon: 'User', roles: ['ADMIN'] },
  { path: '/system/lab', title: '实验室管理', icon: 'OfficeBuilding', roles: ['ADMIN'] }
]

const filteredMenus = computed(() => {
  return menus.filter(menu => {
    if (menu.roles.length === 0) return true
    return menu.roles.includes(userStore.roleType)
  })
})

// ========== 个人信息对话框 ==========
const profileDialogVisible = ref(false)
const profileSaving = ref(false)
const profileForm = reactive({
  realName: '',
  phone: '',
  email: ''
})

const openProfileDialog = () => {
  profileForm.realName = userStore.userInfo.realName || ''
  profileForm.phone = userStore.userInfo.phone || ''
  profileForm.email = userStore.userInfo.email || ''
  profileDialogVisible.value = true
}

const saveProfile = async () => {
  if (!profileForm.realName) {
    ElMessage.warning('姓名不能为空')
    return
  }
  profileSaving.value = true
  try {
    await updateProfile(profileForm)
    await userStore.fetchProfile()
    ElMessage.success('个人信息修改成功')
    profileDialogVisible.value = false
  } catch (e) {
    console.error('修改个人信息失败', e)
  } finally {
    profileSaving.value = false
  }
}

// ========== 修改密码对话框 ==========
const passwordDialogVisible = ref(false)
const passwordSaving = ref(false)
const passwordFormRef = ref()
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const savePassword = async () => {
  try {
    await passwordFormRef.value.validate()
  } catch (e) { return }

  passwordSaving.value = true
  try {
    await changePassword({
      oldPassword: passwordForm.oldPassword,
      newPassword: passwordForm.newPassword
    })
    ElMessage.success('密码修改成功，请重新登录')
    passwordDialogVisible.value = false
    // 清空表单
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    // 退出登录
    try { await logoutApi() } catch (e) { /* ignore */ }
    userStore.logout()
    router.push('/login')
  } catch (e) {
    console.error('修改密码失败', e)
  } finally {
    passwordSaving.value = false
  }
}

// ========== 路由守卫 & 初始化 ==========
onMounted(async () => {
  if (userStore.isLoggedIn) {
    await userStore.fetchProfile()
  }
})

const handleCommand = async (command) => {
  if (command === 'profile') {
    openProfileDialog()
  } else if (command === 'password') {
    passwordDialogVisible.value = true
  } else if (command === 'logout') {
    try {
      await logoutApi()
    } catch (e) { /* ignore */ }
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.aside {
  background-color: #304156;
  overflow-y: auto;
}
.logo {
  padding: 20px;
  text-align: center;
  color: #fff;
}
.logo h2 {
  font-size: 24px;
  margin-bottom: 4px;
  letter-spacing: 4px;
}
.logo p {
  font-size: 12px;
  color: #bfcbd9;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.header-left .page-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
.header-right .user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-size: 14px;
}
.main {
  background: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
