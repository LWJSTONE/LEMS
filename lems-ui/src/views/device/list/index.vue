<template>
  <div class="device-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>设备台账管理</span>
          <el-button v-if="isAdmin" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 新增设备
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form :inline="true" class="search-form">
        <el-form-item label="设备名称">
          <el-input v-model="queryParams.name" placeholder="请输入" clearable @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="所属实验室">
          <el-select v-model="queryParams.labId" placeholder="全部" clearable>
            <el-option v-for="lab in labList" :key="lab.id" :label="lab.name" :value="lab.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="全部" clearable>
            <el-option label="正常" :value="0" />
            <el-option label="维修中" :value="1" />
            <el-option label="已报废" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon> 搜索</el-button>
          <el-button @click="resetQuery"><el-icon><Refresh /></el-icon> 重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table :data="tableData" border stripe style="width:100%">
        <el-table-column prop="code" label="设备编号" width="150" />
        <el-table-column prop="name" label="设备名称" min-width="160" />
        <el-table-column prop="model" label="规格型号" width="160" />
        <el-table-column prop="totalQuantity" label="总数量" width="80" align="center" />
        <el-table-column prop="availableQuantity" label="可借数量" width="90" align="center">
          <template #default="{ row }">
            <span :style="{ color: row.availableQuantity > 0 ? '#67C23A' : '#F56C6C', fontWeight: 600 }">
              {{ row.availableQuantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="60" align="center" />
        <el-table-column prop="price" label="单价(元)" width="100" align="right" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleDetail(row)">详情</el-button>
            <el-button v-if="isAdmin" size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="isAdmin" size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        style="margin-top:16px; text-align:right"
        v-model:current-page="queryParams.current"
        v-model:page-size="queryParams.size"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @current-change="loadData"
        @size-change="loadData"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑设备' : '新增设备'" width="650px" destroy-on-close>
      <el-form :model="form" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="设备编号" required>
              <el-input v-model="form.code" :disabled="isEdit" placeholder="唯一编号/资产号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备名称" required>
              <el-input v-model="form.name" placeholder="请输入设备名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="规格型号">
              <el-input v-model="form.model" placeholder="请输入型号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属实验室">
              <el-select v-model="form.labId" placeholder="请选择" clearable style="width:100%">
                <el-option v-for="lab in labList" :key="lab.id" :label="lab.name" :value="lab.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="总数量">
              <el-input-number v-model="form.totalQuantity" :min="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单位">
              <el-input v-model="form.unit" placeholder="台/套" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单价(元)">
              <el-input-number v-model="form.price" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="存放位置">
          <el-input v-model="form.locationDetail" placeholder="具体位置（柜号）" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getDevicePage, addDevice, updateDevice, deleteDevice } from '@/api/device'
import { getLabList } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const tableData = ref([])
const total = ref(0)
const labList = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)

const queryParams = reactive({ current: 1, size: 10, name: '', labId: null, status: null })
const form = reactive({
  id: null, code: '', name: '', model: '', categoryId: null, labId: null,
  totalQuantity: 1, unit: '台', price: 0, locationDetail: '', description: ''
})

const statusLabel = (s) => ['正常', '维修中', '已报废', '外借中'][s] || '未知'
const statusTagType = (s) => ['success', 'warning', 'danger', ''][s] || 'info'

const loadData = async () => {
  const res = await getDevicePage(queryParams)
  tableData.value = res.data.records
  total.value = res.data.total
}

const resetQuery = () => {
  queryParams.name = ''
  queryParams.labId = null
  queryParams.status = null
  queryParams.current = 1
  loadData()
}

const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, { id: null, code: '', name: '', model: '', categoryId: null, labId: null, totalQuantity: 1, unit: '台', price: 0, locationDetail: '', description: '' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!form.code || !form.name) {
    ElMessage.warning('请填写设备编号和名称')
    return
  }
  if (isEdit.value) {
    await updateDevice(form)
    ElMessage.success('修改成功')
  } else {
    await addDevice(form)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm(`确认删除设备"${row.name}"?`, '提示', { type: 'warning' })
  await deleteDevice(row.id)
  ElMessage.success('删除成功')
  loadData()
}

const handleDetail = (row) => {
  router.push(`/device/detail/${row.id}`)
}

onMounted(() => {
  loadData()
  getLabList().then(res => { labList.value = res.data || [] })
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.search-form { margin-bottom: 12px; }
</style>
