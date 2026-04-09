package com.lab.borrow.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.common.annotation.RequireRole;
import com.lab.common.result.R;
import com.lab.borrow.entity.BorrowRecord;
import com.lab.borrow.service.BorrowService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.Map;

/**
 * 借用预约控制器
 */
@RestController
@RequestMapping("/api/v1/borrow")
public class BorrowController {

    @Resource
    private BorrowService borrowService;

    /**
     * 提交借用申请
     */
    @PostMapping("/apply")
    public R<Void> apply(@RequestBody BorrowRecord record,
                          @RequestHeader("X-User-Id") Long userId) {
        borrowService.apply(record, userId);
        return R.ok();
    }

    /**
     * 我的申请记录
     */
    @GetMapping("/my/list")
    public R<Page<BorrowRecord>> myList(
            @RequestHeader("X-User-Id") Long userId,
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Integer status) {
        return R.ok(borrowService.myList(userId, current, size, status));
    }

    /**
     * 待审批列表
     */
    @RequireRole({"ADMIN", "TEACHER"})
    @GetMapping("/pending/list")
    public R<Page<BorrowRecord>> pendingList(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size) {
        return R.ok(borrowService.pendingList(current, size));
    }

    /**
     * 审批通过
     */
    @RequireRole({"ADMIN", "TEACHER"})
    @PutMapping("/approve/{id}")
    public R<Void> approve(@PathVariable Long id,
                            @RequestHeader("X-User-Id") Long userId) {
        borrowService.approve(id, userId);
        return R.ok();
    }

    /**
     * 驳回申请
     */
    @RequireRole({"ADMIN", "TEACHER"})
    @PutMapping("/reject/{id}")
    public R<Void> reject(@PathVariable Long id,
                           @RequestHeader("X-User-Id") Long userId,
                           @RequestBody Map<String, String> body) {
        String reason = body.get("reason");
        borrowService.reject(id, userId, reason);
        return R.ok();
    }

    /**
     * 取消申请
     */
    @PutMapping("/cancel/{id}")
    public R<Void> cancel(@PathVariable Long id,
                           @RequestHeader("X-User-Id") Long userId) {
        borrowService.cancel(id, userId);
        return R.ok();
    }

    /**
     * 归还确认
     */
    @PutMapping("/return/{id}")
    public R<Void> returnDevice(@PathVariable Long id,
                                 @RequestHeader("X-User-Id") Long userId,
                                 @RequestBody(required = false) Map<String, String> body) {
        String remark = body != null ? body.get("remark") : null;
        borrowService.returnDevice(id, userId, remark);
        return R.ok();
    }

    /**
     * 逾期未归还列表
     */
    @RequireRole({"ADMIN", "TEACHER"})
    @GetMapping("/overdue/list")
    public R<Page<BorrowRecord>> overdueList(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size) {
        return R.ok(borrowService.overdueList(current, size));
    }
}
