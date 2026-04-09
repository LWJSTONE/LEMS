<template>
  <div class="system-user">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
        </div>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="queryParams.keyword" placeholder="用户名/姓名" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="queryParams.roleType" placeholder="全部" clearable>
            <el-option label="管理员" value="ADMIN" />
            <el-option label="教师" value="TEACHER" />
            <el-option label="学生" value="STUDENT" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon> 搜索</el-button>
          <el-button @click="resetQuery"><el-icon><Refresh /></el-icon> 重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="realName" label="姓名" width="100" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="email" label="邮箱" width="170" />
        <el-table-column prop="roleType" label="角色" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.roleType === 'ADMIN' ? 'danger' : row.roleType === 'TEACHER' ? 'warning' : 'info'">
              {{ roleLabel(row.roleType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-switch :model-value="row.status === 1" @change="toggleStatus(row)" />
          </template>
        </el-table-column>
        <el-table-column prop="labName" label="所属实验室" min-width="120">
          <template #default="{ row }">
            {{ row.labName || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="170" />
      </el-table>

      <el-pagination style="margin-top:16px; text-align:right"
        v-model:current-page="queryParams.current" v-model:page-size="queryParams.size"
        :total="total" layout="total, sizes, prev, pager, next"
        @current-change="loadData" @size-change="handleSizeChange" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getUserPage, updateUserStatus } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const queryParams = reactive({ current: 1, size: 10, keyword: '', roleType: null })

const roleLabel = (r) => ({ ADMIN: '管理员', TEACHER: '教师', STUDENT: '学生' }[r] || r)

const loadData = async () => {
  loading.value = true
  try {
    const res = await getUserPage(queryParams)
    tableData.value = res.data?.records || []
    total.value = res.data?.total || 0
  } catch (e) {
    console.error('加载用户列表失败', e)
  } finally {
    loading.value = false
  }
}

const handleSizeChange = () => {
  queryParams.current = 1
  loadData()
}

const resetQuery = () => {
  queryParams.keyword = ''
  queryParams.roleType = null
  queryParams.current = 1
  loadData()
}

const toggleStatus = async (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  const action = newStatus === 1 ? '启用' : '禁用'
  try {
    await ElMessageBox.confirm(`确认${action}用户"${row.realName}"?`, '提示', { type: 'warning' })
    await updateUserStatus(row.id, newStatus)
    ElMessage.success(`${action}成功`)
    loadData()
  } catch (e) {
    if (e !== 'cancel') console.error('切换用户状态失败', e)
  }
}

onMounted(loadData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.search-form { margin-bottom: 12px; }
</style>
