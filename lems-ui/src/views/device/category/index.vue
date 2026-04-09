<template>
  <div class="device-category">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>设备分类管理</span>
          <el-button type="primary" @click="handleAdd(null)">
            <el-icon><Plus /></el-icon> 新增顶级分类
          </el-button>
        </div>
      </template>
      <el-table :data="categoryTree" row-key="id" border default-expand-all :tree-props="{ children: 'children' }" v-loading="loading">
        <el-table-column prop="name" label="分类名称" min-width="200" />
        <el-table-column prop="sortOrder" label="排序" width="100" align="center" />
        <el-table-column label="操作" width="260">
          <template #default="{ row }">
            <el-button size="small" @click="handleAdd(row.id)">添加子分类</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-popconfirm title="确认删除?" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑分类' : '新增分类'" width="450px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类名称" required>
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sortOrder" :min="0" />
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
import { ref, reactive, onMounted } from 'vue'
import { getCategoryTree, addCategory, updateCategory, deleteCategory } from '@/api/device'
import { ElMessage } from 'element-plus'

const categoryTree = ref([])
const dialogVisible = ref(false)
const loading = ref(false)
const form = reactive({ id: null, name: '', parentId: 0, sortOrder: 0 })

const loadData = async () => {
  loading.value = true
  try {
    const res = await getCategoryTree()
    categoryTree.value = res.data || []
  } catch (e) {
    console.error('加载分类树失败', e)
    ElMessage.error('加载分类树失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = (parentId) => {
  Object.assign(form, { id: null, name: '', parentId: parentId || 0, sortOrder: 0 })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, { id: row.id, name: row.name, parentId: row.parentId, sortOrder: row.sortOrder })
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!form.name) { ElMessage.warning('请填写分类名称'); return }
  try {
    if (form.id) {
      await updateCategory(form)
      ElMessage.success('修改成功')
    } else {
      await addCategory(form)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) {
    console.error('提交分类失败', e)
    ElMessage.error('提交分类失败')
  }
}

const handleDelete = async (id) => {
  try {
    await deleteCategory(id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    console.error('删除分类失败', e)
    ElMessage.error('删除分类失败')
  }
}

onMounted(loadData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
