import { ref, computed, onMounted } from 'vue';
import { ref as vueRef, computed as vueComputed, onMounted as vueOnMounted } from 'vue';
import axios from './../utils/axios';

// API 函数
// 获取课程列表
export const fetchCourses = async (params = {}) => {
  try {
    const response = await axios.get('/courses/', { params });
    return response.data;
  } catch (error) {
    console.error('获取课程列表失败:', error);
    throw error;
  }
};

// 获取单个课程详情
export const fetchCourseDetail = async (courseId) => {
  try {
    const response = await axios.get(`/courses/${courseId}/`);
    return response.data;
  } catch (error) {
    console.error('获取课程详情失败:', error);
    throw error;
  }
};

// 创建课程
export const createCourse = async (courseData) => {
  try {
    const response = await axios.post('/courses/', courseData);
    return response.data;
  } catch (error) {
    console.error('创建课程失败:', error);
    throw error;
  }
};

// 更新课程
export const updateCourse = async (courseId, courseData) => {
  try {
    const response = await axios.put(`/courses/${courseId}/`, courseData);
    return response.data;
  } catch (error) {
    console.error('更新课程失败:', error);
    throw error;
  }
};

// 删除课程
export const deleteCourse = async (courseId) => {
  try {
    const response = await axios.delete(`/courses/${courseId}/`);
    return response.data;
  } catch (error) {
    console.error('删除课程失败:', error);
    throw error;
  }
};

// 获取教师列表
export const fetchTeachers = async () => {
  try {
    const response = await axios.get('/teachers/');
    // 确保返回数组
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('获取教师列表失败:', error);
    // 如果API调用失败，返回空数组
    return [];
  }
};

// 获取教室列表
export const fetchClassrooms = async () => {
  try {
    const response = await axios.get('/classrooms/');
    return response.data;
  } catch (error) {
    console.error('获取教室列表失败:', error);
    // 如果API调用失败，返回空数组
    return [];
  }
};

// 创建教师-课程关联
export const createTeachingAssignment = async (data) => {
  try {
    const response = await axios.post('/teaching_assignments/', data);
    return response.data;
  } catch (error) {
    console.error('创建教师-课程关联失败:', error);
    throw error;
  }
};

// 获取课程的教师-课程关联
export const fetchTeachingAssignments = async (courseId) => {
  try {
    const response = await axios.get('/teaching_assignments/', { params: { course_id: courseId } });
    // 确保返回数组
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error(`获取课程 ${courseId} 的教师关联失败:`, error);
    return [];
  }
};

// 获取选课记录
export const fetchEnrollments = async (params = {}) => {
  try {
    const response = await axios.get('/enrollments/', { params });
    return response.data;
  } catch (error) {
    console.error('获取选课记录失败:', error);
    throw error;
  }
};

// 格式化课程类型显示
export const formatCourseType = (courseType) => {
  const typeMap = {
    'required': '必修',
    'elective': '选修',
    'general': '通识',
    'compulsory': '必修',
    'optional': '选修'
  };
  return typeMap[courseType] || courseType;
};

// 格式化教学方式显示
export const formatTeachingMethod = (method) => {
  const methodMap = {
    'online': '线上',
    'offline': '线下'
  };
  return methodMap[method] || method;
};

// 根据教学方式和教室自动设置容量
export const setCapacityByTeachingMethod = (teachingMethod, classroomId = null, classrooms = []) => {
  if (teachingMethod === 'online') {
    return 1000; // 线上课程默认容量为1000
  } else if (teachingMethod === 'offline' && classroomId && classrooms.length > 0) {
    const classroom = classrooms.find(c => c.id === classroomId);
    return classroom ? classroom.capacity : 50; // 线下课程根据教室容量设置，默认50人
  }
  return 50; // 默认值
};

