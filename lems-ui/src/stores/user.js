import { defineStore } from 'pinia'
import { getProfile } from '@/api/user'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}')
  }),

  getters: {
    isLoggedIn: state => !!state.token,
    username: state => state.userInfo.username || '',
    realName: state => state.userInfo.realName || '',
    roleType: state => state.userInfo.roleType || '',
    isAdmin: state => state.userInfo.roleType === 'ADMIN',
    isTeacher: state => state.userInfo.roleType === 'TEACHER',
    isStudent: state => state.userInfo.roleType === 'STUDENT'
  },

  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },

    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },

    async fetchProfile() {
      try {
        const res = await getProfile()
        if (res.code === 200) {
          this.setUserInfo(res.data)
        }
      } catch (e) {
        console.error('获取用户信息失败:', e)
        // 不抛出异常，避免影响上层调用流程
      }
    },

    logout() {
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  }
})
