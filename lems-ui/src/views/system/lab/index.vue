<template>
  <div class="system-lab">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>实验室管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 新增实验室
          </el-button>
        </div>
      </template>

      <el-table :data="labList" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="实验室名称" min-width="150" />
        <el-table-column prop="location" label="位置" min-width="180" />
        <el-table-column prop="managerName" label="负责人" width="100">
          <template #default="{ row }">
            {{ row.managerName || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="contactPhone" label="联系电话" width="130" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '开放' : '关闭' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleMembers(row)">成员</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑实验室' : '新增实验室'" width="500px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="实验室名称" required>
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="位置">
          <el-input v-model="form.location" placeholder="请输入具体位置" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="form.contactPhone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0"
            active-text="开放" inactive-text="关闭" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 实验室成员对话框 -->
    <el-dialog v-model="membersDialogVisible" title="实验室成员" width="600px">
      <el-table :data="memberList" border stripe v-loading="membersLoading" max-height="400">
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="realName" label="姓名" width="120" />
        <el-table-column prop="roleType" label="角色" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.roleType === 'ADMIN' ? 'danger' : row.roleType === 'TEACHER' ? 'warning' : ''" size="small">
              {{ { ADMIN: '管理员', TEACHER: '教师', STUDENT: '学生' }[row.roleType] || row.roleType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="createTime" label="加入时间" min-width="160" />
      </el-table>
      <el-empty v-if="!membersLoading && memberList.length === 0" description="暂无成员" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getLabList, addLab, updateLab, getLabMembers } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const labList = ref([])
const dialogVisible = ref(false)
const loading = ref(false)
const form = reactive({ id: null, name: '', location: '', contactPhone: '', status: 1 })

// 成员管理
const membersDialogVisible = ref(false)
const membersLoading = ref(false)
const memberList = ref([])
const currentLabId = ref(null)

const loadData = async () => {
  loading.value = true
  try {
    const res = await getLabList()
    labList.value = res.data || []
  } catch (e) {
    console.error('加载实验室列表失败', e)
    ElMessage.error('加载实验室列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  Object.assign(form, { id: null, name: '', location: '', contactPhone: '', status: 1 })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, { id: row.id, name: row.name, location: row.location, contactPhone: row.contactPhone, status: row.status })
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确认删除实验室"${row.name}"?`, '提示', { type: 'warning' })
  } catch (e) { return }
  // 目前后端无删除实验室API，暂时提示
  ElMessage.warning('实验室删除功能暂未开放，如需删除请联系系统管理员')
}

const handleMembers = async (row) => {
  currentLabId.value = row.id
  membersDialogVisible.value = true
  membersLoading.value = true
  try {
    const res = await getLabMembers({ labId: row.id, current: 1, size: 100 })
    memberList.value = res.data?.records || []
  } catch (e) {
    console.error('加载实验室成员失败:', e)
    ElMessage.error('加载实验室成员失败')
  } finally {
    membersLoading.value = false
  }
}

const submitForm = async () => {
  if (!form.name) { ElMessage.warning('请填写实验室名称'); return }
  try {
    if (form.id) {
      await updateLab(form)
      ElMessage.success('修改成功')
    } else {
      await addLab(form)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) {
    console.error('提交实验室失败', e)
  }
}

onMounted(loadData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
