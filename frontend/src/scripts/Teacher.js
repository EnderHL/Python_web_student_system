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
