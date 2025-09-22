import { ref, computed, onMounted } from 'vue';
import axios from './../utils/axios';

// 模拟数据
const MOCK_COURSES = [
  { id: 1, name: '高等数学', code: 'MATH101', type: '必修', credit: 4, totalHours: 64, teacherId: 1, classroomId: 1, maxStudents: 100, enrolledStudents: 85, createdAt: '2023-09-01T08:00:00' },
  { id: 2, name: '大学物理', code: 'PHYS101', type: '必修', credit: 3, totalHours: 48, teacherId: 2, classroomId: 2, maxStudents: 80, enrolledStudents: 72, createdAt: '2023-09-01T09:00:00' },
  { id: 3, name: '程序设计基础', code: 'CS101', type: '必修', credit: 4, totalHours: 64, teacherId: 3, classroomId: 3, maxStudents: 60, enrolledStudents: 58, createdAt: '2023-09-01T10:00:00' },
  { id: 4, name: '数据结构', code: 'CS201', type: '必修', credit: 4, totalHours: 64, teacherId: 3, classroomId: 4, maxStudents: 60, enrolledStudents: 56, createdAt: '2023-09-01T14:00:00' },
  { id: 5, name: '操作系统', code: 'CS202', type: '必修', credit: 4, totalHours: 64, teacherId: 4, classroomId: 5, maxStudents: 60, enrolledStudents: 54, createdAt: '2023-09-01T15:00:00' },
  { id: 6, name: '数据库原理', code: 'CS301', type: '必修', credit: 4, totalHours: 64, teacherId: 5, classroomId: 6, maxStudents: 60, enrolledStudents: 52, createdAt: '2023-09-01T16:00:00' },
  { id: 7, name: '人工智能导论', code: 'CS401', type: '选修', credit: 3, totalHours: 48, teacherId: 6, classroomId: 7, maxStudents: 50, enrolledStudents: 48, createdAt: '2023-09-02T08:00:00' },
  { id: 8, name: '云计算', code: 'CS402', type: '选修', credit: 3, totalHours: 48, teacherId: 7, classroomId: 8, maxStudents: 40, enrolledStudents: 38, createdAt: '2023-09-02T09:00:00' },
  { id: 9, name: '网络安全', code: 'CS403', type: '选修', credit: 3, totalHours: 48, teacherId: 8, classroomId: 9, maxStudents: 40, enrolledStudents: 36, createdAt: '2023-09-02T10:00:00' },
  { id: 10, name: 'Python数据分析', code: 'CS404', type: '选修', credit: 3, totalHours: 48, teacherId: 9, classroomId: 10, maxStudents: 40, enrolledStudents: 34, createdAt: '2023-09-02T14:00:00' },
  { id: 11, name: '机器学习', code: 'CS501', type: '选修', credit: 4, totalHours: 64, teacherId: 10, classroomId: 11, maxStudents: 30, enrolledStudents: 28, createdAt: '2023-09-02T15:00:00' },
  { id: 12, name: '深度学习', code: 'CS502', type: '选修', credit: 4, totalHours: 64, teacherId: 10, classroomId: 12, maxStudents: 30, enrolledStudents: 26, createdAt: '2023-09-02T16:00:00' }
];

const MOCK_TEACHERS = [
  { id: 1, name: '张三', department: '数学学院', title: '教授' },
  { id: 2, name: '李四', department: '物理学院', title: '副教授' },
  { id: 3, name: '王五', department: '计算机学院', title: '教授' },
  { id: 4, name: '赵六', department: '计算机学院', title: '副教授' },
  { id: 5, name: '孙七', department: '计算机学院', title: '教授' },
  { id: 6, name: '周八', department: '人工智能学院', title: '教授' },
  { id: 7, name: '吴九', department: '人工智能学院', title: '副教授' },
  { id: 8, name: '郑十', department: '网络空间安全学院', title: '教授' },
  { id: 9, name: '钱十一', department: '数据科学学院', title: '副教授' },
  { id: 10, name: '孙十二', department: '人工智能学院', title: '教授' }
];

const MOCK_CLASSROOMS = [
  { id: 1, name: 'A101', capacity: 100, location: 'A栋1楼' },
  { id: 2, name: 'A102', capacity: 80, location: 'A栋1楼' },
  { id: 3, name: 'B201', capacity: 60, location: 'B栋2楼' },
  { id: 4, name: 'B202', capacity: 60, location: 'B栋2楼' },
  { id: 5, name: 'B301', capacity: 60, location: 'B栋3楼' },
  { id: 6, name: 'B302', capacity: 60, location: 'B栋3楼' },
  { id: 7, name: 'C101', capacity: 50, location: 'C栋1楼' },
  { id: 8, name: 'C102', capacity: 40, location: 'C栋1楼' },
  { id: 9, name: 'C201', capacity: 40, location: 'C栋2楼' },
  { id: 10, name: 'C202', capacity: 40, location: 'C栋2楼' },
  { id: 11, name: 'D101', capacity: 30, location: 'D栋1楼' },
  { id: 12, name: 'D102', capacity: 30, location: 'D栋1楼' }
];

