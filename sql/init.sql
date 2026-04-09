-- =============================================================
-- LEMS - 实验设备管理系统 数据库初始化脚本
-- 数据库: lab_device_mgt
-- 字符集: utf8mb4
-- =============================================================

CREATE DATABASE IF NOT EXISTS `lab_device_mgt` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE `lab_device_mgt`;

-- =============================================================
-- 表1: sys_user (系统用户表)
-- =============================================================
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
    `id` BIGINT NOT NULL COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '学号/工号',
    `password_hash` VARCHAR(100) NOT NULL COMMENT 'BCrypt密文',
    `real_name` VARCHAR(50) NOT NULL COMMENT '真实姓名',
    `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    `email` VARCHAR(50) DEFAULT NULL COMMENT '邮箱',
    `role_type` VARCHAR(20) NOT NULL COMMENT 'ADMIN/TEACHER/STUDENT',
    `lab_id` BIGINT DEFAULT NULL COMMENT '所属实验室ID',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '0禁用/1启用',
    `deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    KEY `idx_role_type` (`role_type`),
    KEY `idx_lab_id` (`lab_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户表';

-- =============================================================
-- 表2: lab_info (实验室/部门信息表)
-- =============================================================
DROP TABLE IF EXISTS `lab_info`;
CREATE TABLE `lab_info` (
    `id` BIGINT NOT NULL COMMENT '实验室ID',
    `name` VARCHAR(100) NOT NULL COMMENT '实验室名称',
    `location` VARCHAR(255) DEFAULT NULL COMMENT '具体位置',
    `manager_id` BIGINT DEFAULT NULL COMMENT '负责人ID(sys_user.id)',
    `contact_phone` VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '0关闭/1开放',
    `deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_manager` (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实验室信息表';

-- =============================================================
-- 表3: device_category (设备分类表)
-- =============================================================
DROP TABLE IF EXISTS `device_category`;
CREATE TABLE `device_category` (
    `id` BIGINT NOT NULL COMMENT '分类ID',
    `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
    `parent_id` BIGINT DEFAULT 0 COMMENT '父级ID',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序',
    `deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备分类表';

-- =============================================================
-- 表4: device_info (设备台账表)
-- =============================================================
DROP TABLE IF EXISTS `device_info`;
CREATE TABLE `device_info` (
    `id` BIGINT NOT NULL COMMENT '设备ID',
    `code` VARCHAR(50) NOT NULL COMMENT '设备唯一编号/资产号',
    `name` VARCHAR(100) NOT NULL COMMENT '设备名称',
    `model` VARCHAR(100) DEFAULT NULL COMMENT '规格型号',
    `category_id` BIGINT DEFAULT NULL COMMENT '分类ID',
    `lab_id` BIGINT DEFAULT NULL COMMENT '所属实验室ID',
    `total_quantity` INT NOT NULL DEFAULT 1 COMMENT '总数量',
    `available_quantity` INT NOT NULL DEFAULT 1 COMMENT '当前可用数量',
    `unit` VARCHAR(20) DEFAULT '台' COMMENT '单位(台/套)',
    `price` DECIMAL(12,2) DEFAULT NULL COMMENT '单价',
    `purchase_date` DATE DEFAULT NULL COMMENT '购置日期',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0正常/1维修/2报废/3外借',
    `location_detail` VARCHAR(255) DEFAULT NULL COMMENT '存放具体位置(柜号)',
    `description` TEXT DEFAULT NULL COMMENT '备注',
    `version` INT NOT NULL DEFAULT 0 COMMENT '乐观锁版本号',
    `deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`code`),
    KEY `idx_lab_category` (`lab_id`, `category_id`),
    KEY `idx_status` (`status`),
    KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备台账表';

