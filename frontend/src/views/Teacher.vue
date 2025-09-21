<template>
  <!-- 主容器，控制整体布局 -->
  <div class="teacher-container">
    <!-- 页面头部，包含标题和用户信息 -->
    <header class="app-header">
      <div class="header-content">
        <h1>学生管理系统 - 教师管理</h1>
        <div class="user-info">
          <span>{{ user?.username }}</span>
          <button @click="handleLogout" class="logout-btn">退出登录</button>
        </div>
      </div>
    </header>

    <!-- 侧边导航栏，提供页面间的切换 -->
    <nav class="sidebar">
      <ul class="nav-menu">
        <li class="nav-item">
          <router-link to="/" class="nav-link">首页</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/teacher" class="nav-link active">教师管理</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/student" class="nav-link">学生管理</router-link>
        </li>
      </ul>
    </nav>

    <!-- 主内容区域，包含所有教师管理的功能 -->
    <main class="main-content">
      <!-- 教师管理区域头部，包含标题和添加按钮 -->
      <div class="teacher-header">
        <h2>教师管理</h2>
        <button @click="showAddForm = !showAddForm" class="add-btn">
          {{ showAddForm ? '取消添加' : '添加教师' }}
        </button>
      </div>

      <!-- 添加教师表单，根据showAddForm状态显示或隐藏 -->
      <div v-if="showAddForm" class="add-teacher-form">
        <h3>添加新教师</h3>
        <form @submit.prevent="addTeacher">
          <div class="form-row">
            <div class="form-group">
              <label>姓名</label>
              <input v-model="teacherForm.name" required placeholder="请输入姓名" />
            </div>
            <div class="form-group">
              <label>年龄</label>
              <input type="number" v-model="teacherForm.age" required placeholder="请输入年龄" />
            </div>
            <div class="form-group">
              <label>性别</label>
              <select v-model="teacherForm.gender">
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>职称</label>
              <input v-model="teacherForm.title" required placeholder="请输入职称" />
            </div>
            <div class="form-group">
              <label>部门</label>
              <input v-model="teacherForm.department" required placeholder="请输入部门" />
            </div>
            <div class="form-group">
              <label>电话</label>
              <input v-model="teacherForm.phone" placeholder="请输入电话" />
            </div>
            <div class="form-group">
              <label>邮箱</label>
              <input type="email" v-model="teacherForm.email" required placeholder="请输入邮箱" />
            </div>
            <div class="form-group">
              <label>入职日期</label>
              <input type="date" v-model="teacherForm.hire_date" required placeholder="请选择入职日期" />
            </div>
          </div>
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? '提交中...' : '添加教师' }}
          </button>
        </form>
      </div>

      <!-- 教师列表区域，包含搜索和表格 -->
      <div class="teacher-list">
        <h3>教师列表</h3>
        <div class="search-container">
          <div class="search-input-wrapper">
            <input v-model="searchQuery" placeholder="搜索教师..." class="search-input" />
            <button @click="handleSearch" class="search-btn">搜索</button>
          </div>
        </div>
        <table class="teacher-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>年龄</th>
              <th>性别</th>
              <th>职称</th>
              <th>部门</th>
              <th>电话</th>
              <th>邮箱</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <!-- 遍历过滤后的教师列表，渲染每个教师的信息行 -->
            <tr v-for="teacher in filteredTeachers" :key="teacher.id">
              <td>{{ teacher.id }}</td>
              <td>{{ teacher.name }}</td>
              <td>{{ teacher.age }}</td>
              <td>{{ teacher.gender }}</td>
              <td>{{ teacher.title || '-' }}</td>
              <td>{{ teacher.department || '-' }}</td>
              <td>{{ teacher.phone || '-' }}</td>
              <td>{{ teacher.email || '-' }}</td>
              <td>
                <button @click="editTeacher(teacher)" class="edit-btn">编辑</button>
                <button @click="deleteTeacher(teacher.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- 无数据提示 -->
        <div v-if="teachers.length === 0" class="no-data">暂无教师数据</div>
      </div>

      <!-- 编辑教师对话框，点击编辑按钮时显示 -->
      <div v-if="editingTeacher" class="modal-overlay" @click="closeEditModal">
        <div class="modal-content" @click.stop>
          <h3>编辑教师</h3>
          <form @submit.prevent="updateTeacher">
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
                <label>职称</label>
                <input v-model="editForm.title" required placeholder="请输入职称" />
              </div>
              <div class="form-group">
                <label>部门</label>
                <input v-model="editForm.department" required placeholder="请输入部门" />
              </div>
              <div class="form-group">
                <label>电话</label>
                <input v-model="editForm.phone" placeholder="请输入电话" />
              </div>
              <div class="form-group">
                <label>邮箱</label>
                <input type="email" v-model="editForm.email" required placeholder="请输入邮箱" />
              </div>
              <div class="form-group">
                <label>入职日期</label>
                <input type="date" v-model="editForm.hire_date" required placeholder="请选择入职日期" />
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

      <!-- 错误提示信息 -->
      <div v-if="error" class="error-message">{{ error }}</div>
    </main>
  </div>
