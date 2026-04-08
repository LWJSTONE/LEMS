<template>
  <div class="borrow-apply">
    <el-card shadow="hover">
      <template #header><span>设备预约借用</span></template>

      <el-row :gutter="20">
        <el-col :span="14">
          <!-- 设备选择 -->
          <el-form :model="form" label-width="100px" ref="formRef" :rules="rules">
            <el-form-item label="选择设备" prop="deviceId">
              <el-select v-model="form.deviceId" placeholder="请选择设备" filterable style="width:100%" @change="onDeviceChange">
                <el-option v-for="d in deviceList" :key="d.id" :label="`${d.code} - ${d.name}`" :value="d.id" />
              </el-select>
            </el-form-item>

            <!-- 设备信息卡片 -->
            <el-card v-if="selectedDevice" shadow="never" class="device-info-card">
              <el-descriptions :column="2" size="small">
                <el-descriptions-item label="设备名称">{{ selectedDevice.name }}</el-descriptions-item>
                <el-descriptions-item label="规格型号">{{ selectedDevice.model }}</el-descriptions-item>
                <el-descriptions-item label="可用数量">
                  <span :style="{ color: selectedDevice.availableQuantity > 0 ? '#67C23A' : '#F56C6C', fontWeight: 700 }">
                    {{ selectedDevice.availableQuantity }} {{ selectedDevice.unit }}
                  </span>
                </el-descriptions-item>
                <el-descriptions-item label="存放位置">{{ selectedDevice.locationDetail || '-' }}</el-descriptions-item>
              </el-descriptions>
            </el-card>

            <el-form-item label="借用数量" prop="borrowQuantity">
              <el-input-number v-model="form.borrowQuantity" :min="1"
                :max="selectedDevice ? selectedDevice.availableQuantity : 1" />
            </el-form-item>

            <el-form-item label="借用时间" prop="dateRange">
              <el-date-picker v-model="form.dateRange" type="datetimerange"
                range-separator="至" start-placeholder="开始时间" end-placeholder="归还时间"
                format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DDTHH:mm:ss"
                style="width:100%" />
            </el-form-item>

            <el-form-item label="用途说明" prop="purpose">
              <el-input v-model="form.purpose" type="textarea" :rows="3" placeholder="请说明借用用途" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" size="large" :loading="submitting" @click="submitApply">
                <el-icon><Promotion /></el-icon> 提交申请
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>

        <el-col :span="10">
          <el-alert type="info" :closable="false" show-icon>
            <template #title>预约须知</template>
            <p>1. 提交申请后，设备库存将被预占，请耐心等待审批。</p>
            <p>2. 审批通过后，请在预约时间内到指定地点领取设备。</p>
            <p>3. 请按时归还设备，逾期将产生违约记录。</p>
            <p>4. 如需取消预约，请在审批前操作，库存将自动释放。</p>
          </el-alert>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDevicePage, getDeviceById } from '@/api/device'
import { applyBorrow } from '@/api/borrow'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const submitting = ref(false)

const deviceList = ref([])
const selectedDevice = ref(null)
const form = reactive({
  deviceId: null, borrowQuantity: 1, dateRange: null, purpose: ''
})
const rules = {
  deviceId: [{ required: true, message: '请选择设备', trigger: 'change' }],
  borrowQuantity: [{ required: true, message: '请输入借用数量', trigger: 'change' }],
  dateRange: [{ required: true, message: '请选择借用时间', trigger: 'change' }]
}

const loadDevices = async () => {
  try {
    const res = await getDevicePage({ current: 1, size: 100, status: 0 })
    deviceList.value = (res.data?.records || []).filter(d => d.availableQuantity > 0)
  } catch (e) {
    console.error('加载设备列表失败', e)
  }
}

const onDeviceChange = async (deviceId) => {
  if (deviceId) {
    try {
      const res = await getDeviceById(deviceId)
      selectedDevice.value = res.data || {}
      form.borrowQuantity = 1
    } catch (e) {
      console.error('加载设备详情失败', e)
      selectedDevice.value = null
    }
  } else {
    selectedDevice.value = null
  }
}

const submitApply = async () => {
  try {
    await formRef.value.validate()
  } catch (e) { return }

  submitting.value = true
  try {
    await applyBorrow({
      deviceId: form.deviceId,
      borrowQuantity: form.borrowQuantity,
      startTime: form.dateRange[0],
      endTime: form.dateRange[1],
      purpose: form.purpose
    })
    ElMessage.success('申请提交成功，等待审批')
    router.push('/borrow/my')
  } catch (e) {
    // error handled by interceptor
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadDevices()
  if (route.query.deviceId) {
    form.deviceId = Number(route.query.deviceId)
    onDeviceChange(form.deviceId)
  }
})
</script>

<style scoped>
.device-info-card { margin-bottom: 16px; background: #f5f7fa; }
.device-info-card p { margin: 2px 0; }
</style>
