# LEMS 实验设备管理系统 - 答辩 PPT 大纲

## 幻灯片 1：封面

**标题**：基于 Spring Cloud 的实验设备管理系统（LEMS）
**副标题**：前后端分离微服务架构设计与实现
**答辩人**：XXX
**指导老师**：XXX 教授
**日期**：2025 年 X 月

---

## 幻灯片 2：目录

1. 项目背景与意义
2. 系统架构设计
3. 核心功能演示
4. 关键技术实现（⭐ 重点）
5. 系统测试与验证
6. 总结与展望

---

## 幻灯片 3：项目背景与意义

- **现状痛点**：
  - 高校实验室设备管理依赖纸质台账和 Excel，效率低下
  - 设备借用预约流程繁琐，需线下填写申请表多层审批
  - 库存状态无法实时更新，多人同时借用时缺乏并发控制
  - 设备维修报废缺乏完整记录，难以全生命周期追踪
- **项目目标**：构建一套功能完善、性能可靠、安全可控的设备全生命周期管理平台

---

## 幻灯片 4：技术选型

- **后端**：Spring Boot 2.7.18 + Spring Cloud 2021.0.8 + Spring Cloud Alibaba（Nacos 注册/配置中心）
- **持久层**：MyBatis-Plus 3.5.5 + MySQL 8.0
- **缓存/锁**：Redis（Token 黑名单 + 分布式锁）
- **认证**：Spring Security + JWT
- **前端**：Vue 3 + Element Plus + ECharts
- **部署**：Nginx 反向代理 + Windows 环境

---

## 幻灯片 5：系统架构总览

**（展示架构拓扑图）**

- 浏览器 → Nginx → API Gateway（:8080）
- Gateway 通过 Nacos 服务发现路由到 6 个微服务
  - Auth（:8081）| User（:8082）| Device（:8083）
  - Borrow（:8084）| Report（:8085）
- 基础设施：Nacos + MySQL + Redis
- **核心设计理念**：API 网关统一鉴权、微服务按业务领域拆分、Feign 声明式服务间调用

---

## 幻灯片 6：微服务职责划分

| 服务 | 职责 | 关键技术点 |
|------|------|-----------|
| Gateway | 路由、JWT 解析、跨域 | GlobalFilter、Redis 黑名单 |
| Auth | 登录注册、Token 签发/注销 | BCrypt 加密、JWT HS512 |
| User | 用户/实验室管理 | RBAC 角色控制 |
| Device | 设备台账/分类/维修 | ⭐ 乐观锁库存控制 |
| Borrow | 借用预约/审批/归还 | ⭐ 分布式锁 + 乐观锁并发控制 |
| Report | 统计报表、Echarts 数据 | 聚合 SQL、趋势分析 |

---

## 幻灯片 7：数据库设计

- **7 张核心表**：sys_user、lab_info、device_category、device_info、borrow_record、device_maintenance、sys_dict
- **设计亮点**：
  - 主键使用雪花算法（BIGINT），全局唯一且趋势递增
  - `device_info` 表的 `version` 字段用于乐观锁并发控制
  - `device_info` 表的 `available_quantity` 字段为库存扣减核心字段
  - `borrow_record` 表的 `idx_end_time` 索引为逾期扫描定时任务优化
  - 所有表支持逻辑删除（`deleted` 字段）和审计字段（`create_time`、`update_time`）

---

## 幻灯片 8：功能演示 - 设备管理

- **（截图展示）**
  - 设备分类树管理：多级树形结构，支持拖拽排序
  - 设备台账列表：分页查询、多条件筛选（名称/分类/实验室/状态）
  - 设备详情页：基本信息、库存状态、快捷操作（预约/报修）
  - 维修记录：报修提交、状态流转、设备自动变更状态

---

## 幻灯片 9：功能演示 - 借用预约

- **（截图展示）**
  - 设备预约页面：选择设备 → 填写信息 → 实时显示可用数量 → 提交申请
  - 我的借用记录：状态标签（待审批/已批准/已归还/已逾期/已驳回/已取消）
  - 借用审批页面：教师查看待审批列表 → 通过/驳回
  - 逾期高亮：已逾期记录以红色标签显示

---

## 幻灯片 10：功能演示 - 数据看板

- **（截图展示 Echarts 图表）**
  - 仪表盘统计卡片：设备总数、活跃借用、待审批、逾期数量
  - 设备使用率 Top10 柱状图
  - 月度借用趋势折线图+柱状图

---

## 幻灯片 11：⭐ 关键技术 - 库存并发控制方案（核心重点）

**这是答辩的核心讲解内容，需要详细讲解整个并发控制流程。**

### 问题定义

当 10 个学生同时借用仅剩 1 件的设备时，如何保证只有 1 人成功且库存不出现负数？

### 解决方案：Redis 分布式锁 + 数据库乐观锁（双重保障）

**第一层：Redis 分布式锁**（防止乐观锁重试风暴）
- 锁键：`lock:device:{deviceId}`
- 加锁：`SET lock:device:1 1 NX EX 30`（原子操作，30 秒超时防死锁）
- 获取锁失败的请求直接返回"操作过于频繁"，不进入数据库

**第二层：数据库乐观锁**（保证数据一致性）
- SQL 语句：
  ```sql
  UPDATE device_info
  SET available_quantity = available_quantity - 1,
      version = version + 1
  WHERE id = 1
    AND version = 5        -- 版本号校验
    AND available_quantity >= 1  -- 库存充足校验
  ```
