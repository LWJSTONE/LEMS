import request from '@/utils/request'

// 获取个人信息
export function getProfile() {
  return request({
    url: '/v1/user/profile',
    method: 'get'
  })
}

// 修改个人信息
export function updateProfile(data) {
  return request({
    url: '/v1/user/profile',
    method: 'put',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/v1/user/password',
    method: 'put',
    data
  })
}

// 分页查询用户列表
export function getUserPage(params) {
  return request({
    url: '/v1/user/page',
    method: 'get',
    params
  })
}

// 更新用户状态
export function updateUserStatus(id, status) {
  return request({
    url: `/v1/user/${id}/status`,
    method: 'put',
    params: { status }
  })
}

// 获取实验室列表
export function getLabList() {
  return request({
    url: '/v1/user/lab/list',
    method: 'get'
  })
}

// 获取实验室成员
export function getLabMembers(params) {
  return request({
    url: '/v1/user/lab/members',
    method: 'get',
    params
  })
}

// 新增实验室
export function addLab(data) {
  return request({
    url: '/v1/user/lab',
    method: 'post',
    data
  })
}

// 修改实验室
export function updateLab(data) {
  return request({
    url: '/v1/user/lab',
    method: 'put',
    data
  })
}
