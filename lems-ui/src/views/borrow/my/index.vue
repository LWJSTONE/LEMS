<template>
  <div class="my-borrow">
    <el-card shadow="hover">
      <template #header><span>我的借用记录</span></template>

      <el-form :inline="true">
        <el-form-item label="状态">
          <el-select v-model="statusFilter" placeholder="全部" clearable @change="loadData">
            <el-option label="待审批" :value="0" />
            <el-option label="已批准" :value="1" />
            <el-option label="已归还" :value="2" />
            <el-option label="已逾期" :value="3" />
            <el-option label="已驳回" :value="4" />
            <el-option label="已取消" :value="5" />
          </el-select>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="申请单号" width="160" />
        <el-table-column prop="deviceName" label="设备名称" min-width="140" show-overflow-tooltip />
        <el-table-column prop="borrowQuantity" label="数量" width="70" align="center" />
        <el-table-column prop="startTime" label="借用时间" width="170" />
        <el-table-column prop="endTime" label="应还时间" width="170" />
        <el-table-column prop="actualReturnTime" label="实际归还" width="170" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" effect="dark">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === 0" size="small" type="danger" @click="handleCancel(row)">取消</el-button>
            <el-button v-if="row.status === 1 || row.status === 3" size="small" type="success" @click="handleReturn(row)">归还</el-button>
            <span v-if="row.rejectReason" class="reject-reason">驳回: {{ row.rejectReason }}</span>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:16px; text-align:right"
        v-model:current-page="queryParams.current" v-model:page-size="queryParams.size"
        :total="total" :page-sizes="[10, 20, 50]" layout="total, sizes, prev, pager, next"
        @current-change="loadData" @size-change="handleSizeChange" />
    </el-card>

    <!-- 归还对话框 -->
    <el-dialog v-model="returnDialogVisible" title="归还确认" width="450px">
      <p>确认归还此设备?</p>
      <el-form label-width="80px">
        <el-form-item label="归还备注">
          <el-input v-model="returnRemark" type="textarea" :rows="3" placeholder="如有损坏请说明" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReturn">确认归还</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getMyBorrowList, cancelBorrow, returnDevice } from '@/api/borrow'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const statusFilter = ref(null)
const queryParams = reactive({ current: 1, size: 10 })
const returnDialogVisible = ref(false)
const returnRemark = ref('')
const returnId = ref(null)

const statusLabel = (s) => ['待审批','已批准','已归还','已逾期','已驳回','已取消'][s] || '未知'
const statusTagType = (s) => ['warning','success','info','danger','',''][s] || 'info'

const loadData = async () => {
  loading.value = true
  try {
    const res = await getMyBorrowList({ ...queryParams, status: statusFilter.value })
    tableData.value = res.data?.records || []
    total.value = res.data?.total || 0
  } catch (e) {
    console.error('加载借用记录失败', e)
    ElMessage.error('加载借用记录失败')
  } finally {
    loading.value = false
  }
}

const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm('确认取消此申请?', '提示', { type: 'warning' })
    await cancelBorrow(row.id)
    ElMessage.success('已取消')
    loadData()
  } catch (e) {
    if (e !== 'cancel') console.error('取消失败', e)
  }
}

const handleReturn = (row) => {
  returnId.value = row.id
  returnRemark.value = ''
  returnDialogVisible.value = true
}

const confirmReturn = async () => {
  try {
    await returnDevice(returnId.value, returnRemark.value)
    ElMessage.success('归还成功')
    returnDialogVisible.value = false
    loadData()
  } catch (e) {
    console.error('归还失败', e)
    ElMessage.error('归还失败')
  }
}

onMounted(loadData)

const handleSizeChange = () => {
  queryParams.current = 1
  loadData()
}
</script>

<style scoped>
.reject-reason { color: #F56C6C; font-size: 12px; margin-left: 8px; }
</style>