// 课程管理功能模块
export default function CourseManager() {
  // 状态管理
  const userInfo = ref({ name: '管理员', role: '系统管理员' });
  const courses = ref(MOCK_COURSES);
  const teachers = ref(MOCK_TEACHERS);
  const classrooms = ref(MOCK_CLASSROOMS);
  const showAddCourseForm = ref(false);
  const showEditCourseForm = ref(false);
  const showCourseDetails = ref(false);
  const selectedCourse = ref({});
  const editingCourse = ref({});
  const filterType = ref('');
  const searchQuery = ref('');
  const currentPage = ref(1);
  const pageSize = ref(10);
  
  // 新课程表单数据
  const newCourse = ref({
    name: '',
    code: '',
    type: '必修',
    credit: 0,
    totalHours: 0,
    teacherId: '',
    classroomId: '',
    maxStudents: 0,
    enrolledStudents: 0
  });
  
  // 加载用户信息
  const loadUserInfo = async () => {
    try {
      const response = await axios.get('/auth/profile/');
      userInfo.value = response.data;
    } catch (error) {
      console.error('加载用户信息失败:', error);
      // 使用模拟数据
    }
  };
  
  // 获取课程列表
  const fetchCourses = async () => {
    try {
      const response = await axios.get('/courses/');
      courses.value = response.data;
    } catch (error) {
      console.error('获取课程列表失败:', error);
      // 确保使用模拟数据
      courses.value = MOCK_COURSES;
    }
  };
  
  // 添加课程
  const addCourse = async () => {
    try {
      // 模拟添加课程
      const newId = Math.max(...courses.value.map(c => c.id)) + 1;
      const courseToAdd = {
        ...newCourse.value,
        id: newId,
        enrolledStudents: 0,
        createdAt: new Date().toISOString()
      };
      courses.value.push(courseToAdd);
      
      // 重置表单
      newCourse.value = {
        name: '',
        code: '',
        type: '必修',
        credit: 0,
        totalHours: 0,
        teacherId: '',
        classroomId: '',
        maxStudents: 0,
        enrolledStudents: 0
      };
      
      showAddCourseForm.value = false;
    } catch (error) {
      console.error('添加课程失败:', error);
    }
  };
  
  // 查看课程详情
  const viewCourseDetails = (id) => {
    const course = courses.value.find(c => c.id === id);
    if (course) {
      selectedCourse.value = { ...course };
      showCourseDetails.value = true;
    }
  };
  
  // 编辑课程
  const editCourse = (id) => {
    const course = courses.value.find(c => c.id === id);
    if (course) {
      editingCourse.value = { ...course };
      showEditCourseForm.value = true;
    }
  };
  
  // 更新课程
  const updateCourse = async () => {
    try {
      const index = courses.value.findIndex(c => c.id === editingCourse.value.id);
      if (index !== -1) {
        courses.value[index] = { ...editingCourse.value };
        showEditCourseForm.value = false;
      }
    } catch (error) {
      console.error('更新课程失败:', error);
    }
  };
  
  // 删除课程
  const deleteCourse = async (id) => {
    if (confirm('确定要删除这门课程吗？')) {
      try {
        const index = courses.value.findIndex(c => c.id === id);
        if (index !== -1) {
          courses.value.splice(index, 1);
        }
      } catch (error) {
        console.error('删除课程失败:', error);
      }
    }
  };
  
  // 格式化日期
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
  };
  
  // 根据教师ID获取教师名称
  const getTeacherName = (id) => {
    const teacher = teachers.value.find(t => t.id === id);
    return teacher ? teacher.name : '未知';
  };
  
  // 根据教室ID获取教室名称
  const getClassName = (id) => {
    const classroom = classrooms.value.find(c => c.id === id);
    return classroom ? classroom.name : '未知';
  };
  
  // 筛选和搜索课程
  const filteredCourses = computed(() => {
    // 确保courses.value始终是数组
    const courseList = Array.isArray(courses.value) ? courses.value : MOCK_COURSES;
    let result = [...courseList];
    
    // 按课程类型筛选
    if (filterType.value) {
      result = result.filter(course => course.type === filterType.value);
    }
    
    // 搜索
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      result = result.filter(
        course => course.name.toLowerCase().includes(query) || course.code.toLowerCase().includes(query)
      );
    }
    
    // 分页
    const startIndex = (currentPage.value - 1) * pageSize.value;
    result = result.slice(startIndex, startIndex + pageSize.value);
    
    return result;
  });
  
  // 计算总页数
  const totalPages = computed(() => {
    // 确保courses.value始终是数组
    const courseList = Array.isArray(courses.value) ? courses.value : MOCK_COURSES;
    let result = [...courseList];
    
    // 按课程类型筛选
    if (filterType.value) {
      result = result.filter(course => course.type === filterType.value);
    }
    
    // 搜索
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      result = result.filter(
        course => course.name.toLowerCase().includes(query) || course.code.toLowerCase().includes(query)
      );
    }
    
    return Math.ceil(result.length / pageSize.value);
  });
  
  // 组件挂载时加载数据
  onMounted(() => {
    loadUserInfo();
    fetchCourses();
  });
  
  // 返回所有需要的值和方法
  return {
    userInfo,
    courses,
    teachers,
    classrooms,
    showAddCourseForm,
    showEditCourseForm,
    showCourseDetails,
    selectedCourse,
    editingCourse,
    filterType,
    searchQuery,
    currentPage,
    newCourse,
    filteredCourses,
    totalPages,
    addCourse,
    viewCourseDetails,
    editCourse,
    updateCourse,
    deleteCourse,
    formatDate,
    getTeacherName,
    getClassName
  };
}
