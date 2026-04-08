# LEMS 实验设备管理系统 - API 接口文档

| 项目信息 | 内容 |
|---------|------|
| 基础路径 | http://localhost:8080/api/v1 |
| 认证方式 | Bearer Token（JWT） |
| 内容类型 | application/json |
| 文档版本 | V1.0 |

---

## 1. 统一响应格式

所有接口返回统一的 JSON 响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1712000000000
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码：200=成功，400=参数错误，401=未认证，403=无权限，500=服务器错误 |
| message | string | 提示信息 |
| data | object/array/null | 响应数据 |
| timestamp | long | 响应时间戳（毫秒） |

**分页响应格式**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "records": [],
    "total": 100,
    "size": 10,
    "current": 1
  },
  "timestamp": 1712000000000
}
```

---

## 2. 认证模块 `/auth`

### 2.1 用户登录

- **URL**: `POST /api/v1/auth/login`
- **无需认证**: 是

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名（学号/工号） |
| password | string | 是 | 密码 |

**请求示例**：
```json
{ "username": "admin", "password": "admin123" }
```

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "Bearer eyJhbGciOiJIUzUxMiJ9...",
    "userId": 1,
    "username": "admin",
    "realName": "系统管理员",
    "roleType": "ADMIN",
    "labId": null
  }
}
```

### 2.2 用户注册

- **URL**: `POST /api/v1/auth/register`
- **无需认证**: 是

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |
| realName | string | 是 | 真实姓名 |
| phone | string | 否 | 手机号 |
| email | string | 否 | 邮箱 |
| roleType | string | 否 | STUDENT / TEACHER，默认 STUDENT |
| labId | long | 否 | 所属实验室 ID |

### 2.3 用户登出

- **URL**: `POST /api/v1/auth/logout`
- **需要认证**: 是

**请求头**：`Authorization: Bearer {token}`

---

## 3. 用户模块 `/user`

### 3.1 获取个人信息

- **URL**: `GET /api/v1/user/profile`
- **需要认证**: 是
- **网关传递**: X-User-Id

**响应示例**：
```json
{
  "code": 200,
  "data": {
    "id": 1, "username": "admin", "realName": "系统管理员",
    "phone": "13800000001", "email": "admin@lab.edu.cn",
    "roleType": "ADMIN", "labId": null, "labName": null,
    "status": 1, "createTime": "2024-01-01 00:00:00"
  }
}
```

### 3.2 修改个人信息

- **URL**: `PUT /api/v1/user/profile`
- **需要认证**: 是

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| realName | string | 否 | 真实姓名 |
| phone | string | 否 | 手机号 |
| email | string | 否 | 邮箱 |

### 3.3 用户列表分页查询

- **URL**: `GET /api/v1/user/page`
- **需要认证**: 是
- **权限**: ADMIN

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| current | int | 否 | 当前页码，默认 1 |
| size | int | 否 | 每页大小，默认 10 |
| keyword | string | 否 | 搜索关键词（用户名/姓名） |
| roleType | string | 否 | 角色筛选：ADMIN / TEACHER / STUDENT |

### 3.4 更新用户状态

- **URL**: `PUT /api/v1/user/{id}/status`
- **需要认证**: 是
- **权限**: ADMIN

**查询参数**：`status`（0=禁用，1=启用）

### 3.5 获取实验室列表

- **URL**: `GET /api/v1/user/lab/list`
- **需要认证**: 是

### 3.6 获取实验室成员列表

- **URL**: `GET /api/v1/user/lab/members`
- **需要认证**: 是

**查询参数**：`labId`（实验室 ID），`current`，`size`

### 3.7 新增实验室

- **URL**: `POST /api/v1/user/lab`
- **需要认证**: 是
- **权限**: ADMIN

### 3.8 修改实验室

- **URL**: `PUT /api/v1/user/lab`
- **需要认证**: 是
- **权限**: ADMIN

---

## 4. 设备管理模块 `/device`

### 4.1 获取分类树

- **URL**: `GET /api/v1/device/categories/tree`
- **需要认证**: 是

