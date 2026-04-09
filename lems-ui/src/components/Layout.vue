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
  </el-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { logout as logoutApi } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const roleLabel = computed(() => {
  const map = { ADMIN: '管理员', TEACHER: '教师', STUDENT: '学生' }
  return map[userStore.roleType] || userStore.roleType
})

const menus = [
  { path: '/dashboard', title: '首页仪表盘', icon: 'Odometer', roles: [] },
  { path: '/device/category', title: '设备分类管理', icon: 'Menu', roles: ['ADMIN'] },
  { path: '/device/list', title: '设备台账管理', icon: 'Monitor', roles: [] },
  { path: '/borrow/apply', title: '设备预约', icon: 'Calendar', roles: [] },
  { path: '/borrow/my', title: '我的借用', icon: 'Document', roles: [] },
  { path: '/borrow/approval', title: '借用审批', icon: 'Checked', roles: ['ADMIN', 'TEACHER'] },
  { path: '/system/user', title: '用户管理', icon: 'User', roles: ['ADMIN'] },
  { path: '/system/lab', title: '实验室管理', icon: 'OfficeBuilding', roles: ['ADMIN'] }
]

const filteredMenus = computed(() => {
  return menus.filter(menu => {
    if (menu.roles.length === 0) return true
    return menu.roles.includes(userStore.roleType)
  })
})

onMounted(async () => {
  if (userStore.isLoggedIn) {
    try {
      await userStore.fetchProfile()
    } catch (e) {
      userStore.logout()
      router.push('/login')
    }
  }
})

const handleCommand = async (command) => {
  if (command === 'profile') {
    ElMessage.info('个人信息功能开发中')
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
