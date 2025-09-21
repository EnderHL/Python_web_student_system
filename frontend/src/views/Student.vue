<template>
  <div class="student-container">
    <header class="app-header">
      <div class="header-content">
        <h1>学生管理系统 - 学生管理</h1>
        <div class="user-info">
          <span>{{ user?.username }}</span>
          <button @click="handleLogout" class="logout-btn">退出登录</button>
        </div>
      </div>
    </header>

    <nav class="sidebar">
      <ul class="nav-menu">
        <li class="nav-item">
          <router-link to="/" class="nav-link">首页</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/teacher" class="nav-link">教师管理</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/student" class="nav-link active">学生管理</router-link>
        </li>
      </ul>
    </nav>

    <main class="main-content">
      <div class="student-header">
        <h2>学生管理</h2>
        <button @click="showAddForm = !showAddForm" class="add-btn">
          {{ showAddForm ? '取消添加' : '添加学生' }}
        </button>
      </div>

      <!-- 添加学生表单 -->
      <div v-if="showAddForm" class="add-student-form">
        <h3>添加新学生</h3>
        <form @submit.prevent="addStudent">
          <div class="form-row">
            <div class="form-group">
              <label>姓名</label>
              <input v-model="studentForm.name" required placeholder="请输入姓名" />
            </div>
            <div class="form-group">
              <label>年龄</label>
              <input type="number" v-model="studentForm.age" required placeholder="请输入年龄" />
            </div>
            <div class="form-group">
              <label>性别</label>
              <select v-model="studentForm.gender">
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>班级</label>
              <input v-model="studentForm.class_name" required placeholder="请输入班级" />
            </div>
            <div class="form-group">
              <label>学号</label>
              <input v-model="studentForm.student_id" required placeholder="请输入学号" />
            </div>
            <div class="form-group">
              <label>学院</label>
              <input v-model="studentForm.college" required placeholder="请输入学院" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>电话</label>
              <input v-model="studentForm.phone" placeholder="请输入电话" />
            </div>
          </div>
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? '提交中...' : '添加学生' }}
          </button>
        </form>
      </div>

      <!-- 学生列表 -->
      <div class="student-list">
        <h3>学生列表</h3>
        <div class="search-container">
          <div class="search-input-wrapper">
            <input v-model="searchQuery" placeholder="搜索学生..." class="search-input" />
            <button @click="handleSearch" class="search-btn">搜索</button>
          </div>
        </div>
        <table class="student-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>年龄</th>
              <th>性别</th>
              <th>班级</th>
              <th>学号</th>
              <th>学院</th>
              <th>电话</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in filteredStudents" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.name }}</td>
              <td>{{ student.age }}</td>
              <td>{{ student.gender }}</td>
              <td>{{ student.class_name }}</td>
              <td>{{ student.student_id }}</td>
              <td>{{ student.college }}</td>
              <td>{{ student.phone || '-' }}</td>
              <td>
                <button @click="editStudent(student)" class="edit-btn">编辑</button>
                <button @click="deleteStudent(student.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="students.length === 0" class="no-data">暂无学生数据</div>
      </div>

      <!-- 编辑学生对话框 -->
      <div v-if="editingStudent" class="modal-overlay" @click="closeEditModal">
        <div class="modal-content" @click.stop>
          <h3>编辑学生</h3>
          <form @submit.prevent="updateStudent">
            <div class="form-row">
              <div class="form-group">
                <label>姓名</label>
                <input v-model="editForm.name" required placeholder="请输入姓名" />
              </div>
              <div class="form-group">
                <label>年龄</label>
                <input type="number" v-model="editForm.age" required placeholder="请输入年龄" />
              </div>
              <div class="form-group">
                <label>性别</label>
                <select v-model="editForm.gender">
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>班级</label>
                <input v-model="editForm.class_name" required placeholder="请输入班级" />
              </div>
              <div class="form-group">
                <label>学号</label>
                <input v-model="editForm.student_id" required placeholder="请输入学号" />
              </div>
              <div class="form-group">
                <label>学院</label>
                <input v-model="editForm.college" required placeholder="请输入学院" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>电话</label>
                <input v-model="editForm.phone" placeholder="请输入电话" />
              </div>
            </div>
            <div class="modal-actions">
              <button type="button" @click="closeEditModal" class="cancel-btn">取消</button>
              <button type="submit" :disabled="loading" class="submit-btn">
                {{ loading ? '更新中...' : '更新' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-message">{{ error }}</div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import api from '../utils/axios'

export default {
  name: 'Student',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    return {
      authStore,
      router
    }
  },
  data() {
    return {
      user: null,
      students: [],
      searchQuery: '',
      showAddForm: false,
      editingStudent: null,
      studentForm: {
          name: '',
          age: '',
          gender: '男',
          class_name: '',
          student_id: '',
          college: '',
          phone: ''
        },
      editForm: {
        name: '',
        age: '',
        gender: '男',
        class_name: '',
        student_id: '',
        phone: ''
      },
      loading: false,
      error: ''
    }
  },
  computed: {
    filteredStudents() {
      // 过滤掉students数组中的null值
      const validStudents = this.students.filter(student => student !== null)
      
      if (!this.searchQuery) return validStudents
      return validStudents.filter(student => 
        student.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        student.class_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        student.student_id.includes(this.searchQuery) ||
        student.college.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        student.phone.includes(this.searchQuery)
      )
    }
  },
  mounted() {
    this.loadUserInfo()
    this.loadStudents()
  },
  methods: {
    async loadUserInfo() {
      try {
        await this.authStore.fetchUserInfo()
        this.user = this.authStore.user
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    },
    async handleLogout() {
      try {
        await this.authStore.logout()
        this.router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
    async loadStudents() {
      try {
        const response = await api.get('/students/')
        // 检查是否存在分页对象，如果存在则使用results字段
        this.students = response.data?.results || response.data || []
      } catch (error) {
        this.error = '获取学生列表失败'
        console.error('Failed to load students:', error)
        // 发生错误时设置为空数组以避免后续渲染错误
        this.students = []
      }
    },
    async addStudent() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.post('/students/', this.studentForm)
        // 确保将新学生数据（response.data）添加到数组中
        this.students.push(response.data)
        
        // 重置表单
        this.studentForm = {
          name: '',
          age: '',
          gender: '男',
          class_name: '',
          student_id: '',
          phone: ''
        }
        
        this.showAddForm = false
      } catch (error) {
        this.error = '添加学生失败'
        console.error('Failed to add student:', error)
      } finally {
        this.loading = false
      }
    },
    editStudent(student) {
      this.editingStudent = student
      // 复制学生信息到编辑表单
      this.editForm = {
        name: student.name,
        age: student.age,
        gender: student.gender,
        class_name: student.class_name,
        student_id: student.student_id,
        college: student.college || '',
        phone: student.phone || ''
      }
    },
    closeEditModal() {
      this.editingStudent = null
    },
    async updateStudent() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.put(`/students/${this.editingStudent.id}/`, this.editForm)
        
        // 更新学生列表中的数据
        const index = this.students.findIndex(s => s.id === this.editingStudent.id)
        if (index !== -1) {
          // 确保使用response.data更新学生数据
          this.students[index] = response.data
        }
        
        this.closeEditModal()
      } catch (error) {
        this.error = '更新学生信息失败'
        console.error('Failed to update student:', error)
      } finally {
        this.loading = false
      }
    },
    async deleteStudent(id) {
      if (confirm('确定要删除这位学生吗？')) {
        try {
          await api.delete(`/students/${id}/`)
          // 从列表中移除
          this.students = this.students.filter(student => student.id !== id)
        } catch (error) {
          this.error = '删除学生失败'
          console.error('Failed to delete student:', error)
        }
      }
    },
    handleSearch() {
      // 搜索功能已通过computed属性实现，这里可以添加额外的搜索逻辑
      // 例如日志记录或特定的搜索动画等
    }
  }
}
</script>