**响应示例**：
```json
{
  "code": 200,
  "data": [
    {
      "id": 1, "name": "电子仪器", "parentId": 0, "sortOrder": 1,
      "children": [
        { "id": 11, "name": "示波器", "parentId": 1, "sortOrder": 1, "children": [] },
        { "id": 12, "name": "信号发生器", "parentId": 1, "sortOrder": 2, "children": [] }
      ]
    }
  ]
}
```

### 4.2 新增分类

- **URL**: `POST /api/v1/device/categories`
- **需要认证**: 是
- **权限**: ADMIN

### 4.3 修改分类

- **URL**: `PUT /api/v1/device/categories`
- **需要认证**: 是
- **权限**: ADMIN

### 4.4 删除分类

- **URL**: `DELETE /api/v1/device/categories/{id}`
- **需要认证**: 是
- **权限**: ADMIN

### 4.5 设备列表分页查询

- **URL**: `GET /api/v1/device/info/page`
- **需要认证**: 是

**查询参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| current | int | 否 | 当前页码，默认 1 |
| size | int | 否 | 每页大小，默认 10 |
| name | string | 否 | 设备名称模糊搜索 |
| categoryId | long | 否 | 分类 ID 筛选 |
| labId | long | 否 | 实验室 ID 筛选 |
| status | int | 否 | 状态筛选：0=正常，1=维修，2=报废 |

### 4.6 获取设备详情

- **URL**: `GET /api/v1/device/info/{id}`
- **需要认证**: 是

**响应示例**：
```json
{
  "code": 200,
  "data": {
    "id": 1, "code": "DEV-2024-0001", "name": "数字示波器",
    "model": "Tektronix TBS1052B", "categoryId": 11, "labId": 1,
    "totalQuantity": 10, "availableQuantity": 8, "unit": "台",
    "price": 8500.00, "purchaseDate": "2024-01-15",
    "status": 0, "locationDetail": "A301-柜1", "description": "50MHz双通道",
    "version": 5
  }
}
```

### 4.7 新增设备

- **URL**: `POST /api/v1/device/info`
- **需要认证**: 是
- **权限**: ADMIN

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 设备编号（唯一） |
| name | string | 是 | 设备名称 |
| model | string | 否 | 规格型号 |
| categoryId | long | 否 | 分类 ID |
| labId | long | 否 | 实验室 ID |
| totalQuantity | int | 否 | 总数量，默认 1 |
| unit | string | 否 | 单位，默认"台" |
| price | decimal | 否 | 单价 |
| purchaseDate | date | 否 | 购置日期 (yyyy-MM-dd) |
| locationDetail | string | 否 | 存放位置 |
| description | string | 否 | 备注 |

### 4.8 修改设备

- **URL**: `PUT /api/v1/device/info`
- **需要认证**: 是
- **权限**: ADMIN

### 4.9 删除设备

- **URL**: `DELETE /api/v1/device/info/{id}`
- **需要认证**: 是
- **权限**: ADMIN（逻辑删除）

### 4.10 更新设备状态

- **URL**: `PUT /api/v1/device/info/{id}/status`
- **需要认证**: 是
- **权限**: ADMIN

**查询参数**：`status`（0=正常，1=维修，2=报废）

### 4.11 新增维修记录

- **URL**: `POST /api/v1/device/maintenance`
- **需要认证**: 是

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| deviceId | long | 是 | 设备 ID |
| faultDesc | string | 是 | 故障描述 |

### 4.12 维修记录分页查询

- **URL**: `GET /api/v1/device/maintenance/page`
- **需要认证**: 是

**查询参数**：`deviceId`, `status`, `current`, `size`

### 4.13 更新维修状态

- **URL**: `PUT /api/v1/device/maintenance/{id}/status`
- **需要认证**: 是

**查询参数**：`status`（0=待处理，1=维修中，2=已修复，3=无法修复）

---

## 5. 借用预约模块 `/borrow`

### 5.1 提交借用申请 ⭐

- **URL**: `POST /api/v1/borrow/apply`
- **需要认证**: 是
- **网关传递**: X-User-Id
- **并发控制**: Redis 分布式锁 + 数据库乐观锁

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| deviceId | long | 是 | 借用设备 ID |
| borrowQuantity | int | 是 | 借用数量 |
| startTime | string | 是 | 借用开始时间 (yyyy-MM-ddTHH:mm:ss) |
| endTime | string | 是 | 预计归还时间 (yyyy-MM-ddTHH:mm:ss) |
| purpose | string | 否 | 用途说明 |