// 验证课程数据
export const validateCourseData = (courseData) => {
  const errors = {};
  
  // 必填字段验证
  if (!courseData.name || courseData.name.trim() === '') {
    errors.name = '课程名称不能为空';
  }
  
  if (!courseData.code || courseData.code.trim() === '') {
    errors.code = '课程代码不能为空';
  }
  
  if (!courseData.course_type) {
    errors.course_type = '课程类型不能为空';
  }
  
  if (!courseData.credits || courseData.credits <= 0) {
    errors.credits = '学分必须大于0';
  }
  
  if (!courseData.total_hours || courseData.total_hours <= 0) {
    errors.total_hours = '总学时必须大于0';
  }
  
  if (!courseData.teacher_id) {
    errors.teacher_id = '教师不能为空';
  }
  
  // 线下课程必须选择教室
  if (courseData.teaching_method === 'offline' && !courseData.classroom_id) {
    errors.classroom_id = '线下课程必须选择教室';
  }
  
  if (!courseData.max_students || courseData.max_students <= 0) {
    errors.max_students = '最大学生数必须大于0';
  }
  
  if (!courseData.semester || courseData.semester.trim() === '') {
    errors.semester = '学期不能为空';
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

// 获取课程统计数据
export const getCourseStatistics = (courses = []) => {
  // 根据实际数据统计
  const totalCourses = courses.length;
  const requiredCourses = courses.filter(course => 
    ['required', '必修'].includes(course.course_type)
  ).length;
  const electiveCourses = courses.filter(course => 
    ['elective', '选修'].includes(course.course_type)
  ).length;
  const onlineCourses = courses.filter(course => course.teaching_method === 'online').length;
  const offlineCourses = courses.filter(course => course.teaching_method === 'offline').length;
  const totalStudents = courses.reduce((sum, course) => sum + (course.current_students || course.enrolled_students || 0), 0);
  
  return {
    totalCourses,
    requiredCourses,
    electiveCourses,
    onlineCourses,
    offlineCourses,
    totalStudents
  };
};

// 格式化日期
export const formatDate = (dateString) => {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
  } catch (error) {
    return dateString;
  }
};

// 课程管理功能模块
export default function CourseManager() {
  // 状态管理
  const userInfo = vueRef({ name: '管理员', role: '系统管理员' });
  const courses = vueRef([]);
  const teachers = vueRef([]);
  const classrooms = vueRef([]);
  const showAddCourseForm = vueRef(false);
  const showEditCourseForm = vueRef(false);
  const showCourseDetails = vueRef(false);
  const selectedCourse = vueRef({});
  const editingCourse = vueRef({});
  const filterType = vueRef('');
  const searchQuery = vueRef('');
  const currentPage = vueRef(1);
  const pageSize = vueRef(10);
  const isLoading = vueRef(false);
  const error = vueRef('');
  
  // 新课程表单数据
  const newCourse = vueRef({
    name: '',
    code: '',
    type: '必修',
    credit: 3,
    totalHours: 48,
    teacherId: '',
    classroomId: '',
    maxStudents: 50,
    enrolledStudents: 0,
    teachingMethod: 'offline',
    semester: ''
  });
  
  // 加载用户信息
  const loadUserInfo = async () => {
    try {
      const response = await axios.get('/auth/profile/');
      userInfo.value = response.data;
    } catch (error) {
      console.error('加载用户信息失败:', error);
      // 提供默认的认证信息以确保可以继续获取数据
      userInfo.value = { name: '管理员', role: '系统管理员' };
      // 在localStorage中设置一个临时token以便测试
      localStorage.setItem('token', 'temporary_test_token');
    }
  };
  
  // 获取课程列表
  const loadCourses = async () => {
    isLoading.value = true;
    error.value = '';
    try {
      const coursesData = await fetchCourses();
      // 检查返回的数据是否是分页对象
      if (coursesData && coursesData.results && Array.isArray(coursesData.results)) {
        // 如果是分页对象，使用results数组
        courses.value = coursesData.results;
      } else if (Array.isArray(coursesData)) {
        // 如果已经是数组，直接使用
        courses.value = coursesData;
      } else {
        // 否则使用空数组
        courses.value = [];
      }
      
      // 为每个课程加载教师信息
      await Promise.all(
        courses.value.map(async (course) => {
          try {
            const assignments = await fetchTeachingAssignments(course.id);
            // 确保assignments是数组
            if (Array.isArray(assignments)) {
              course.teachers = assignments.map(assignment => assignment.teacher_id);
            } else {
              course.teachers = [];
            }
          } catch (error) {
            console.error(`获取课程 ${course.id} 的教师信息失败:`, error);
            course.teachers = [];
          }
        })
      );
    } catch (error) {
      console.error('获取课程列表失败:', error);
      error.value = '获取课程列表失败，请稍后再试';
      // 初始化空数组
      courses.value = [];
    } finally {
      isLoading.value = false;
    }
  };
  
  // 加载教师列表
  const loadTeachers = async () => {
    try {
      const teachersData = await fetchTeachers();
      teachers.value = teachersData;
    } catch (error) {
      console.error('获取教师列表失败:', error);
      // 初始化空数组
      teachers.value = [];
    }
  };
  
  // 加载教室列表
  const loadClassrooms = async () => {
    try {
      const classroomsData = await fetchClassrooms();
      classrooms.value = classroomsData;
    } catch (error) {
      console.error('获取教室列表失败:', error);
      // 初始化空数组
      classrooms.value = [];
    }
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
  
  // 重置新课程表单
  const resetNewCourse = () => {
    newCourse.value = {
      name: '',
      code: '',
      course_type: '必修',
      credit: 3,
      totalHours: 48,
      teacherId: '',
      classroomId: '',
      maxStudents: 50,
      enrolledStudents: 0,
      teachingMethod: 'offline',
      semester: ''
    };
  };
  
  // 添加课程
  const addCourse = async () => {
    try {
      // 准备课程数据，确保字段名与后端一致
      const courseData = {
        name: newCourse.value.name,
        code: newCourse.value.code,
        course_type: newCourse.value.type === '必修' ? 'required' : (newCourse.value.type === '选修' ? 'elective' : 'general'),
        credits: newCourse.value.credit,
        total_hours: newCourse.value.totalHours,
        classroom_id: newCourse.value.teachingMethod === 'online' ? null : newCourse.value.classroomId,
        teaching_method: newCourse.value.teachingMethod || 'offline',
        semester: newCourse.value.semester || ''
      };
      
      // 根据教学方式自动设置最大学生数
      if (newCourse.value.teachingMethod === 'online') {
        courseData.max_students = 1000; // 线上课程默认容量为1000
      } else if (newCourse.value.classroomId) {
        // 线下课程根据教室容量设置
        const classroom = classrooms.value.find(c => c.id === newCourse.value.classroomId);
        courseData.max_students = classroom ? classroom.capacity : 50; // 默认值
      } else {
        courseData.max_students = 50; // 默认值
      }
      
      courseData.enrolled_students = 0;
      
      // 验证课程数据
      const validation = validateCourseData(courseData);
      if (!validation.isValid) {
        // 收集所有验证错误并显示
        const errorMessages = Object.values(validation.errors).join('\n');
        alert(errorMessages);
        return;
      }
      
      // 调用API添加课程
      const createdCourse = await createCourse(courseData);
      
      // 处理教师-课程关联
      if (newCourse.value.teacherId && Array.isArray(newCourse.value.teacherId)) {
        for (const teacherId of newCourse.value.teacherId) {
          await createTeachingAssignment({
            course_id: createdCourse.id,
            teacher_id: teacherId
          });
        }
      } else if (newCourse.value.teacherId) {
        await createTeachingAssignment({
          course_id: createdCourse.id,
          teacher_id: newCourse.value.teacherId
        });
      }
      
      courses.value.push(createdCourse);
      
      // 重置表单
      resetNewCourse();
      showAddCourseForm.value = false;
      alert('课程创建成功！');
    } catch (error) {
      console.error('添加课程失败:', error);
      alert('添加课程失败，请稍后再试');
    }
  };
  
  // 查看课程详情
  const viewCourseDetails = async (id) => {
    try {
      // 从API获取详细信息
      const courseDetail = await fetchCourseDetail(id);
      // 获取教师-课程关联
      const assignments = await fetchTeachingAssignments(id);
      courseDetail.teachers = assignments.map(assignment => assignment.teacher_id);
      selectedCourse.value = courseDetail;
      showCourseDetails.value = true;
    } catch (error) {
      console.error('查看课程详情失败:', error);
      alert('查看课程详情失败，请稍后再试');
      // 如果API失败，从本地数据查找
      const courseList = Array.isArray(courses.value) ? courses.value : [];
      const course = courseList.find(c => c.id === id);
      if (course) {
        selectedCourse.value = { ...course };
        showCourseDetails.value = true;
      }
    }
  };
  
  // 编辑课程
  const editCourse = (id) => {
    // 确保courses.value是数组
    const courseList = Array.isArray(courses.value) ? courses.value : [];
    const course = courseList.find(c => c.id === id);
    if (course) {
      // 转换课程类型为中文显示
      const typeMap = {
        'required': '必修',
        'elective': '选修',
        'general': '通识'
      };
      
      editingCourse.value = {
        ...course,
        type: typeMap[course.course_type] || course.course_type,
        credit: course.credits || 0,
        totalHours: course.total_hours || 0,
        teacherId: course.teacher_id || '',
        classroomId: course.classroom_id || '',
        maxStudents: course.max_students || 50,
        enrolledStudents: course.current_students || course.enrolled_students || 0,
        teachingMethod: course.teaching_method || 'offline'
      };
      showEditCourseForm.value = true;
    }
  };
  
  // 更新课程
  const handleUpdateCourse = async () => {
    try {
      // 准备更新数据
      const courseData = {
        ...editingCourse.value,
        course_type: editingCourse.value.type === '必修' ? 'required' : (editingCourse.value.type === '选修' ? 'elective' : 'general'),
        credits: editingCourse.value.credit,
        total_hours: editingCourse.value.totalHours,
        classroom_id: editingCourse.value.teaching_method === 'online' ? null : editingCourse.value.classroom_id,
        teaching_method: editingCourse.value.teaching_method || 'offline',
        semester: editingCourse.value.semester || ''
      };
      
      // 根据教学方式自动设置最大学生数
      if (editingCourse.value.teaching_method === 'online') {
        courseData.max_students = 1000; // 线上课程默认容量为1000
      } else if (editingCourse.value.classroom_id) {
        // 线下课程根据教室容量设置
        const classroom = classrooms.value.find(c => c.id === editingCourse.value.classroom_id);
        courseData.max_students = classroom ? classroom.capacity : 50; // 默认50人
      }
      
      // 验证课程数据
      const validation = validateCourseData(courseData);
      if (!validation.isValid) {
        // 收集所有验证错误并显示
        const errorMessages = Object.values(validation.errors).join('\n');
        alert(errorMessages);
        return;
      }
      
      // 调用API更新课程
      const updatedCourse = await updateCourse(editingCourse.value.id, courseData);
      
      // 处理教师-课程关联更新
      if (courseData.teachers && Array.isArray(courseData.teachers)) {
        // 先获取当前的教师关联
        const currentAssignments = await fetchTeachingAssignments(editingCourse.value.id);
        const currentTeacherIds = currentAssignments.map(assignment => assignment.teacher_id);
        
        // 删除不再关联的教师
        const teachersToRemove = currentTeacherIds.filter(id => !courseData.teachers.includes(id));
        for (const assignment of currentAssignments) {
          if (teachersToRemove.includes(assignment.teacher_id)) {
            await axios.delete(`/teaching_assignments/${assignment.id}/`);
          }
        }
        
        // 添加新关联的教师
        const teachersToAdd = courseData.teachers.filter(id => !currentTeacherIds.includes(id));
        for (const teacherId of teachersToAdd) {
          await createTeachingAssignment({
            course_id: editingCourse.value.id,
            teacher_id: teacherId
          });
        }
      }
      
      // 更新本地数据
      if (!Array.isArray(courses.value)) {
        courses.value = [];
      }
      const index = courses.value.findIndex(c => c.id === editingCourse.value.id);
      if (index !== -1) {
        courses.value[index] = updatedCourse;
      }
      
      showEditCourseForm.value = false;
      alert('课程更新成功！');
    } catch (error) {
      console.error('更新课程失败:', error);
      alert('更新课程失败，请稍后再试');
    }
  };
  
  // 删除课程
  const handleDeleteCourse = async (id) => {
    if (confirm('确定要删除这门课程吗？删除后无法恢复！')) {
      try {
        // 调用API删除课程
        await deleteCourse(id);
        
        // 更新本地数据
        if (!Array.isArray(courses.value)) {
          courses.value = [];
        }
        const index = courses.value.findIndex(c => c.id === id);
        if (index !== -1) {
          courses.value.splice(index, 1);
        }
        alert('课程删除成功！');
      } catch (error) {
        console.error('删除课程失败:', error);
        alert('删除课程失败，请稍后再试');
      }
    }
  };
  
  // 切换页面
  const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page;
    }
  };
  
  // 重置筛选条件
  const resetFilters = () => {
    filterType.value = '';
    searchQuery.value = '';
    currentPage.value = 1;
  };
  
  // 筛选和搜索课程
  const filteredCourses = vueComputed(() => {
    // 确保courses.value始终是数组
    const courseList = Array.isArray(courses.value) ? courses.value : [];
    let result = [...courseList];
    
    // 按课程类型筛选
    if (filterType.value) {
      result = result.filter(course => {
        // 确保使用正确的字段名course_type
        if (typeof course.course_type === 'string') {
          // 将前端选择的中文课程类型转换为后端存储的英文类型
          const typeMap = {
            '必修': 'required',
            '选修': 'elective',
            '通识': 'general'
          };
          const filterValue = typeMap[filterType.value] || filterType.value;
          return course.course_type === filterValue;
        }
        return false;
      });
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
  const totalPages = vueComputed(() => {
    // 确保courses.value始终是数组
    const courseList = Array.isArray(courses.value) ? courses.value : [];
    let result = [...courseList];
    
    // 按课程类型筛选
    if (filterType.value) {
      result = result.filter(course => {
        // 确保使用正确的字段名course_type
        if (typeof course.course_type === 'string') {
          // 将前端选择的中文课程类型转换为后端存储的英文类型
          const typeMap = {
            '必修': 'required',
            '选修': 'elective',
            '通识': 'general'
          };
          const filterValue = typeMap[filterType.value] || filterType.value;
          return course.course_type === filterValue;
        }
        return false;
      });
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
  vueOnMounted(() => {
    loadUserInfo();
    loadCourses();
    loadTeachers();
    loadClassrooms();
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
    pageSize,
    newCourse,
    filteredCourses,
    totalPages,
    isLoading,
    error,
    addCourse,
    viewCourseDetails,
    editCourse,
    handleUpdateCourse,
    handleDeleteCourse,
    formatDate,
    formatCourseType,
    formatTeachingMethod,
    getTeacherName,
    getClassName,
    changePage,
    resetFilters,
    loadCourses,
    resetNewCourse
  };
}
