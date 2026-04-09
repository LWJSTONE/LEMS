package com.lab.common.result;

import lombok.Data;

import java.io.Serializable;
import java.util.List;

/**
 * 分页查询返回结构
 */
@Data
public class PageResult<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    /** 数据列表 */
    private List<T> records;

    /** 总记录数 */
    private long total;

    /** 每页大小 */
    private long size;

    /** 当前页码 */
    private long current;

    public PageResult() {
    }

    public PageResult(List<T> records, long total, long size, long current) {
        this.records = records;
        this.total = total;
        this.size = size;
        this.current = current;
    }
}
