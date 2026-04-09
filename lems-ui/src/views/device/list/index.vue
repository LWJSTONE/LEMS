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
        <el-form-item label="设备分类">
          <el-select v-model="queryParams.categoryId" placeholder="全部" clearable style="width:160px">
            <el-option v-for="cat in flatCategories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属实验室">
          <el-select v-model="queryParams.labId" placeholder="全部" clearable style="width:160px">
            <el-option v-for="lab in labList" :key="lab.id" :label="lab.name" :value="lab.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="全部" clearable style="width:120px">
            <el-option label="正常" :value="0" />
            <el-option label="维修中" :value="1" />
            <el-option label="已报废" :value="2" />
            <el-option label="外借中" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon> 搜索</el-button>
          <el-button @click="resetQuery"><el-icon><Refresh /></el-icon> 重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table :data="tableData" border stripe v-loading="loading" style="width:100%">
        <el-table-column prop="code" label="设备编号" width="150" />
        <el-table-column prop="name" label="设备名称" min-width="160" />
        <el-table-column prop="categoryName" label="设备分类" width="120">
          <template #default="{ row }">{{ row.categoryName || '-' }}</template>
        </el-table-column>
        <el-table-column prop="model" label="规格型号" width="140" />
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
        @size-change="handleSizeChange"
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
            <el-form-item label="设备分类">
              <el-select v-model="form.categoryId" placeholder="请选择分类" clearable style="width:100%">
                <el-option v-for="cat in flatCategories" :key="cat.id" :label="cat.name" :value="cat.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="所属实验室">
              <el-select v-model="form.labId" placeholder="请选择" clearable style="width:100%">
                <el-option v-for="lab in labList" :key="lab.id" :label="lab.name" :value="lab.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="购置日期">
              <el-date-picker v-model="form.purchaseDate" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width:100%" />
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
import { getDevicePage, addDevice, updateDevice, deleteDevice, getCategoryTree } from '@/api/device'
import { getLabList } from '@/api/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const labList = ref([])
const categoryTree = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)

const queryParams = reactive({ current: 1, size: 10, name: '', labId: null, categoryId: null, status: null })
const form = reactive({
  id: null, code: '', name: '', model: '', categoryId: null, labId: null,
  totalQuantity: 1, unit: '台', price: 0, purchaseDate: '', locationDetail: '', description: '', version: null
})

// 将树形分类扁平化用于下拉选择
const flatCategories = computed(() => {
  const result = []
  const walk = (nodes) => {
    if (!nodes) return
    nodes.forEach(node => {
      result.push({ id: node.id, name: node.name })
      if (node.children && node.children.length) walk(node.children)
    })
  }
  walk(categoryTree.value)
  return result
})

const statusLabel = (s) => ['正常', '维修中', '已报废', '外借中'][s] || '未知'
const statusTagType = (s) => ['success', 'warning', 'danger', ''][s] || 'info'

const loadData = async () => {
  loading.value = true
  try {
    const res = await getDevicePage(queryParams)
    tableData.value = res.data.records
    total.value = res.data.total
  } catch (e) {
    console.error('加载设备列表失败:', e)
  } finally {
    loading.value = false
  }
}

const handleSizeChange = () => {
  queryParams.current = 1
  loadData()
}

const resetQuery = () => {
  queryParams.name = ''
  queryParams.labId = null
  queryParams.categoryId = null
  queryParams.status = null
  queryParams.current = 1
  loadData()
}

const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, { id: null, code: '', name: '', model: '', categoryId: null, labId: null, totalQuantity: 1, unit: '台', price: 0, purchaseDate: '', locationDetail: '', description: '', version: null })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  // 只复制需要编辑的字段，避免携带无关字段
  Object.assign(form, {
    id: row.id, code: row.code, name: row.name, model: row.model,
    categoryId: row.categoryId, labId: row.labId, totalQuantity: row.totalQuantity,
    unit: row.unit, price: row.price, purchaseDate: row.purchaseDate || '',
    locationDetail: row.locationDetail, description: row.description, version: row.version
  })
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!form.code || !form.name) {
    ElMessage.warning('请填写设备编号和名称')
    return
  }
  try {
    if (isEdit.value) {
      await updateDevice(form)
      ElMessage.success('修改成功')
    } else {
      await addDevice(form)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) {
    console.error('提交设备失败:', e)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确认删除设备"${row.name}"?`, '提示', { type: 'warning' })
  } catch (e) { return }
  try {
    await deleteDevice(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    console.error('删除设备失败:', e)
  }
}

const handleDetail = (row) => {
  router.push(`/device/detail/${row.id}`)
}

const loadCategories = async () => {
  try {
    const res = await getCategoryTree()
    categoryTree.value = res.data || []
  } catch (e) {
    console.error('加载分类失败:', e)
  }
}

onMounted(() => {
  loadData()
  loadCategories()
  getLabList().then(res => { labList.value = res.data || [] }).catch(e => { console.error('加载实验室列表失败:', e) })
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.search-form { margin-bottom: 12px; }
</style>
