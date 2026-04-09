import request from '@/utils/request'

// 获取分类树
export function getCategoryTree() {
  return request({
    url: '/v1/device/categories/tree',
    method: 'get'
  })
}

// 新增分类
export function addCategory(data) {
  return request({
    url: '/v1/device/categories',
    method: 'post',
    data
  })
}

// 修改分类
export function updateCategory(data) {
  return request({
    url: '/v1/device/categories',
    method: 'put',
    data
  })
}

// 删除分类
export function deleteCategory(id) {
  return request({
    url: `/v1/device/categories/${id}`,
    method: 'delete'
  })
}

// 分页查询设备列表
export function getDevicePage(params) {
  return request({
    url: '/v1/device/info/page',
    method: 'get',
    params
  })
}

// 获取设备详情
export function getDeviceById(id) {
  return request({
    url: `/v1/device/info/${id}`,
    method: 'get'
  })
}

// 新增设备
export function addDevice(data) {
  return request({
    url: '/v1/device/info',
    method: 'post',
    data
  })
}

// 修改设备
export function updateDevice(data) {
  return request({
    url: '/v1/device/info',
    method: 'put',
    data
  })
}

// 删除设备
export function deleteDevice(id) {
  return request({
    url: `/v1/device/info/${id}`,
    method: 'delete'
  })
}

// 更新设备状态
export function updateDeviceStatus(id, status) {
  return request({
    url: `/v1/device/info/${id}/status`,
    method: 'put',
    params: { status }
  })
}

// 新增维修记录
export function addMaintenance(data) {
  return request({
    url: '/v1/device/maintenance',
    method: 'post',
    data
  })
}

// 获取维修记录分页
export function getMaintenancePage(params) {
  return request({
    url: '/v1/device/maintenance/page',
    method: 'get',
    params
  })
}

// 更新维修状态
export function updateMaintenanceStatus(id, status) {
  return request({
    url: `/v1/device/maintenance/${id}/status`,
    method: 'put',
    params: { status }
  })
}
