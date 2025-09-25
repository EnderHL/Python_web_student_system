<template>
  <div class="teacher-container">
    <!-- 教师管理区域头部，包含标题和添加按钮 -->
    <div class="teacher-header">
      <h2>教师管理</h2>
      <el-button @click="showAddForm = !showAddForm" type="primary" :icon="showAddForm ? 'Delete' : 'Plus'">
        {{ showAddForm ? '取消添加' : '添加教师' }}
      </el-button>
    </div>

    <!-- 添加教师表单，根据showAddForm状态显示或隐藏 -->
    <el-card v-if="showAddForm" class="add-teacher-form">
      <template #header>
        <div class="card-header">
          <span>添加新教师</span>
        </div>
      </template>
      <el-form ref="addFormRef" :model="teacherForm" :rules="formRules" label-width="80px" size="default">
        <el-row :gutter="15">
          <el-col :span="8">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="teacherForm.name" placeholder="请输入姓名" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="年龄" prop="age">
              <el-input v-model.number="teacherForm.age" placeholder="请输入年龄" type="number" min="18" max="65" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="teacherForm.gender" placeholder="请选择性别">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="15">
          <el-col :span="8">
            <el-form-item label="职称" prop="title">
              <el-input v-model="teacherForm.title" placeholder="请输入职称" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="部门" prop="department">
              <el-input v-model="teacherForm.department" placeholder="请输入部门" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="电话" prop="phone">
              <el-input v-model="teacherForm.phone" placeholder="请输入电话" clearable />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="15">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="teacherForm.email" placeholder="请输入邮箱" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入职日期" prop="hire_date">
              <el-date-picker v-model="teacherForm.hire_date" type="date" placeholder="请选择入职日期" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="handleAddTeacher" :loading="loading">
            {{ loading ? '提交中...' : '添加教师' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 教师列表区域，包含搜索和表格 -->
    <el-card class="teacher-list">
      <template #header>
        <div class="card-header">
          <span>教师列表</span>
        </div>
      </template>
      <div class="search-container">
        <el-input v-model="searchQuery" placeholder="搜索教师..." clearable class="search-input" />
      </div>
      <el-table v-loading="loading" :data="filteredTeachers" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="姓名" width="120" align="center" />
        <el-table-column prop="age" label="年龄" width="80" align="center" />
        <el-table-column prop="gender" label="性别" width="80" align="center" />
        <el-table-column prop="title" label="职称" align="center" />
        <el-table-column prop="department" label="部门" align="center" />
        <el-table-column prop="phone" label="电话" align="center" />
        <el-table-column prop="email" label="邮箱" align="center" />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <el-button type="primary" @click="editTeacher(scope.row)" size="small" :icon="'Edit'">编辑</el-button>
            <el-button type="danger" @click="deleteTeacher(scope.row.id)" size="small" :icon="'Delete'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 无数据提示 -->
      <div v-if="teachers.length === 0 && !loading" class="no-data">暂无教师数据</div>
    </el-card>

    <!-- 编辑教师对话框，点击编辑按钮时显示 -->
    <el-dialog v-model="editingTeacher" title="编辑教师" width="600px" center>
      <el-form ref="editFormRef" :model="editForm" :rules="formRules" label-width="80px" size="default">
        <el-row :gutter="15">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="editForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input v-model.number="editForm.age" placeholder="请输入年龄" type="number" min="18" max="65" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="15">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="editForm.gender" placeholder="请选择性别">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="职称" prop="title">
              <el-input v-model="editForm.title" placeholder="请输入职称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="15">
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-input v-model="editForm.department" placeholder="请输入部门" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电话" prop="phone">
              <el-input v-model="editForm.phone" placeholder="请输入电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="15">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="editForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入职日期" prop="hire_date">
              <el-date-picker v-model="editForm.hire_date" type="date" placeholder="请选择入职日期" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="closeEditModal">取消</el-button>
        <el-button type="primary" @click="updateTeacher" :loading="loading">
          {{ loading ? '更新中...' : '更新' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import api from '../utils/axios'
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton, ElTable, ElTableColumn, ElDialog, ElDatePicker, ElRow, ElCol, ElCard } from 'element-plus'

export default {
  name: 'Teacher',
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElSelect,
    ElOption,
    ElButton,
    ElTable,
    ElTableColumn,
    ElDialog,
    ElDatePicker,
    ElRow,
    ElCol,
    ElCard
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const user = ref(null)
    const teachers = ref([])
    const searchQuery = ref('')
    const showAddForm = ref(false)
    const editingTeacher = ref(null)
    const loading = ref(false)
    const error = ref('')
    const addFormRef = ref(null)
    const editFormRef = ref(null)
    
    // 添加教师表单数据
    const teacherForm = reactive({
      name: '',
      age: '',
      gender: '男',
      title: '',
      department: '',
      phone: '',
      email: '',
      hire_date: ''
    })
    
    // 编辑教师表单数据
    const editForm = reactive({
      name: '',
      age: '',
      gender: '男',
      title: '',
      department: '',
      phone: '',
      email: '',
      hire_date: ''
    })
    
    // 表单验证规则
    const formRules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      age: [
        { required: true, message: '请输入年龄', trigger: 'blur' },
        { type: 'number', min: 18, max: 65, message: '年龄必须在18-65之间', trigger: 'blur' }
      ],
      gender: [
        { required: true, message: '请选择性别', trigger: 'change' }
      ],
      title: [
        { required: true, message: '请输入职称', trigger: 'blur' }
      ],
      department: [
        { required: true, message: '请输入部门', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
      ],
      hire_date: [
        { required: true, message: '请选择入职日期', trigger: 'change' }
      ]
    }
    
    // 计算属性：根据搜索查询过滤教师列表
    const filteredTeachers = computed(() => {
      // 过滤掉teachers数组中的null值
      const validTeachers = teachers.value.filter(teacher => teacher !== null)
      
      if (!searchQuery.value) return validTeachers
      return validTeachers.filter(teacher => 
        teacher.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (teacher.title && teacher.title.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
        (teacher.department && teacher.department.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
        (teacher.phone && teacher.phone.includes(searchQuery.value))
      )
    })
    
    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        await authStore.fetchUserInfo()
        user.value = authStore.user
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    }
    
    // 处理退出登录
    const handleLogout = async () => {
      try {
        await authStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    // 加载教师列表数据
    const loadTeachers = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await api.get('/teachers/')
        // API返回的是分页对象，教师数据在results字段中
        teachers.value = response.data && response.data.results && Array.isArray(response.data.results) 
          ? response.data.results 
          : []
        // 打印教师列表数据到控制台
        console.log('教师列表数据:', teachers.value)
      } catch (error) {
        error.value = '获取教师列表失败'
        ElMessage.error('获取教师列表失败')
        console.error('Failed to load teachers:', error)
        teachers.value = [] // 确保teachers是数组类型
      } finally {
        loading.value = false
      }
    }
    
    // 添加新教师
    const handleAddTeacher = async () => {
      addFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          error.value = ''
          
          try {
            const response = await api.post('/teachers/', teacherForm)
            // 确保将新教师数据添加到数组中
            teachers.value.push(response.data)
            
            // 重置表单
            Object.assign(teacherForm, {
              name: '',
              age: '',
              gender: '男',
              title: '',
              department: '',
              phone: '',
              email: '',
              hire_date: ''
            })
            
            showAddForm.value = false // 隐藏添加表单
            ElMessage.success('教师添加成功')
          } catch (error) {
            ElMessage.error('添加教师失败')
            console.error('Failed to add teacher:', error)
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    // 编辑教师信息
    const editTeacher = (teacher) => {
      editingTeacher.value = teacher
      // 复制教师信息到编辑表单
      Object.assign(editForm, {
        name: teacher.name,
        age: teacher.age,
        gender: teacher.gender,
        title: teacher.title || '',
        department: teacher.department || '',
        phone: teacher.phone || '',
        email: teacher.email || '',
        hire_date: teacher.hire_date || ''
      })
    }
    
    // 关闭编辑对话框
    const closeEditModal = () => {
      editingTeacher.value = false
      editFormRef.value?.resetFields()
    }
    
    // 更新教师信息
    const updateTeacher = async () => {
      editFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          error.value = ''
          
          try {
            const response = await api.put(`/teachers/${editingTeacher.value.id}/`, editForm)
            
            // 更新教师列表中的数据
            const index = teachers.value.findIndex(t => t.id === editingTeacher.value.id)
            if (index !== -1) {
              // 确保使用response.data更新教师数据
              teachers.value[index] = response.data
            }
            
            closeEditModal() // 关闭编辑对话框
            ElMessage.success('教师信息更新成功')
          } catch (error) {
            ElMessage.error('更新教师信息失败')
            console.error('Failed to update teacher:', error)
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    // 删除教师
    const deleteTeacher = async (id) => {
      ElMessageBox.confirm(
        '确定要删除这位教师吗？',
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
        .then(async () => {
          try {
            await api.delete(`/teachers/${id}/`)
            // 从列表中移除
            teachers.value = teachers.value.filter(teacher => teacher.id !== id)
            ElMessage.success('教师删除成功')
          } catch (error) {
            ElMessage.error('删除教师失败')
            console.error('Failed to delete teacher:', error)
          }
        })
        .catch(() => {
          // 用户取消删除
        })
    }
    
    // 组件挂载时执行的方法
    onMounted(() => {
      loadUserInfo() // 加载用户信息
      loadTeachers() // 加载教师列表数据
    })
    
    return {
      authStore,
      router,
      user,
      teachers,
      searchQuery,
      showAddForm,
      editingTeacher,
      loading,
      error,
      teacherForm,
      editForm,
      addFormRef,
      editFormRef,
      formRules,
      filteredTeachers,
      loadUserInfo,
      handleLogout,
      loadTeachers,
      handleAddTeacher,
      editTeacher,
      closeEditModal,
      updateTeacher,
      deleteTeacher
    }
  }
}
</script>

<style scoped>
.teacher-container {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

<style scoped src="../styles/Teacher.css"></style>
