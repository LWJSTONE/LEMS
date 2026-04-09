package com.lab.borrow.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.borrow.entity.BorrowRecord;

import java.util.Map;

/**
 * 借用预约服务接口
 */
public interface BorrowService {

    /**
     * 提交借用申请（扣减available_quantity预占库存）
     */
    void apply(BorrowRecord record, Long userId);

    /**
     * 我的申请记录
     */
    Page<BorrowRecord> myList(Long userId, int pageNum, int pageSize, Integer status);

    /**
     * 待审批列表（教师/管理员）
     */
    Page<BorrowRecord> pendingList(int pageNum, int pageSize);

    /**
     * 审批通过（库存已预占，无需再次扣减）
     */
    void approve(Long id, Long approverId);

    /**
     * 驳回申请（释放预占库存）
     */
    void reject(Long id, Long approverId, String reason);

    /**
     * 取消申请（释放预占库存）
     */
    void cancel(Long id, Long userId);

    /**
     * 归还确认（库存回增）
     */
    void returnDevice(Long id, Long userId, String remark);

    /**
     * 逾期未归还列表
     */
    Page<BorrowRecord> overdueList(int pageNum, int pageSize);

    /**
     * 定时任务：扫描并标记逾期借用记录
     */
    void checkOverdueRecords();
}
