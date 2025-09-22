import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/axios.js'

export default {
  name: 'Schedule',
  setup() {
    const router = useRouter()

    // 用户信息
    const user = ref(JSON.parse(localStorage.getItem('user')) || null)

    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        if (!user.value) {
          const response = await api.get('/user/me/')
          user.value = response.data
          localStorage.setItem('user', JSON.stringify(response.data))
        }
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    }

    // 根据课程ID获取课程名称
    const getCourseName = (course) => {
      if (!course) return '无'
      // 如果course是对象，直接返回name属性
      if (typeof course === 'object') {
        return course.name || '未知课程'
      }
      // 如果是数组，返回第一个课程的名称
      if (Array.isArray(course)) {
        return course.length > 0 ? course[0].name || '未知课程' : '无'
      }
      // 如果是字符串，直接返回
      return course
    }

    // 排课列表数据
    const schedules = ref([])
    const loading = ref(false)
    
    // 筛选条件
    const searchQuery = ref('')
    const dayFilter = ref('')
    const courseFilter = ref('')
    const classroomFilter = ref('')
    const teacherFilter = ref('')
    
    // 分页相关
    const currentPage = ref(1)
    const totalPages = ref(1)
    const pageSize = ref(12)
    const totalSchedules = ref(0)

    // 添加排课表单
    const showAddForm = ref(false)
    const scheduleForm = ref({
      day: '',
      time_slot: '',
      course: '',
      classroom: '',
      teacher: '',
      description: ''
    })

    // 课程、教室、教师数据
    const courses = ref([])
    const classrooms = ref([])
    const teachers = ref([])

    // 弹窗控制
    const showDetailDialog = ref(false)
    const selectedSchedule = ref(null)
    const showEditDialog = ref(false)
    const editForm = ref({})

    // 退出登录
    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }

    // 获取课程列表
    const fetchCourses = async () => {
      try {
        const response = await api.get('courses/')
        courses.value = response.data.results
      } catch (error) {
        console.error('获取课程列表失败:', error)
      }
    }

    // 获取教室列表
    const fetchClassrooms = async () => {
      try {
        const response = await api.get('classrooms/')
        classrooms.value = response.data.results
      } catch (error) {
        console.error('获取教室列表失败:', error)
      }
    }

    // 获取教师列表
    const fetchTeachers = async () => {
      try {
        const response = await api.get('/teachers/')
        teachers.value = response.data.results
      } catch (error) {
        console.error('获取教师列表失败:', error)
      }
    }

    // 获取排课列表
    const fetchSchedules = async () => {
      loading.value = true
      try {
        let url = `/schedules/?page=${currentPage.value}&page_size=${pageSize.value}`

        // 添加搜索条件
        if (searchQuery.value) {
          url += `&search=${encodeURIComponent(searchQuery.value)}`
        }

        // 添加筛选条件
        if (dayFilter.value) {
          url += `&day=${dayFilter.value}`
        }

        if (courseFilter.value) {
          url += `&course=${courseFilter.value}`
        }

        if (classroomFilter.value) {
          url += `&classroom=${classroomFilter.value}`
        }

        if (teacherFilter.value) {
          url += `&teacher=${teacherFilter.value}`
        }

        const response = await api.get(url)
        schedules.value = response.data.results
        totalSchedules.value = response.data.count
        totalPages.value = Math.ceil(response.data.count / pageSize.value)
      } catch (error) {
        console.error('获取排课列表失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 添加排课
    const addSchedule = async () => {
      loading.value = true
      try {
        await api.post('/schedules/', scheduleForm.value)
        showAddForm.value = false
        fetchSchedules()
        alert('排课添加成功！')
      } catch (error) {
        console.error('添加排课失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 查看排课详情
    const viewScheduleDetails = (schedule) => {
      selectedSchedule.value = { ...schedule }
      showDetailDialog.value = true
    }

    // 编辑排课
    const editSchedule = (schedule) => {
      editForm.value = { ...schedule }
      showEditDialog.value = true
    }

    // 更新排课
    const updateSchedule = async () => {
      loading.value = true
      try {
        await api.put(`/api/schedules/${editForm.value.id}/`, editForm.value)
        showEditDialog.value = false
        fetchSchedules()
        alert('排课更新成功！')
      } catch (error) {
        console.error('更新排课失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 删除排课
    const deleteSchedule = async (id) => {
      if (confirm('确定要删除这个排课吗？')) {
        loading.value = true
        try {
          await api.delete(`/api/schedules/${id}/`)
          fetchSchedules()
          alert('排课删除成功！')
        } catch (error) {
          console.error('删除排课失败:', error)
        } finally {
          loading.value = false
        }
      }
    }

    // 处理搜索
    const handleSearch = () => {
      currentPage.value = 1
      fetchSchedules()
    }

    // 分页
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchSchedules()
      }
    }

    // 清空筛选条件
    const clearFilters = () => {
      searchQuery.value = ''
      dayFilter.value = ''
      courseFilter.value = ''
      classroomFilter.value = ''
      teacherFilter.value = ''
      currentPage.value = 1
      fetchSchedules()
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

    // 获取教室名称
    const getClassName = (classroomId) => {
      const classroom = classrooms.value.find(c => c.id === classroomId)
      return classroom ? classroom.name : '未知教室'
    }

    // 获取星期文本
    const getDayOfWeekText = (day) => {
      const days = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']
      return days[day] || '未知'
    }

    // 获取排课模式文本
    const getWeekPatternText = (pattern) => {
      const patterns = {
        all: '每周',
        odd: '单周',
        even: '双周'
      }
      return patterns[pattern] || '未知'
    }

    // 处理筛选条件变化
    const handleFilterChange = () => {
      currentPage.value = 1
      fetchSchedules()
    }

    // 计算统计数据
    const weeklySchedulesCount = computed(() => {
      return schedules.value.filter(s => s.week_pattern === 'all').length
    })
    const oddWeekSchedulesCount = computed(() => {
      return schedules.value.filter(s => s.week_pattern === 'odd').length
    })
    const evenWeekSchedulesCount = computed(() => {
      return schedules.value.filter(s => s.week_pattern === 'even').length
    })

    // 课程节次
    const courseSections = [1, 2, 3, 4, 5, 6, 7, 8]

    // 根据起始节次获取可选的结束节次
    const getAvailableEndSections = (startSection) => {
      if (!startSection) return []
      return courseSections.filter(section => section >= startSection)
    }

    // 教学任务相关
    const teachingAssignments = ref([])
    const editTeachingAssignments = ref([])

    // 获取教学任务
    const fetchTeachingAssignments = async () => {
      try {
        const response = await api.get('/teaching_assignments/')
        teachingAssignments.value = response.data.results
      } catch (error) {
        console.error('获取教学任务失败:', error)
      }
    }

    // 课程变化处理
    const onCourseChange = (event) => {
      const courseId = event.target.value
      editTeachingAssignments.value = teachingAssignments.value.filter(ta => ta.course_id === courseId)
    }

    // 编辑课程变化处理
    const onEditCourseChange = (event) => {
      const courseId = event.target.value
      editTeachingAssignments.value = teachingAssignments.value.filter(ta => ta.course_id === courseId)
    }

    // 起始节次变化处理
    const onStartSectionChange = (event) => {
      const startSection = event.target.value
      if (editForm.value && editForm.value.start_section && editForm.value.end_section < startSection) {
        editForm.value.end_section = startSection
      }
    }

    // 编辑起始节次变化处理
    const onEditStartSectionChange = (event) => {
      const startSection = event.target.value
      if (editForm.value.end_section && editForm.value.end_section < startSection) {
        editForm.value.end_section = startSection
      }
    }

    // 页面挂载时加载数据
    onMounted(async () => {
      await loadUserInfo()
      await Promise.all([
        fetchSchedules(),
        fetchCourses(),
        fetchClassrooms(),
        fetchTeachers(),
        fetchTeachingAssignments()
      ])
    })

    return {
      user,
      schedules,
      loading,
      searchQuery,
      dayFilter,
      courseFilter,
      classroomFilter,
      teacherFilter,
      currentPage,
      totalPages,
      pageSize,
      totalSchedules,
      showAddForm,
      scheduleForm,
      courses,
      classrooms,
      teachers,
      showDetailDialog,
      selectedSchedule,
      showEditDialog,
      editForm,
      loadUserInfo,
      getCourseName,
      getClassName,
      getDayOfWeekText,
      getWeekPatternText,
      formatDate,
      fetchSchedules,
      addSchedule,
      editSchedule,
      deleteSchedule,
      viewScheduleDetails,
      handleLogout,
      handleSearch,
      goToPage,
      clearFilters,
      handleFilterChange,
      weeklySchedulesCount,
      oddWeekSchedulesCount,
      evenWeekSchedulesCount,
      courseSections,
      getAvailableEndSections,
      teachingAssignments,
      editTeachingAssignments,
      onCourseChange,
      onEditCourseChange,
      onStartSectionChange,
      onEditStartSectionChange,
      updateSchedule,
      fetchCourses,
      fetchClassrooms,
      fetchTeachers,
      fetchTeachingAssignments
    }
  }
}