import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/v1/auth/login',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/v1/auth/register',
    method: 'post',
    data
  })
}

// 登出
export function logout() {
  return request({
    url: '/v1/auth/logout',
    method: 'post'
  })
}
