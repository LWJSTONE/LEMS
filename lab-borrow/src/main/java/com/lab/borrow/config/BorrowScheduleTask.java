package com.lab.borrow.config;

import com.lab.borrow.service.BorrowService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;

/**
 * 定时任务：扫描逾期借用记录
 */
@Slf4j
@Component
public class BorrowScheduleTask {

    @Resource
    private BorrowService borrowService;

    /**
     * 每小时执行一次，标记逾期未归还的借用记录
     */
    @Scheduled(cron = "0 0 * * * ?")
    public void checkOverdue() {
        log.info("开始执行逾期借用记录扫描...");
        try {
            borrowService.checkOverdueRecords();
        } catch (Exception e) {
            log.error("逾期扫描任务执行失败: ", e);
        }
    }
}
