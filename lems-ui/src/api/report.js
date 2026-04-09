import request from '@/utils/request'

// 获取仪表盘统计数据
export function getDashboardStats() {
  return request({
    url: '/v1/report/dashboard',
    method: 'get'
  })
}

// 设备使用率Top10
export function getDeviceUsageTop() {
  return request({
    url: '/v1/report/device/usage/top',
    method: 'get'
  })
}

// 月度借用趋势
export function getMonthlyTrend() {
  return request({
    url: '/v1/report/borrow/trend',
    method: 'get'
  })
}