- 影响行数 = 1 → 成功；影响行数 = 0 → 库存不足或被并发修改

---

## 幻灯片 12：⭐ 关键技术 - 借用流程中的库存操作

### 申请阶段（预占库存）
1. 获取 Redis 分布式锁
2. 查询设备 `available_quantity` 和 `version`
3. 校验库存充足
4. 执行乐观锁 SQL 扣减库存
5. 影响行数 = 0 → 抛出 BusinessException("库存不足或操作频繁")，事务回滚
6. 影响行数 = 1 → 创建借用记录（状态：待审批），释放锁

### 审批阶段（无需操作库存）
- 审批通过：库存已在申请时预占，直接更新状态
- 审批驳回：释放预占库存（乐观锁回加 `available_quantity + quantity`）

### 归还/取消阶段（回加库存）
- 归还确认 / 用户取消 / 审批驳回 → 乐观锁回加库存
- SQL：`UPDATE ... SET available_quantity = available_quantity + #{quantity}, version = version + 1 WHERE id = #{id} AND version = #{version}`

---

## 幻灯片 13：⭐ 关键技术 - 100 并发测试验证

**JMeter 测试配置**：
- 线程数：100（模拟 100 个用户同时借用）
- 设备可用库存：1 件
- 目标接口：`POST /api/v1/borrow/apply`

**测试结果**：

| 指标 | 结果 |
|------|------|
| 成功请求数 | 1 |
| 失败请求数 | 99 |
| 最终 available_quantity | 0（✅ 未出现负数） |
| 平均响应时间 | 45ms |
| 结论 | ✅ 库存并发安全 |

---

## 幻灯片 14：关键技术 - JWT 认证链路

- 用户登录 → Auth 服务签发 JWT Token（Payload: userId, username, role）
- 后续请求携带 Token → Nginx → Gateway
- Gateway 的 `JwtAuthGlobalFilter` 解析 Token：
  1. 检查 Redis 黑名单（登出的 Token）
  2. 校验 Token 过期时间
  3. 将 userId、role 注入 Header（`X-User-Id`、`X-User-Role`）传递给下游服务
- 下游服务直接从 Header 获取用户信息，无需解析 JWT
- 登出时 Token 加入 Redis 黑名单

---

## 幻灯片 15：关键技术 - 角色权限控制

- **三级权限控制**：
  1. **前端路由守卫**：`router.beforeEach` 根据 `meta.roles` 过滤菜单
  2. **前端 UI 控制**：`v-if="isAdmin"` 控制按钮显示
  3. **后端接口校验**：通过网关传递的 `X-User-Role` 判断权限
- **角色权限矩阵**：

| 功能 | ADMIN | TEACHER | STUDENT |
|------|-------|---------|---------|
| 设备管理（CRUD） | ✅ | ❌ | ❌ |
| 用户管理 | ✅ | ❌ | ❌ |
| 借用审批 | ✅ | ✅ | ❌ |
| 设备预约 | ✅ | ✅ | ✅ |
| 我的借用 | ✅ | ✅ | ✅ |
| 数据看板 | ✅ | ✅ | ✅ |

---

## 幻灯片 16：关键技术 - 逾期定时任务

- 使用 Spring `@Scheduled` 注解实现定时任务
- Cron 表达式：`0 0 * * * ?`（每小时整点执行）
- 扫描逻辑：`UPDATE borrow_record SET status = 3 WHERE status = 1 AND end_time < NOW()`
- 逾期记录在前端以红色 Tag 高亮显示
- 用户归还后状态变更为"已归还"

---

## 幻灯片 17：项目总结

### 已完成功能
- ✅ 6 个微服务独立部署（Gateway、Auth、User、Device、Borrow、Report）
- ✅ 完整的设备管理功能（分类树、台账 CRUD、维修记录）
- ✅ 借用预约全流程（申请→审批→借用→归还→逾期处理）
- ✅ 库存并发安全保障（Redis 分布式锁 + 乐观锁）
- ✅ JWT 认证 + RBAC 角色权限控制
- ✅ 数据可视化仪表盘（Echarts 图表）
- ✅ 前端 Vue 3 + Element Plus 响应式界面
- ✅ Windows 一键启动脚本 + Nginx 部署

### 项目亮点
- 🏆 并发安全：100 并发测试下库存数据零异常
- 🏆 架构规范：严格遵循前后端分离和 RESTful 设计
- 🏆 代码质量：全局异常处理、Feign 降级、统一响应格式

---

## 幻灯片 18：致谢

**感谢各位老师的指导和评审！**

- 项目源码：https://github.com/LWJSTONE/LEMS
- 技术栈：Spring Cloud + Vue 3 + MySQL + Redis
- 交付物：源码、需求文档、架构文档、数据库文档、接口文档、测试报告、部署手册

**Q & A**

---

## 答辩技巧提示

1. **重点讲解库存并发控制**（幻灯片 11-13），这是毕设的技术核心，评委最可能深入提问。
2. 准备好回答"为什么用分布式锁+乐观锁双重保障"：分布式锁减少数据库压力，乐观锁保证数据最终一致性。
3. 熟悉每个微服务的职责和端口，能快速画出架构图。
4. 了解 MyBatis-Plus 乐观锁的实现原理（`@Version` 注解）。
5. 能解释为什么审批通过时不需要再操作库存（申请阶段已预占）。
