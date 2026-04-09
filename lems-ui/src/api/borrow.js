import request from '@/utils/request'

// 提交借用申请
export function applyBorrow(data) {
  return request({
    url: '/v1/borrow/apply',
    method: 'post',
    data
  })
}

// 我的申请记录
export function getMyBorrowList(params) {
  return request({
    url: '/v1/borrow/my/list',
    method: 'get',
    params
  })
}

// 待审批列表
export function getPendingList(params) {
  return request({
    url: '/v1/borrow/pending/list',
    method: 'get',
    params
  })
}

// 审批通过
export function approveBorrow(id) {
  return request({
    url: `/v1/borrow/approve/${id}`,
    method: 'put'
  })
}

// 驳回申请
export function rejectBorrow(id, reason) {
  return request({
    url: `/v1/borrow/reject/${id}`,
    method: 'put',
    data: { reason }
  })
}

// 取消申请
export function cancelBorrow(id) {
  return request({
    url: `/v1/borrow/cancel/${id}`,
    method: 'put'
  })
}

// 归还确认
export function returnDevice(id, remark) {
  return request({
    url: `/v1/borrow/return/${id}`,
    method: 'put',
    data: { remark }
  })
}

// 逾期列表
export function getOverdueList(params) {
  return request({
    url: '/v1/borrow/overdue/list',
    method: 'get',
    params
  })
}