-- =============================================================
-- 表5: borrow_record (借用预约记录表)
-- =============================================================
DROP TABLE IF EXISTS `borrow_record`;
CREATE TABLE `borrow_record` (
    `id` BIGINT NOT NULL COMMENT '申请单号',
    `device_id` BIGINT NOT NULL COMMENT '设备ID',
    `user_id` BIGINT NOT NULL COMMENT '借用人ID',
    `purpose` VARCHAR(255) DEFAULT NULL COMMENT '用途说明',
    `borrow_quantity` INT NOT NULL DEFAULT 1 COMMENT '借用数量',
    `start_time` DATETIME NOT NULL COMMENT '预计借用开始时间',
    `end_time` DATETIME NOT NULL COMMENT '预计归还时间',
    `actual_return_time` DATETIME DEFAULT NULL COMMENT '实际归还时间',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0待审批/1已批准/2已归还/3已逾期/4已驳回/5已取消',
    `approver_id` BIGINT DEFAULT NULL COMMENT '审批人ID',
    `approve_time` DATETIME DEFAULT NULL COMMENT '审批时间',
    `reject_reason` VARCHAR(255) DEFAULT NULL COMMENT '驳回理由',
    `return_remark` VARCHAR(255) DEFAULT NULL COMMENT '归还备注(损坏情况)',
    `version` INT NOT NULL DEFAULT 0 COMMENT '乐观锁',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_status` (`user_id`, `status`),
    KEY `idx_device_status` (`device_id`, `status`),
    KEY `idx_end_time` (`end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='借用预约记录表';

-- =============================================================
-- 表6: device_maintenance (维修记录表)
-- =============================================================
DROP TABLE IF EXISTS `device_maintenance`;
CREATE TABLE `device_maintenance` (
    `id` BIGINT NOT NULL COMMENT '维修记录ID',
    `device_id` BIGINT NOT NULL COMMENT '设备ID',
    `report_user_id` BIGINT NOT NULL COMMENT '报修人ID',
    `fault_desc` VARCHAR(500) DEFAULT NULL COMMENT '故障描述',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0待处理/1维修中/2已修复/3无法修复',
    `cost` DECIMAL(10,2) DEFAULT NULL COMMENT '维修费用',
    `repair_company` VARCHAR(100) DEFAULT NULL COMMENT '维修厂商',
    `finish_time` DATETIME DEFAULT NULL COMMENT '修复时间',
    `deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_device_status` (`device_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='维修记录表';

-- =============================================================
-- 表7: sys_dict (数据字典)
-- =============================================================
DROP TABLE IF EXISTS `sys_dict`;
CREATE TABLE `sys_dict` (
    `dict_type` VARCHAR(50) NOT NULL COMMENT '类型',
    `dict_code` VARCHAR(50) NOT NULL COMMENT '编码',
    `dict_label` VARCHAR(100) NOT NULL COMMENT '标签',
    PRIMARY KEY (`dict_type`, `dict_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据字典表';

-- =============================================================
-- 初始化数据
-- =============================================================

-- 初始管理员密码: admin123 (BCrypt加密)
INSERT INTO `sys_user` (`id`, `username`, `password_hash`, `real_name`, `phone`, `email`, `role_type`, `status`) VALUES
(1, 'admin', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '系统管理员', '13800000001', 'admin@lab.edu.cn', 'ADMIN', 1),
(2, 'teacher01', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '张老师', '13800000002', 'teacher@lab.edu.cn', 'TEACHER', 1),
(3, 'student01', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '李同学', '13800000003', 'student@lab.edu.cn', 'STUDENT', 1);

-- 初始实验室
INSERT INTO `lab_info` (`id`, `name`, `location`, `manager_id`, `contact_phone`, `status`) VALUES
(1, '物理实验室', '理科楼A301', 2, '0571-88888001', 1),
(2, '化学实验室', '理科楼B202', 2, '0571-88888002', 1),
(3, '计算机实验室', '工科楼C501', NULL, '0571-88888003', 1);

-- 初始设备分类
INSERT INTO `device_category` (`id`, `name`, `parent_id`, `sort_order`) VALUES
(1, '电子仪器', 0, 1),
(2, '光学仪器', 0, 2),
(3, '机械设备', 0, 3),
(4, '化学器材', 0, 4),
(5, '计算机设备', 0, 5),
(11, '示波器', 1, 1),
(12, '信号发生器', 1, 2),
(21, '显微镜', 2, 1),
(22, '光谱仪', 2, 2),
(51, '笔记本电脑', 5, 1),
(52, '台式工作站', 5, 2);

-- 初始设备
INSERT INTO `device_info` (`id`, `code`, `name`, `model`, `category_id`, `lab_id`, `total_quantity`, `available_quantity`, `unit`, `price`, `purchase_date`, `status`, `location_detail`, `description`, `version`) VALUES
(1, 'DEV-2024-0001', '数字示波器', 'Tektronix TBS1052B', 11, 1, 10, 10, '台', 8500.00, '2024-01-15', 0, 'A301-柜1', '50MHz双通道数字示波器', 0),
(2, 'DEV-2024-0002', '任意波形发生器', 'Keysight 33210A', 12, 1, 5, 5, '台', 12000.00, '2024-02-20', 0, 'A301-柜2', '10MHz任意波形发生器', 0),
(3, 'DEV-2024-0003', '光学显微镜', 'Olympus CX23', 21, 2, 8, 8, '台', 3500.00, '2024-03-10', 0, 'B202-柜1', '400倍生物显微镜', 0),
(4, 'DEV-2024-0004', 'UV-Vis分光光度计', 'Shimadzu UV-1800', 22, 2, 3, 3, '台', 45000.00, '2024-01-25', 0, 'B202-柜3', '紫外可见分光光度计', 0),
(5, 'DEV-2024-0005', '编程笔记本电脑', 'ThinkPad T14s', 51, 3, 30, 30, '台', 6500.00, '2024-06-01', 0, 'C501-机房', 'i7-1360P/16GB/512GB', 0),
(6, 'DEV-2024-0006', '高性能工作站', 'Dell Precision 3660', 52, 3, 5, 5, '台', 15000.00, '2024-05-15', 0, 'C501-机房2', 'i9-12900K/64GB/1TB+RTX3080', 0);

-- 初始数据字典
INSERT INTO `sys_dict` (`dict_type`, `dict_code`, `dict_label`) VALUES
('device_status', '0', '正常'),
('device_status', '1', '维修中'),
('device_status', '2', '已报废'),
('device_status', '3', '外借中'),
('borrow_status', '0', '待审批'),
('borrow_status', '1', '已批准'),
('borrow_status', '2', '已归还'),
('borrow_status', '3', '已逾期'),
('borrow_status', '4', '已驳回'),
('borrow_status', '5', '已取消'),
('role_type', 'ADMIN', '管理员'),
('role_type', 'TEACHER', '教师'),
('role_type', 'STUDENT', '学生'),
('maintenance_status', '0', '待处理'),
('maintenance_status', '1', '维修中'),
('maintenance_status', '2', '已修复'),
('maintenance_status', '3', '无法修复');
