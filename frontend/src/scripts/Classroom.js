import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/axios.js'

export default {
  name: 'Classroom',
  setup() {
    const router = useRouter()

    // 用户信息
    const user = ref(JSON.parse(localStorage.getItem('user')) || null)

    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        if (!user.value) {
          const response = await api.get('/api/user/me/')
          user.value = response.data
          localStorage.setItem('user', JSON.stringify(response.data))
        }
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    }

    // 根据教室容量获取CSS类名
    const getCapacityClass = (capacity) => {
      if (capacity < 30) return 'small-capacity'
      if (capacity < 60) return 'medium-capacity'
      if (capacity < 100) return 'large-capacity'
      return 'xlarge-capacity'
    }

    // 教室列表相关数据
    const classrooms = ref([])
    const totalClassrooms = ref(0)
    const averageCapacity = ref(0)
    const searchQuery = ref('')
    const capacityFilter = ref('')
    const equipmentFilter = ref('')
    const loading = ref(false)

    // 分页相关
    const currentPage = ref(1)
    const totalPages = ref(1)
    const pageSize = ref(12)

    // 添加教室表单
    const showAddForm = ref(false)
    const classroomForm = ref({
      name: '',
      location: '',
      capacity: '',
      equipment: [],
      equipmentText: '',
      description: ''
    })
    
    // 设备相关
    const newEquipment = ref('')
    const availableEquipment = ref(['投影仪', '电脑', '白板', '音响系统', '空调', '网络', '视频会议设备'])
    const allEquipment = ref(['投影仪', '电脑', '白板', '音响系统', '空调', '网络', '视频会议设备'])

    // 教室详情弹窗
    const showDetailDialog = ref(false)
    const selectedClassroom = ref(null)

    // 编辑教室弹窗
    const showEditDialog = ref(false)
    const editForm = ref({})
    const editNewEquipment = ref('')

    // 退出登录
    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }

    // 获取教室列表
    const fetchClassrooms = async () => {
      loading.value = true
      try {
        let url = `classrooms/?page=${currentPage.value}&page_size=${pageSize.value}`

        // 添加搜索条件
        if (searchQuery.value) {
          url += `&search=${encodeURIComponent(searchQuery.value)}`
        }

        // 添加容量筛选
        if (capacityFilter.value) {
          url += `&capacity_filter=${capacityFilter.value}`
        }

        // 添加设备筛选
        if (equipmentFilter.value) {
          url += `&equipment=${encodeURIComponent(equipmentFilter.value)}`
        }

        const response = await api.get(url)
        classrooms.value = response.data.results
        totalClassrooms.value = response.data.count
        totalPages.value = Math.ceil(response.data.count / pageSize.value)

        // 计算平均容量
        if (classrooms.value.length > 0) {
          const totalCapacity = classrooms.value.reduce((sum, classroom) => sum + classroom.capacity, 0)
          averageCapacity.value = Math.round((totalCapacity / classrooms.value.length) * 10) / 10
        } else {
          averageCapacity.value = 0
        }

        // 更新所有设备列表
        updateAllEquipmentList()
      } catch (error) {
        console.error('获取教室列表失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 更新所有设备列表（包括用户自定义的设备）
    const updateAllEquipmentList = () => {
      const allEquipmentSet = new Set(availableEquipment.value)
      
      classrooms.value.forEach(classroom => {
        if (classroom.equipment) {
          const equipmentList = parseEquipment(classroom.equipment)
          equipmentList.forEach(equipment => {
            allEquipmentSet.add(equipment)
          })
        }
      })
      
      allEquipment.value = Array.from(allEquipmentSet)
    }

    // 搜索教室
    const handleSearch = () => {
      currentPage.value = 1
      fetchClassrooms()
    }

    // 分页
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchClassrooms()
      }
    }

    // 添加教室
    const addClassroom = async () => {
      loading.value = true
      try {
        // 处理设备数据
        const formData = {
          ...classroomForm.value,
          equipment: classroomForm.value.equipment.join(',')
        }
        
        await api.post(`classrooms/`, formData)

        // 重置表单
        classroomForm.value = {
          name: '',
          location: '',
          capacity: '',
          equipment: [],
          equipmentText: '',
          description: ''
        }
        newEquipment.value = ''

        showAddForm.value = false
        fetchClassrooms()
        alert('教室添加成功！')
      } catch (error) {
        console.error('添加教室失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 查看教室详情
    const viewClassroomDetails = (classroom) => {
      selectedClassroom.value = { ...classroom }
      showDetailDialog.value = true
    }

    // 编辑教室
    const editClassroom = (classroom) => {
      // 解析设备数据
      const equipmentList = parseEquipment(classroom.equipment)
      
      // 设置编辑表单数据
      editForm.value = {
        ...classroom,
        equipment: equipmentList,
        equipmentText: classroom.equipment
      }
      editNewEquipment.value = ''
      showEditDialog.value = true
    }

    // 更新教室
    const updateClassroom = async () => {
      loading.value = true
      try {
        // 处理设备数据
        const formData = {
          ...editForm.value,
          equipment: editForm.value.equipment.join(',')
        }
        
        await api.put(`classrooms/${editForm.value.id}/`, formData)

        showEditDialog.value = false
        fetchClassrooms()
        alert('教室更新成功！')
      } catch (error) {
        console.error('更新教室失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 删除教室
    const deleteClassroom = async (id) => {
      if (confirm('确定要删除这个教室吗？')) {
        loading.value = true
        try {
          await api.delete(`classrooms/${id}/`)
          fetchClassrooms()
          alert('教室删除成功！')
        } catch (error) {
          console.error('删除教室失败:', error)
        } finally {
          loading.value = false
        }
      }
    }

    // 解析设备数据
    const parseEquipment = (equipmentStr) => {
      if (!equipmentStr) return []
      return equipmentStr.split(',').map(e => e.trim()).filter(e => e)
    }

    // 切换设备选择（添加表单）
    const toggleEquipment = (equipment) => {
      const index = classroomForm.value.equipment.indexOf(equipment)
      if (index > -1) {
        classroomForm.value.equipment.splice(index, 1)
      } else {
        classroomForm.value.equipment.push(equipment)
      }
      classroomForm.value.equipmentText = classroomForm.value.equipment.join(',')
    }

    // 添加新设备（添加表单）
    const addNewEquipment = () => {
      if (newEquipment.value.trim() && !classroomForm.value.equipment.includes(newEquipment.value.trim())) {
        const newEq = newEquipment.value.trim()
        classroomForm.value.equipment.push(newEq)
        classroomForm.value.equipmentText = classroomForm.value.equipment.join(',')
        
        // 添加到可用设备列表（如果不存在）
        if (!availableEquipment.value.includes(newEq)) {
          availableEquipment.value.push(newEq)
        }
        
        newEquipment.value = ''
      }
    }

    // 切换设备选择（编辑表单）
    const toggleEditEquipment = (equipment) => {
      const index = editForm.value.equipment.indexOf(equipment)
      if (index > -1) {
        editForm.value.equipment.splice(index, 1)
      } else {
        editForm.value.equipment.push(equipment)
      }
      editForm.value.equipmentText = editForm.value.equipment.join(',')
    }

    // 添加新设备（编辑表单）
    const addEditNewEquipment = () => {
      if (editNewEquipment.value.trim() && !editForm.value.equipment.includes(editNewEquipment.value.trim())) {
        const newEq = editNewEquipment.value.trim()
        editForm.value.equipment.push(newEq)
        editForm.value.equipmentText = editForm.value.equipment.join(',')
        
        // 添加到可用设备列表（如果不存在）
        if (!availableEquipment.value.includes(newEq)) {
          availableEquipment.value.push(newEq)
        }
        
        editNewEquipment.value = ''
      }
    }

    // 清空搜索条件
    const clearSearch = () => {
      searchQuery.value = ''
      capacityFilter.value = ''
      equipmentFilter.value = ''
      currentPage.value = 1
      fetchClassrooms()
    }

    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }

    // 获取容量标签样式
    const getCapacityBadgeClass = (capacity) => {
      if (capacity <= 30) return 'small-capacity'
      if (capacity <= 60) return 'medium-capacity'
      if (capacity <= 100) return 'large-capacity'
      return 'xlarge-capacity'
    }

    // 组件挂载时加载数据
    onMounted(() => {
      loadUserInfo()
      fetchClassrooms()
    })

    return {
      user,
      classrooms,
      totalClassrooms,
      averageCapacity,
      searchQuery,
      capacityFilter,
      equipmentFilter,
      loading,
      currentPage,
      totalPages,
      pageSize,
      showAddForm,
      classroomForm,
      newEquipment,
      availableEquipment,
      allEquipment,
      showDetailDialog,
      selectedClassroom,
      showEditDialog,
      editForm,
      editNewEquipment,
      handleLogout,
      fetchClassrooms,
      handleSearch,
      goToPage,
      addClassroom,
      viewClassroomDetails,
      editClassroom,
      updateClassroom,
      deleteClassroom,
      parseEquipment,
      toggleEquipment,
      addNewEquipment,
      toggleEditEquipment,
      addEditNewEquipment,
      clearSearch,
      formatDate,
      getCapacityBadgeClass
    }
  }
}
