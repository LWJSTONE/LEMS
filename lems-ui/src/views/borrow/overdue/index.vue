<template>
  <div class="borrow-overdue">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>逾期未还管理</span>
          <el-tag type="danger" effect="dark" v-if="total > 0">
            共 {{ total }} 条逾期记录
          </el-tag>
        </div>
      </template>

      <el-table :data="tableData" border stripe v-loading="loading" style="width:100%">
        <el-table-column prop="id" label="记录ID" width="100" />
        <el-table-column prop="deviceName" label="设备名称" min-width="140" />
        <el-table-column prop="deviceCode" label="设备编号" width="140" />
        <el-table-column prop="userName" label="借用人" width="100" />
        <el-table-column prop="borrowQuantity" label="借用人数量" width="100" align="center" />
        <el-table-column prop="endTime" label="应还日期" width="170" />
        <el-table-column prop="purpose" label="用途说明" min-width="120" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag type="danger" size="small">逾期</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top:16px; text-align:right"
        v-model:current-page="queryParams.current" v-model:page-size="queryParams.size"
        :total="total" :page-sizes="[10, 20, 50]" layout="total, sizes, prev, pager, next"
        @current-change="loadData" @size-change="handleSizeChange" />

      <el-empty v-if="!loading && tableData.length === 0" description="暂无逾期记录" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getOverdueList } from '@/api/borrow'
import { ElMessage } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const queryParams = reactive({ current: 1, size: 10 })

const loadData = async () => {
  loading.value = true
  try {
    const res = await getOverdueList(queryParams)
    tableData.value = res.data?.records || []
    total.value = res.data?.total || 0
  } catch (e) {
    console.error('加载逾期列表失败:', e)
    ElMessage.error('加载逾期列表失败')
  } finally {
    loading.value = false
  }
}

const handleSizeChange = () => {
  queryParams.current = 1
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
