<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background:#409EFF"><el-icon><Monitor /></el-icon></div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.totalDevices || 0 }}</p>
              <p class="stat-label">设备总数</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background:#67C23A"><el-icon><Document /></el-icon></div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.activeBorrows || 0 }}</p>
              <p class="stat-label">活跃借用</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background:#E6A23C"><el-icon><Clock /></el-icon></div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.pendingApprovals || 0 }}</p>
              <p class="stat-label">待审批</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background:#F56C6C"><el-icon><Warning /></el-icon></div>
            <div class="stat-info">
              <p class="stat-value">{{ stats.overdueCount || 0 }}</p>
              <p class="stat-label">逾期未还</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span>设备使用率 Top 10</span>
          </template>
          <div ref="usageChartRef" style="height:350px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span>月度借用趋势</span>
          </template>
          <div ref="trendChartRef" style="height:350px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats, getDeviceUsageTop, getMonthlyTrend } from '@/api/report'
import { ElMessage } from 'element-plus'

const stats = ref({})
const usageChartRef = ref(null)
const trendChartRef = ref(null)
let usageChart = null
let trendChart = null

onMounted(async () => {
  const [statsRes, usageRes, trendRes] = await Promise.allSettled([
    getDashboardStats(),
    getDeviceUsageTop(),
    getMonthlyTrend()
  ])

  // 处理统计卡片数据
  if (statsRes.status === 'fulfilled') {
    stats.value = statsRes.value.data || {}
  } else {
    console.error('加载统计数据失败:', statsRes.reason)
    ElMessage.warning('统计数据加载失败，部分数据可能不完整')
  }

  // 设备使用率图表
  if (usageRes.status === 'fulfilled' && usageRes.value.data && usageChartRef.value) {
    usageChart = echarts.init(usageChartRef.value)
    usageChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: usageRes.value.data.map(i => i.name.length > 6 ? i.name.substring(0,6)+'...' : i.name),
        axisLabel: { rotate: 30 }
      },
      yAxis: { type: 'value', name: '使用率(%)' },
      series: [{
        type: 'bar',
        data: usageRes.value.data.map(i => i.usageRate),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409EFF' },
            { offset: 1, color: '#67C23A' }
          ])
        }
      }]
    })
  } else if (usageRes.status === 'rejected') {
    console.error('加载使用率数据失败:', usageRes.reason)
    ElMessage.warning('设备使用率数据加载失败')
  }

  // 月度趋势图表
  if (trendRes.status === 'fulfilled' && trendRes.value.data && trendChartRef.value) {
    trendChart = echarts.init(trendChartRef.value)
    trendChart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['借用次数', '借用数量'] },
      xAxis: { type: 'category', data: trendRes.value.data.map(i => i.month) },
      yAxis: [
        { type: 'value', name: '次数' },
        { type: 'value', name: '数量' }
      ],
      series: [
        { name: '借用次数', type: 'line', data: trendRes.value.data.map(i => i.borrowCount), smooth: true },
        { name: '借用数量', type: 'bar', yAxisIndex: 1, data: trendRes.value.data.map(i => i.totalQuantity) }
      ]
    })
  } else if (trendRes.status === 'rejected') {
    console.error('加载趋势数据失败:', trendRes.reason)
    ElMessage.warning('月度趋势数据加载失败')
  }

  window.addEventListener('resize', handleResize)
})

const handleResize = () => {
  usageChart?.resize()
  trendChart?.resize()
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  usageChart?.dispose()
  trendChart?.dispose()
})
</script>

<style scoped>
.stat-cards .stat-card {
  margin-bottom: 0;
}
.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
}
.stat-info .stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}
.stat-info .stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
</style>
