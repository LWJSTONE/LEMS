import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('@/components/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '首页仪表盘', icon: 'Odometer' }
      },
      {
        path: 'device/category',
        name: 'DeviceCategory',
        component: () => import('@/views/device/category/index.vue'),
        meta: { title: '设备分类管理', icon: 'Menu', roles: ['ADMIN'] }
      },
      {
        path: 'device/list',
        name: 'DeviceList',
        component: () => import('@/views/device/list/index.vue'),
        meta: { title: '设备台账管理', icon: 'Monitor' }
      },
      {
        path: 'device/detail/:id',
        name: 'DeviceDetail',
        component: () => import('@/views/device/detail/index.vue'),
        meta: { title: '设备详情', hidden: true }
      },
      {
        path: 'borrow/apply',
        name: 'BorrowApply',
        component: () => import('@/views/borrow/apply/index.vue'),
        meta: { title: '设备预约', icon: 'Calendar' }
      },
      {
        path: 'borrow/my',
        name: 'MyBorrow',
        component: () => import('@/views/borrow/my/index.vue'),
        meta: { title: '我的借用', icon: 'Document' }
      },
      {
        path: 'borrow/approval',
        name: 'BorrowApproval',
        component: () => import('@/views/borrow/approval/index.vue'),
        meta: { title: '借用审批', icon: 'Checked', roles: ['ADMIN', 'TEACHER'] }
      },
      {
        path: 'system/user',
        name: 'SystemUser',
        component: () => import('@/views/system/user/index.vue'),
        meta: { title: '用户管理', icon: 'User', roles: ['ADMIN'] }
      },
      {
        path: 'system/lab',
        name: 'SystemLab',
        component: () => import('@/views/system/lab/index.vue'),
        meta: { title: '实验室管理', icon: 'OfficeBuilding', roles: ['ADMIN'] }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = (to.meta.title ? to.meta.title + ' - ' : '') + 'LEMS实验设备管理系统'

  const token = localStorage.getItem('token')
  if (to.path === '/login') {
    if (token) {
      next('/dashboard')
    } else {
      next()
    }
  } else {
    if (!token) {
      next('/login')
    } else {
      // 角色权限检查
      const userStore = useUserStore()
      const roles = to.meta.roles
      if (roles && roles.length > 0 && !roles.includes(userStore.roleType)) {
        next('/dashboard')
      } else {
        next()
      }
    }
  }
})

export default router