</template>

<script>
// 导入必要的模块
import { useAuthStore } from '../stores/auth' // 导入认证相关的store
import { useRouter } from 'vue-router' // 导入路由
import api from '../utils/axios' // 导入axios实例

export default {
  name: 'Teacher', // 组件名称
  setup() {
    // 使用Composition API设置store和router
    const authStore = useAuthStore()
    const router = useRouter()
    
    return {
      authStore,
      router
    }
  },
  data() {
    // 组件数据定义
    return {
      user: null, // 当前登录用户信息
      teachers: [], // 教师列表数据，初始化为空数组
      searchQuery: '', // 搜索查询字符串
      showAddForm: false, // 是否显示添加教师表单
      editingTeacher: null, // 当前正在编辑的教师对象
      // 添加教师表单数据
      teacherForm: {
        name: '',
        age: '',
        gender: '男',
        title: '',
        department: '',
        phone: '',
        email: '',
        hire_date: ''
      },
      // 编辑教师表单数据
      editForm: {
        name: '',
        age: '',
        gender: '男',
        title: '',
        department: '',
        phone: '',
        email: '',
        hire_date: ''
      },
      loading: false, // 加载状态标志
      error: '' // 错误信息
    }
  },
  computed: {
    // 计算属性：根据搜索查询过滤教师列表
    filteredTeachers() {
      // 过滤掉teachers数组中的null值
      const validTeachers = this.teachers.filter(teacher => teacher !== null)
      
      if (!this.searchQuery) return validTeachers
      return validTeachers.filter(teacher => 
        teacher.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        (teacher.title && teacher.title.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
        (teacher.department && teacher.department.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
        teacher.phone.includes(this.searchQuery)
      )
    }
  },
  mounted() {
    // 组件挂载时执行的方法
    this.loadUserInfo() // 加载用户信息
    this.loadTeachers() // 加载教师列表数据
  },
  methods: {
     // 搜索教师
     handleSearch() {
       // 搜索逻辑已通过computed属性filteredTeachers实现
       // 点击按钮时可以添加额外的搜索逻辑或UI反馈
     },
     // 加载用户信息
    async loadUserInfo() {
      try {
        await this.authStore.fetchUserInfo()
        this.user = this.authStore.user
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    },
    // 处理退出登录
    async handleLogout() {
      try {
        await this.authStore.logout()
        this.router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
    // 加载教师列表数据
    async loadTeachers() {
      this.loading = true
      
      try {
        const response = await api.get('/teachers/')
        // API返回的是分页对象，教师数据在results字段中
        this.teachers = response.data && response.data.results && Array.isArray(response.data.results) 
          ? response.data.results 
          : []
        // 打印教师列表数据到控制台
        console.log('教师列表数据:', this.teachers)
      } catch (error) {
        this.error = '获取教师列表失败'
        console.error('Failed to load teachers:', error)
        this.teachers = [] // 确保teachers是数组类型
      } finally {
        this.loading = false
      }
    },
    // 添加新教师
    async addTeacher() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.post('/teachers/', this.teacherForm)
        // 确保将新教师数据添加到数组中
        this.teachers.push(response.data)
        
        // 重置表单
        this.teacherForm = {
          name: '',
          age: '',
          gender: '男',
          title: '',
          department: '',
          phone: '',
          email: '',
          hire_date: ''
        }
        
        this.showAddForm = false // 隐藏添加表单
      } catch (error) {
        this.error = '添加教师失败'
        console.error('Failed to add teacher:', error)
      } finally {
        this.loading = false
      }
    },
    // 编辑教师信息
    editTeacher(teacher) {
      this.editingTeacher = teacher
      // 复制教师信息到编辑表单
        this.editForm = {
          name: teacher.name,
          age: teacher.age,
          gender: teacher.gender,
          title: teacher.title || '',
          department: teacher.department || '',
          phone: teacher.phone || '',
          email: teacher.email || '',
          hire_date: teacher.hire_date || ''
        }
    },
    // 关闭编辑对话框
    closeEditModal() {
      this.editingTeacher = null
    },
    // 更新教师信息
    async updateTeacher() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.put(`/teachers/${this.editingTeacher.id}/`, this.editForm)
        
        // 更新教师列表中的数据
        const index = this.teachers.findIndex(t => t.id === this.editingTeacher.id)
        if (index !== -1) {
          // 确保使用response.data更新教师数据
          this.teachers[index] = response.data
        }
        
        this.closeEditModal() // 关闭编辑对话框
      } catch (error) {
        this.error = '更新教师信息失败'
        console.error('Failed to update teacher:', error)
      } finally {
        this.loading = false
      }
    },
    // 删除教师
    async deleteTeacher(id) {
      if (confirm('确定要删除这位教师吗？')) {
        try {
          await api.delete(`/teachers/${id}/`)
          // 从列表中移除
          this.teachers = this.teachers.filter(teacher => teacher.id !== id)
        } catch (error) {
          this.error = '删除教师失败'
          console.error('Failed to delete teacher:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
/* 样式与Home.vue类似，但包含了表单和表格样式 */

/* 主容器样式，控制整体布局为垂直方向，高度100vh占据整屏 */
.teacher-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* 页面头部样式，蓝色背景，白色文字 */
.app-header {
  background-color: #2196F3;
  color: white;
  padding: 15px 20px;
}

/* 头部内容样式，使用flex布局实现两端对齐 */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

/* 头部标题样式 */
.header-content h1 {
  margin: 0;
  font-size: 24px;
}

/* 用户信息区域样式 */
.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 退出登录按钮样式 */
.logout-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 退出登录按钮悬停样式 */
.logout-btn:hover {
  background-color: #d32f2f;
}

/* 侧边栏样式，固定在左侧，宽度200px */
.sidebar {
  width: 200px;
  background-color: #f5f5f5;
  height: calc(100vh - 64px);
  position: fixed;
  left: 0;
  top: 64px;
}

/* 导航菜单样式 */
.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* 导航菜单项样式 */
.nav-item {
  padding: 0;
}

/* 导航链接样式，显示为块级元素 */
.nav-link {
  display: block;
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  border-bottom: 1px solid #e0e0e0;
}

/* 导航链接悬停和活动状态样式 */
.nav-link:hover,
.nav-link.active {
  background-color: #e0e0e0;
}

/* 主内容区域样式，设置左侧边距以避开侧边栏 */
.main-content {
  margin-left: 200px;
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

/* 教师管理区域头部样式，实现两端对齐 */
.teacher-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* 教师管理区域标题样式 */
.teacher-header h2 {
  margin: 0;
  color: #333;
}

/* 添加教师按钮样式 */
.add-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 添加教师按钮悬停样式 */
.add-btn:hover {
  background-color: #45a049;
}

/* 添加教师表单样式，白色背景，带阴影 */
.add-teacher-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

/* 添加教师表单标题样式 */
.add-teacher-form h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 15px;
}

/* 表单行样式，使用网格布局 */
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

/* 表单组样式，使用flex布局 */
.form-group {
  display: flex;
  flex-direction: column;
}

/* 表单标签样式 */
.form-group label {
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

/* 表单输入框和选择框样式 */
.form-group input,
.form-group select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

/* 提交按钮样式 */
.submit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 提交按钮悬停样式（非禁用状态） */
.submit-btn:hover:not(:disabled) {
  background-color: #45a049;
}

/* 提交按钮禁用状态样式 */
.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 教师列表容器样式 */
.teacher-list {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 教师列表标题样式 */
.teacher-list h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 15px;
}

/* 搜索容器样式 */
  .search-container {
    margin-bottom: 15px;
  }

  /* 搜索输入框包装器，使用flex布局使输入框和按钮并排显示 */
  .search-input-wrapper {
    display: flex;
    align-items: center;
    gap: 0;
  }

  /* 搜索输入框样式，设置合适的宽度比例 */
  .search-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-right: none;
    border-radius: 4px 0 0 4px;
    font-size: 14px;
    box-sizing: border-box;
  }

  /* 搜索按钮样式，与输入框保持视觉对齐 */
  .search-btn {
    background-color: #2196F3;
    color: white;
    border: 1px solid #2196F3;
    padding: 10px 20px;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    font-size: 14px;
    white-space: nowrap;
    height: 100%;
  }

  /* 搜索按钮悬停样式 */
  .search-btn:hover {
    background-color: #0b7dda;
    border-color: #0b7dda;
  }

/* 教师表格样式 */
.teacher-table {
  width: 100%;
  border-collapse: collapse;
}

/* 教师表格表头和单元格样式 */
.teacher-table th,
.teacher-table td {
  padding: 12px;
  text-align: left;
  color: #000;
  border-bottom: 1px solid #e0e0e0;
}

/* 教师表格表头样式 */
.teacher-table th {
  background-color: #f5f5f5;
  font-weight: 500;
  color: #333;
}

/* 编辑按钮样式 */
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

/* 编辑按钮悬停样式 */
.edit-btn:hover {
  background-color: #0b7dda;
}

/* 删除按钮样式 */
.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

/* 删除按钮悬停样式 */
.delete-btn:hover {
  background-color: #d32f2f;
}

/* 无数据提示样式 */
.no-data {
  text-align: center;
  padding: 20px;
  color: #999;
}

/* 模态框遮罩层样式，固定定位，半透明背景 */
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

/* 模态框内容样式，白色背景，固定最大宽度 */
.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 600px;
}

/* 模态框标题样式 */
.modal-content h3 {
  margin-top: 0;
  color: #333;
  margin-bottom: 20px;
}

/* 模态框按钮组样式 */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

/* 取消按钮样式 */
.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 取消按钮悬停样式 */
.cancel-btn:hover {
  background-color: #e0e0e0;
}

/* 错误提示信息样式，红色背景 */
.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px 15px;
  border-radius: 4px;
  margin-top: 15px;
}
</style>