<template>
  <div class="borrow-approval">
    <el-card shadow="hover">
      <template #header><span>借用审批</span></template>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="申请单号" width="160" />
        <el-table-column prop="deviceId" label="设备ID" width="100" />
        <el-table-column prop="borrowQuantity" label="数量" width="70" align="center" />
        <el-table-column prop="startTime" label="借用时间" width="170" />
        <el-table-column prop="endTime" label="应还时间" width="170" />
        <el-table-column prop="purpose" label="用途" min-width="160" show-overflow-tooltip />
        <el-table-column prop="createTime" label="申请时间" width="170" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="success" @click="handleApprove(row)">通过</el-button>
            <el-button size="small" type="danger" @click="handleReject(row)">驳回</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:16px; text-align:right"
        v-model:current-page="queryParams.current" v-model:page-size="queryParams.size"
        :total="total" layout="total, prev, pager, next"
        @current-change="loadData" />
    </el-card>

    <el-dialog v-model="rejectDialogVisible" title="驳回原因" width="450px">
      <el-input v-model="rejectReason" type="textarea" :rows="4" placeholder="请输入驳回理由" />
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReject">确认驳回</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getPendingList, approveBorrow, rejectBorrow } from '@/api/borrow'
import { ElMessage } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const queryParams = reactive({ current: 1, size: 10 })
const rejectDialogVisible = ref(false)
const rejectReason = ref('')
const rejectId = ref(null)

const loadData = () => {
  getPendingList(queryParams).then(res => {
    tableData.value = res.data?.records || []
    total.value = res.data?.total || 0
  })
}

const handleApprove = async (row) => {
  await approveBorrow(row.id)
  ElMessage.success('审批通过')
  loadData()
}

const handleReject = (row) => {
  rejectId.value = row.id
  rejectReason.value = ''
  rejectDialogVisible.value = true
}

const confirmReject = async () => {
  if (!rejectReason.value) { ElMessage.warning('请填写驳回理由'); return }
  await rejectBorrow(rejectId.value, rejectReason.value)
  ElMessage.success('已驳回')
  rejectDialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>