**响应**：
- 成功：`{ "code": 200, "message": "success" }`
- 库存不足：`{ "code": 500, "message": "库存不足，当前可用数量为 X" }`
- 操作频繁：`{ "code": 500, "message": "操作过于频繁，请稍后重试" }`

**并发控制说明**：此接口使用 Redis 分布式锁（`lock:device:{deviceId}`，30 秒超时）+ 数据库乐观锁双重保障。多个用户同时借用同一设备时，只有第一个获取锁且乐观锁版本匹配的请求会成功。

### 5.2 我的借用记录

- **URL**: `GET /api/v1/borrow/my/list`
- **需要认证**: 是

**查询参数**：`current`, `size`, `status`（可选状态筛选）

### 5.3 待审批列表

- **URL**: `GET /api/v1/borrow/pending/list`
- **需要认证**: 是
- **权限**: ADMIN / TEACHER

### 5.4 审批通过

- **URL**: `PUT /api/v1/borrow/approve/{id}`
- **需要认证**: 是
- **权限**: ADMIN / TEACHER

**说明**：审批通过后库存无需再次操作（申请时已预占）。

### 5.5 驳回申请

- **URL**: `PUT /api/v1/borrow/reject/{id}`
- **需要认证**: 是
- **权限**: ADMIN / TEACHER

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reason | string | 是 | 驳回理由 |

**说明**：驳回后系统自动释放预占库存。

### 5.6 取消申请

- **URL**: `PUT /api/v1/borrow/cancel/{id}`
- **需要认证**: 是

**说明**：仅待审批状态可取消，取消后释放预占库存。

### 5.7 归还确认

- **URL**: `PUT /api/v1/borrow/return/{id}`
- **需要认证**: 是

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| remark | string | 否 | 归还备注（损坏说明） |

**说明**：归还后系统自动回加设备可用库存。

### 5.8 逾期未归还列表

- **URL**: `GET /api/v1/borrow/overdue/list`
- **需要认证**: 是
- **权限**: ADMIN / TEACHER

---

## 6. 统计报表模块 `/report`

### 6.1 首页仪表盘统计

- **URL**: `GET /api/v1/report/dashboard`
- **需要认证**: 是

**响应示例**：
```json
{
  "code": 200,
  "data": {
    "totalDevices": 61,
    "activeBorrows": 5,
    "pendingApprovals": 3,
    "overdueCount": 1,
    "totalUsers": 3
  }
}
```

### 6.2 设备使用率 Top10

- **URL**: `GET /api/v1/report/device/usage/top`
- **需要认证**: 是
- **用途**: Echarts 柱状图数据

**响应示例**：
```json
{
  "code": 200,
  "data": [
    { "name": "编程笔记本电脑", "code": "DEV-2024-0005", "totalQuantity": 30, "borrowCount": 45, "totalBorrowQuantity": 120, "usageRate": 400.00 },
    { "name": "数字示波器", "code": "DEV-2024-0001", "totalQuantity": 10, "borrowCount": 25, "totalBorrowQuantity": 38, "usageRate": 380.00 }
  ]
}
```

### 6.3 月度借用趋势

- **URL**: `GET /api/v1/report/borrow/trend`
- **需要认证**: 是
- **用途**: Echarts 折线图+柱状图数据

**响应示例**：
```json
{
  "code": 200,
  "data": [
    { "month": "2024-01", "borrowCount": 15, "totalQuantity": 28 },
    { "month": "2024-02", "borrowCount": 22, "totalQuantity": 35 },
    { "month": "2024-03", "borrowCount": 30, "totalQuantity": 48 }
  ]
}
```

---

## 7. 状态码说明

| 状态码 | 含义 | 触发场景 |
|--------|------|---------|
| 200 | 成功 | 请求处理成功 |
| 400 | 参数错误 | 必填参数缺失、格式不正确 |
| 401 | 未认证 | Token 缺失、Token 过期、Token 在黑名单中 |
| 403 | 无权限 | 角色权限不足（如学生访问管理接口） |
| 500 | 业务异常 | 库存不足、操作频繁、设备不存在等 |