<style scoped>
/* 样式与Teacher.vue类似 */
.student-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  background-color: #2196F3;
  color: white;
  padding: 15px 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logout-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.logout-btn:hover {
  background-color: #d32f2f;
}

.sidebar {
  width: 200px;
  background-color: #f5f5f5;
  height: calc(100vh - 64px);
  position: fixed;
  left: 0;
  top: 64px;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  padding: 0;
}

.nav-link {
  display: block;
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  border-bottom: 1px solid #e0e0e0;
}

.nav-link:hover,
.nav-link.active {
  background-color: #e0e0e0;
}

.main-content {
  margin-left: 200px;
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.student-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.student-header h2 {
  margin: 0;
  color: #333;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.add-btn:hover {
  background-color: #45a049;
}

.add-student-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.add-student-form h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.student-list {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.student-list h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 15px;
}

.search-container {
  margin-bottom: 15px;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-right: none;
  border-radius: 4px 0 0 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.search-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 14px;
}

.search-btn:hover {
  background-color: #0b7dda;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
}

.student-table th,
.student-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
  color: #000;
}

.student-table th {
  background-color: #f5f5f5;
  font-weight: 500;
  color: #333;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  margin-right: 5px;
}

.edit-btn:hover {
  background-color: #0b7dda;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #999;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 600px;
}

.modal-content h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 20px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-top: 15px;
}
</style>