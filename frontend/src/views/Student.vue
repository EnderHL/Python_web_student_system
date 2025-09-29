<template>
  <div class="student-container">
    <div class="student-main">
      <div class="student-header">
        <h2>学生管理</h2>
        <el-button @click="showAddForm = !showAddForm" :type="showAddForm ? 'default' : 'primary'"
          :icon="showAddForm ? Remove : Plus"
        >
          {{ showAddForm ? '取消添加' : '添加学生' }}
        </el-button>
      </div>

      <!-- 添加学生表单 -->
      <el-card v-if="showAddForm" class="add-student-form">
        <template #header>
          <div class="card-header">
            <span>添加新学生</span>
          </div>
        </template>
        <el-form
          ref="addFormRef"
          :model="studentForm"
          :rules="addFormRules"
          label-width="80px"
          @submit.prevent="addStudent"
        >
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="姓名" prop="name">
                <el-input v-model="studentForm.name" placeholder="请输入姓名" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="年龄" prop="age">
                <el-input type="number" v-model.number="studentForm.age" placeholder="请输入年龄" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="性别" prop="gender">
                <el-select v-model="studentForm.gender" placeholder="请选择性别">
                  <el-option label="男" value="男" />
                  <el-option label="女" value="女" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="班级" prop="class_name">
                <el-input v-model="studentForm.class_name" placeholder="请输入班级" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="学号" prop="student_id">
                <el-input v-model="studentForm.student_id" placeholder="请输入学号" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="学院" prop="college">
                <el-input v-model="studentForm.college" placeholder="请输入学院" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="电话" prop="phone">
                <el-input v-model="studentForm.phone" placeholder="请输入电话" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="addStudent">
              {{ loading ? '提交中...' : '添加学生' }}
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 学生列表 -->
      <el-card class="student-list">
        <template #header>
          <div class="card-header">
            <span>学生列表</span>
          </div>
        </template>
        <div class="search-container">
          <el-input
            v-model="searchQuery"
            placeholder="搜索学生..."
            clearable
            style="width: 300px;"
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button @click="handleSearch" :icon="Search" />
            </template>
          </el-input>
        </div>
        <el-table
          v-if="students.length > 0"
          :data="filteredStudents"
          style="width: 100%;"
          border
          stripe
          empty-text="暂无学生数据"
        >
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="name" label="姓名" min-width="100" align="center" />
          <el-table-column prop="age" label="年龄" width="80" align="center" />
          <el-table-column prop="gender" label="性别" width="80" align="center" />
          <el-table-column prop="class_name" label="班级" min-width="120" align="center" />
          <el-table-column prop="student_id" label="学号" min-width="120" align="center" />
          <el-table-column prop="college" label="学院" min-width="120" align="center" />
          <el-table-column prop="phone" label="电话" min-width="120" align="center">
            <template #default="scope">{{ scope.row.phone || '-' }}</template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right" align="center">
            <template #default="scope">
              <el-button @click="editStudent(scope.row)" type="primary" size="small" :icon="Edit" />
              <el-button @click="deleteStudent(scope.row.id)" type="danger" size="small" :icon="Delete" />
            </template>
          </el-table-column>
        </el-table>
        <div v-else class="no-data">
          <el-empty description="暂无学生数据" />
        </div>
      </el-card>

      <!-- 编辑学生对话框 -->
      <el-dialog
        v-model="dialogVisible"
        title="编辑学生"
        width="50%"
        :before-close="closeEditModal"
      >
        <el-form
          ref="editFormRef"
          :model="editForm"
          :rules="editFormRules"
          label-width="80px"
        >
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="姓名" prop="name">
                <el-input v-model="editForm.name" placeholder="请输入姓名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="年龄" prop="age">
                <el-input type="number" v-model.number="editForm.age" placeholder="请输入年龄" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="性别" prop="gender">
                <el-select v-model="editForm.gender" placeholder="请选择性别">
                  <el-option label="男" value="男" />
                  <el-option label="女" value="女" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="班级" prop="class_name">
                <el-input v-model="editForm.class_name" placeholder="请输入班级" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="学号" prop="student_id">
                <el-input v-model="editForm.student_id" placeholder="请输入学号" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="学院" prop="college">
                <el-input v-model="editForm.college" placeholder="请输入学院" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="电话" prop="phone">
                <el-input v-model="editForm.phone" placeholder="请输入电话" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="closeEditModal">取消</el-button>
            <el-button type="primary" :loading="loading" @click="updateStudent">
              {{ loading ? '更新中...' : '更新' }}
            </el-button>
          </span>
        </template>
      </el-dialog>

      <!-- 错误提示 -->
      <el-message v-if="error" type="error" :message="error" :show-close="true" />
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ref, reactive, computed, onMounted } from 'vue'
import { Plus, Remove, Search, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../utils/axios'

export default {
  name: 'Student',
  components: {
    Plus,
    Remove,
    Search,
    Edit,
    Delete
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    // 状态管理
    const students = ref([])
    const searchQuery = ref('')
    const showAddForm = ref(false)
    const dialogVisible = ref(false)
    const editingStudent = ref(null)
    const loading = ref(false)
    const error = ref('')
    const addFormRef = ref(null)
    const editFormRef = ref(null)
    
    // 表单数据
    const studentForm = reactive({
      name: '',
      age: '',
      gender: '男',
      class_name: '',
      student_id: '',
      college: '',
      phone: ''
    })
    
    const editForm = reactive({
      name: '',
      age: '',
      gender: '男',
      class_name: '',
      student_id: '',
      college: '',
      phone: ''
    })
    
    // 表单验证规则
    const addFormRules = {
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      age: [
        { required: true, message: '请输入年龄', trigger: 'blur' },
        { type: 'number', min: 1, max: 120, message: '年龄应在1-120之间', trigger: 'blur' }
      ],
      gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
      class_name: [{ required: true, message: '请输入班级', trigger: 'blur' }],
      student_id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
      college: [{ required: true, message: '请输入学院', trigger: 'blur' }]
    }
    
    const editFormRules = {
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      age: [
        { required: true, message: '请输入年龄', trigger: 'blur' },
        { type: 'number', min: 1, max: 120, message: '年龄应在1-120之间', trigger: 'blur' }
      ],
      gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
      class_name: [{ required: true, message: '请输入班级', trigger: 'blur' }],
      student_id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
      college: [{ required: true, message: '请输入学院', trigger: 'blur' }]
    }
    
    // 计算属性 - 过滤学生列表
    const filteredStudents = computed(() => {
      const validStudents = students.value.filter(student => student !== null)
      
      if (!searchQuery.value) return validStudents
      return validStudents.filter(student => 
        student.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        student.class_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        student.student_id.includes(searchQuery.value) ||
        student.college.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        student.phone.includes(searchQuery.value)
      )
    })
    
    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        await authStore.fetchUserInfo()
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    }
    
    // 处理登出
    const handleLogout = async () => {
      try {
        await authStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    // 加载学生列表
    const loadStudents = async () => {
      try {
        const response = await api.get('/students/')
        students.value = response.data?.results || response.data || []
      } catch (err) {
        error.value = '获取学生列表失败'
        console.error('Failed to load students:', err)
        students.value = []
      }
    }
    
    // 添加学生
    const addStudent = async () => {
      try {
        await addFormRef.value.validate()
        loading.value = true
        error.value = ''
        
        const response = await api.post('/students/', studentForm)
        students.value.push(response.data)
        
        // 重置表单
        Object.keys(studentForm).forEach(key => {
          studentForm[key] = key === 'gender' ? '男' : ''
        })
        
        showAddForm.value = false
        
        // 成功提示
        ElMessage.success('添加学生成功')
      } catch (err) {
        if (err.name !== 'Error') {
          // 处理表单验证之外的错误
          error.value = '添加学生失败'
          console.error('Failed to add student:', err)
        }
      } finally {
        loading.value = false
      }
    }
    
    // 编辑学生
    const editStudent = (student) => {
      editingStudent.value = student
      // 复制学生信息到编辑表单
      Object.assign(editForm, {
        name: student.name,
        age: student.age,
        gender: student.gender,
        class_name: student.class_name,
        student_id: student.student_id,
        college: student.college || '',
        phone: student.phone || ''
      })
      dialogVisible.value = true
    }
    
    // 关闭编辑模态框
    const closeEditModal = () => {
      dialogVisible.value = false
      editingStudent.value = null
      if (editFormRef.value) {
        editFormRef.value.resetFields()
      }
    }
    
    // 更新学生
    const updateStudent = async () => {
      try {
        await editFormRef.value.validate()
        loading.value = true
        error.value = ''
        
        const response = await api.put(`/students/${editingStudent.value.id}/`, editForm)
        
        // 更新学生列表中的数据
        const index = students.value.findIndex(s => s.id === editingStudent.value.id)
        if (index !== -1) {
          students.value[index] = response.data
        }
        
        closeEditModal()
        
        // 成功提示
        ElMessage.success('更新学生信息成功')
      } catch (err) {
        if (err.name !== 'Error') {
          // 处理表单验证之外的错误
          error.value = '更新学生信息失败'
          console.error('Failed to update student:', err)
        }
      } finally {
        loading.value = false
      }
    }
    
    // 删除学生
    const deleteStudent = async (id) => {
      const confirmResult = await ElMessageBox.confirm(
        '确定要删除这位学生吗？',
        '确认删除',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      if (confirmResult === 'confirm') {
        try {
          await api.delete(`/students/${id}/`)
          students.value = students.value.filter(student => student.id !== id)
          ElMessage.success('删除学生成功')
        } catch (err) {
          error.value = '删除学生失败'
          console.error('Failed to delete student:', err)
        }
      }
    }
    
    // 搜索处理
    const handleSearch = () => {
      // 搜索功能已通过computed属性实现
      // 这里可以添加额外的搜索逻辑，例如日志记录或特定的搜索动画等
    }
    
    // 挂载时加载数据
    onMounted(() => {
      loadUserInfo()
      loadStudents()
    })
    
    return {
      students,
      searchQuery,
      showAddForm,
      dialogVisible,
      editingStudent,
      loading,
      error,
      addFormRef,
      editFormRef,
      studentForm,
      editForm,
      addFormRules,
      editFormRules,
      filteredStudents,
      loadUserInfo,
      handleLogout,
      loadStudents,
      addStudent,
      editStudent,
      closeEditModal,
      updateStudent,
      deleteStudent,
      handleSearch
    }
  }
}
</script>

  <style scoped>
  .student-container {
    width: 100%;
  }
  
  .student-main {
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .search-container {
    margin-bottom: 20px;
  }
  
  .no-data {
    padding: 40px 0;
    text-align: center;
  }
  </style>
  
  <style scoped src="../styles/Student.css"></style>
