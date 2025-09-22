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
