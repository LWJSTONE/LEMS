<template>
  <div class="device-detail">
    <el-page-header @back="$router.back()" content="设备详情" style="margin-bottom:20px" />

    <el-row :gutter="20">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header><span>基本信息</span></template>
          <el-descriptions :column="2" border v-loading="loading">
            <el-descriptions-item label="设备编号">{{ device.code }}</el-descriptions-item>
            <el-descriptions-item label="设备名称">{{ device.name }}</el-descriptions-item>
            <el-descriptions-item label="规格型号">{{ device.model }}</el-descriptions-item>
            <el-descriptions-item label="所属实验室">{{ device.labName || '-' }}</el-descriptions-item>
            <el-descriptions-item label="总数量">{{ device.totalQuantity }} {{ device.unit }}</el-descriptions-item>
            <el-descriptions-item label="可用数量">
              <span :style="{ color: device.availableQuantity > 0 ? '#67C23A' : '#F56C6C', fontWeight: 700, fontSize: '18px' }">
                {{ device.availableQuantity }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="单价">¥{{ device.price }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="statusTagType(device.status)">{{ statusLabel(device.status) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="购置日期">{{ device.purchaseDate }}</el-descriptions-item>
            <el-descriptions-item label="存放位置">{{ device.locationDetail || '-' }}</el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ device.description || '-' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header><span>快捷操作</span></template>
          <div style="display:flex; flex-direction:column; gap:12px">
            <el-button type="primary" size="large" :disabled="device.availableQuantity <= 0 || device.status !== 0"
              @click="$router.push('/borrow/apply?deviceId=' + device.id)">
              <el-icon><Calendar /></el-icon> 预约借用此设备
            </el-button>
            <el-button size="large" @click="showMaintenanceForm = true">
              <el-icon><SetUp /></el-icon> 报修
            </el-button>
          </div>
        </el-card>

        <!-- 维修记录 -->
        <el-card shadow="hover" style="margin-top:20px">
          <template #header><span>维修记录</span></template>
          <el-table :data="maintenanceList" border size="small" max-height="300" v-loading="maintLoading">
            <el-table-column prop="faultDesc" label="故障描述" min-width="120" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="80" align="center">
              <template #default="{ row }">
                <el-tag size="small" :type="['info','warning','success','danger'][row.status]">
                  {{ ['待处理','维修中','已修复','无法修复'][row.status] }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="报修时间" width="160" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 报修对话框 -->
    <el-dialog v-model="showMaintenanceForm" title="报修" width="500px">
      <el-form :model="maintForm" label-width="80px">
        <el-form-item label="故障描述" required>
          <el-input v-model="maintForm.faultDesc" type="textarea" :rows="4" placeholder="请描述故障情况" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showMaintenanceForm = false">取消</el-button>
        <el-button type="primary" @click="submitMaintenance">提交报修</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getDeviceById } from '@/api/device'
import { getMaintenancePage, addMaintenance } from '@/api/device'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()
const deviceId = route.params.id

const device = ref({})
const maintenanceList = ref([])
const showMaintenanceForm = ref(false)
const loading = ref(false)
const maintLoading = ref(false)
const maintForm = reactive({ deviceId, faultDesc: '' })

const statusLabel = (s) => ['正常', '维修中', '已报废', '外借中'][s] || '未知'
const statusTagType = (s) => ['success', 'warning', 'danger', ''][s] || 'info'

const loadDevice = async () => {
  loading.value = true
  try {
    const res = await getDeviceById(deviceId)
    device.value = res.data || {}
  } catch (e) {
    console.error('加载设备详情失败', e)
    ElMessage.error('加载设备详情失败')
  } finally {
    loading.value = false
  }
}

const loadMaintenance = async () => {
  maintLoading.value = true
  try {
    const res = await getMaintenancePage({ deviceId, current: 1, size: 20 })
    maintenanceList.value = res.data?.records || []
  } catch (e) {
    console.error('加载维修记录失败', e)
    ElMessage.error('加载维修记录失败')
  } finally {
    maintLoading.value = false
  }
}

const submitMaintenance = async () => {
  if (!maintForm.faultDesc) { ElMessage.warning('请填写故障描述'); return }
  try {
    // reportUserId 由后端从 X-User-Id Header 自动设置，无需前端传递
    await addMaintenance({ deviceId: maintForm.deviceId, faultDesc: maintForm.faultDesc })
    ElMessage.success('报修提交成功')
    showMaintenanceForm.value = false
    maintForm.faultDesc = ''
    loadMaintenance()
  } catch (e) {
    console.error('报修提交失败', e)
  }
}

onMounted(() => { loadDevice(); loadMaintenance() })
</script>
