# LEMS - 实验设备管理系统

## 项目简介

基于 Spring Cloud 微服务架构的高校实验室仪器设备全生命周期管理平台，涵盖设备入库、借用预约、归还验收、维修报废、库存盘点与使用统计。

## 技术栈

### 后端
- JDK 1.8 + Spring Boot 2.7.18 + Spring Cloud 2021.0.8
- Spring Cloud Alibaba 2021.0.5.0 (Nacos 注册/配置中心)
- MyBatis-Plus 3.5.5 + MySQL 8.0
- Spring Security + JWT 认证
- Redis 分布式锁 + Token黑名单

### 前端
- Vue 3.3.13 + Vite 4.5.3
- Element Plus 2.7.6 + Pinia 2.1.7
- ECharts 5.5.0 数据可视化
- Axios 1.6.7

## 微服务模块

| 模块 | 端口 | 职责 |
|------|------|------|
| lab-gateway | 8080 | API网关、JWT鉴权、路由分发 |
| lab-auth | 8081 | 登录注册、JWT签发/注销 |
| lab-user | 8082 | 用户管理、实验室管理 |
| lab-device | 8083 | 设备台账、分类、库存(乐观锁) |
| lab-borrow | 8084 | 预约借用、审批、归还(并发控制) |
| lab-report | 8085 | 统计报表、数据看板 |

## 数据库

- 数据库名: `lab_device_mgt`
- 字符集: `utf8mb4`
- 初始化脚本: `sql/init.sql` (含7张表 + 初始数据)

## 快速开始

### 环境要求
- JDK 1.8, Maven 3.8+, MySQL 8.0, Redis, Node.js 18

### 1. 初始化数据库
```sql
mysql -u root -p < sql/init.sql
```

### 2. 启动中间件
- Nacos: `bin/startup.cmd` (Windows)
- Redis: `redis-server`

### 3. 编译后端
```bash
mvn clean package -DskipTests
```

### 4. 启动后端服务
```bash
# 按顺序启动
java -jar lab-gateway/target/lab-gateway-1.0.0.jar
java -jar lab-auth/target/lab-auth-1.0.0.jar
java -jar lab-user/target/lab-user-1.0.0.jar
java -jar lab-device/target/lab-device-1.0.0.jar
java -jar lab-borrow/target/lab-borrow-1.0.0.jar
java -jar lab-report/target/lab-report-1.0.0.jar
```

或使用一键启动脚本: `start-lab.bat` (Windows)

### 5. 启动前端
```bash
cd lems-ui
npm install
npm run dev
```

### 6. 访问
- 前端: http://localhost:3000
- 网关: http://localhost:8080
- Nacos: http://localhost:8848/nacos

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 教师 | teacher01 | admin123 |
| 学生 | student01 | admin123 |

## 核心特性

### 库存并发控制（乐观锁 + Redis分布式锁）
- 申请阶段: Redis分布式锁避免乐观锁重试风暴
- 库存扣减: `UPDATE ... WHERE version = ? AND available_quantity >= ?`
- 归还/取消/驳回: 乐观锁回加库存
- 若影响行数为0 → 抛出 BusinessException("库存不足或操作频繁")

### 设备借用状态流转
待审批(0) → 已批准(1) → 已归还(2)
待审批(0) → 已驳回(4) / 已取消(5)
已批准(1) → 已逾期(3) → 已归还(2) [定时任务扫描]
