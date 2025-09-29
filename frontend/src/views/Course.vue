<template>
  <div class="course-container">
    <!-- 主内容区域 -->
    <main class="main-content">
        <!-- 课程管理标题和添加按钮 -->
        <div class="course-header">
          <h2>课程管理</h2>
          <el-button type="success" plain @click="showAddCourseForm = true">添加课程</el-button>
        </div>
        
        <!-- 添加课程表单 -->
        <AddCourseForm 
          v-if="showAddCourseForm"
          :teachers="teachers"
          :classrooms="classrooms"
          :newCourse="newCourse"
          @add-course="addCourse"
          @cancel="showAddCourseForm = false"
        />
        
        <!-- 筛选和搜索 -->
        <div class="filter-container">
          <div class="filter-row">
            <div class="filter-group">
              <label>课程类型</label>
              <select v-model="filterType">
                <option value="">全部类型</option>
                <option value="必修">必修</option>
                <option value="选修">选修</option>
                <option value="通识">通识</option>
              </select>
            </div>
            <div class="filter-group">
              <label>搜索</label>
              <input v-model="searchQuery" type="text" placeholder="搜索课程名称或代码" />
            </div>
          </div>
        </div>
        
        <!-- 课程列表 -->
        <div class="course-list">
          <table>
            <thead>
              <tr>
                <th>课程名称</th>
                <th>课程代码</th>
                <th>课程类型</th>
                <th>学分</th>
                <th>总课时</th>
                <th>教学方式</th>
                <th>学期</th>
                <th>教师</th>
                <th>已选人数/总人数</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in filteredCourses" :key="course.id">
                <td>{{ course.name }}</td>
                <td>{{ course.code }}</td>
                <td>
                  <span class="course-type-tag" :class="course.course_type">
                    {{ formatCourseType(course.course_type) }}
                  </span>
                </td>
                <td>{{ course.credits }}</td>
                <td>{{ course.total_hours }}</td>
                <td>{{ formatTeachingMethod(course.teaching_method) }}</td>
                <td>{{ course.semester || '暂无信息' }}</td>
                <td>
                  <span v-if="course.teachers && course.teachers.length > 0">
                    {{ course.teachers.map(teacherId => getTeacherName(teacherId)).join(', ') }}
                  </span>
                  <span v-else>未分配</span>
                </td>
                <td>{{ course.current_students || 0 }}/{{ course.max_students }}</td>
                <td>
                  <div class="button-row">
                    <el-button type="info" plain @click="viewCourseDetails(course.id)">查看</el-button>
                    <el-button type="primary" plain @click="editCourse(course.id)">编辑</el-button>
                    <el-button type="danger" plain @click="handleDeleteCourse(course.id)">删除</el-button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 分页 -->
        <div class="pagination">
          <el-button type="primary" plain :disabled="currentPage <= 1" @click="currentPage > 1 && (currentPage--)">上一页</el-button>
          <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
          <el-button type="primary" plain :disabled="currentPage >= totalPages" @click="currentPage < totalPages && (currentPage++)">下一页</el-button>
        </div>
        
        <!-- 课程详情弹窗 -->
        <CourseDetailDialog 
          v-if="showCourseDetails"
          :course="selectedCourse"
          :getTeacherName="getTeacherName"
          :getClassName="getClassName"
          :formatDate="formatDate"
          :formatCourseType="formatCourseType"
          :formatTeachingMethod="formatTeachingMethod"
          @close="showCourseDetails = false"
        />
        
        <!-- 编辑课程弹窗 -->
        <EditCourseDialog 
          v-if="showEditCourseForm"
          :course="editingCourse"
          :teachers="teachers"
          :classrooms="classrooms"
          @update-course="handleUpdateCourse"
          @cancel="showEditCourseForm = false"
        />
      </main>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import CourseManager from '../scripts/Course.js';
import { formatTeachingMethod, formatCourseType } from '../scripts/Course.js';

// 定义子组件
const AddCourseForm = defineComponent({
  name: 'AddCourseForm',
  props: {
    teachers: Array,
    classrooms: Array,
    newCourse: Object
  },
  emits: ['add-course', 'cancel'],
  template: `
    <div class="add-course-form">
      <h3>添加新课程</h3>
      <div class="form-row">
        <div class="form-group">
          <label>课程名称 <span class="required">*</span></label>
          <input v-model="newCourse.name" type="text" placeholder="请输入课程名称" required />
        </div>
        <div class="form-group">
          <label>课程代码 <span class="required">*</span></label>
          <input v-model="newCourse.code" type="text" placeholder="请输入课程代码" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>课程类型 <span class="required">*</span></label>
          <select v-model="newCourse.course_type">
            <option value="必修">必修</option>
            <option value="选修">选修</option>
            <option value="通识">通识</option>
          </select>
        </div>
        <div class="form-group">
          <label>学分 <span class="required">*</span></label>
          <input v-model.number="newCourse.credits" type="number" placeholder="请输入学分" min="0.5" max="6" step="0.5" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>总课时 <span class="required">*</span></label>
          <input v-model.number="newCourse.total_hours" type="number" placeholder="请输入总课时" min="16" max="128" step="8" required />
        </div>
        <div class="form-group">
          <label>教学方式 <span class="required">*</span></label>
          <select v-model="newCourse.teaching_method" @change="updateClassroomSelection">
            <option value="online">线上</option>
            <option value="offline">线下</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>学期 <span class="required">*</span></label>
          <input v-model="newCourse.semester" type="text" placeholder="请输入学期" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>教室 <span v-if="newCourse.teaching_method === 'offline'" class="required">*</span></label>
          <select v-model="newCourse.classroom_id" :disabled="newCourse.teaching_method === 'online'" :required="newCourse.teaching_method === 'offline'">
            <option value="">请选择教室</option>
            <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">{{ classroom.name }} (容量: {{ classroom.capacity }})</option>
          </select>
          <span v-if="newCourse.teaching_method === 'online'" class="online-course-note">线上课程无需选择教室，容量自动设置为1000人</span>
        </div>
      </div>
      <div class="form-actions">
          <el-button type="primary" plain @click="handleSubmit">提交</el-button>
          <el-button plain @click="$emit('cancel')">取消</el-button>
        </div>
    </div>
  `,
  methods: {
    updateClassroomSelection() {
      if (this.newCourse.teaching_method === 'online') {
        this.newCourse.classroom_id = null;
      }
    },
    handleSubmit() {
      // 进行基本的表单验证
      if (!this.newCourse.name || !this.newCourse.code || !this.newCourse.course_type || 
          this.newCourse.credits === null || this.newCourse.total_hours === null || 
          !this.newCourse.teaching_method || !this.newCourse.semester) {
        alert('请填写所有必填字段');
        return;
      }
      
      if (this.newCourse.teaching_method === 'offline' && !this.newCourse.classroom_id) {
        alert('线下课程必须选择教室');
        return;
      }
      
      // 学分和学时验证
      if (this.newCourse.credits < 0.5 || this.newCourse.credits > 6) {
        alert('学分必须在0.5到6之间');
        return;
      }
      
      if (this.newCourse.total_hours < 16 || this.newCourse.total_hours > 128 || this.newCourse.total_hours % 8 !== 0) {
        alert('总课时必须是8的倍数，且在16到128之间');
        return;
      }
      
      this.$emit('add-course');
    }
  }
});

const CourseDetailDialog = defineComponent({
  name: 'CourseDetailDialog',
  props: {
    course: Object,
    getTeacherName: Function,
    getClassName: Function,
    formatDate: Function,
    formatCourseType: Function,
    formatTeachingMethod: Function
  },
  emits: ['close'],
  template: `
    <div class="course-details-overlay">
      <div class="course-details-dialog">
        <h3>课程详情</h3>
        <div class="detail-content">
          <div class="detail-row">
            <div class="detail-label">课程名称：</div>
            <div class="detail-value">{{ course.name }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">课程代码：</div>
            <div class="detail-value">{{ course.code }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">课程类型：</div>
            <div class="detail-value">{{ formatCourseType(course.course_type) }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">学分：</div>
            <div class="detail-value">{{ course.credits }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">总课时：</div>
            <div class="detail-value">{{ course.total_hours }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">教学方式：</div>
            <div class="detail-value">{{ formatTeachingMethod(course.teaching_method) }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">学期：</div>
            <div class="detail-value">{{ course.semester }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">最大选课人数：</div>
            <div class="detail-value">{{ course.max_students }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">已选人数：</div>
            <div class="detail-value">{{ course.current_students || 0 }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">教室：</div>
            <div class="detail-value">{{ getClassName(course.classroom_id) || '线上课程' }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">创建时间：</div>
            <div class="detail-value">{{ formatDate(course.created_at) }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">状态：</div>
            <div class="detail-value">
              <span v-if="course.current_students >= course.max_students" class="status-full">已报满</span>
              <span v-else class="status-available">可报名</span>
            </div>
          </div>
        </div>
        <div class="dialog-actions">
          <el-button plain @click="$emit('close')">关闭</el-button>
        </div>
      </div>
    </div>
  `
});

const EditCourseDialog = defineComponent({
  name: 'EditCourseDialog',
  props: {
    course: Object,
    teachers: Array,
    classrooms: Array
  },
  emits: ['update-course', 'cancel'],
  template: `
    <div class="course-details-overlay">
      <div class="course-details-dialog">
        <h3>编辑课程</h3>
        <div class="edit-form">
          <div class="form-row">
            <div class="form-group">
              <label>课程名称 <span class="required">*</span></label>
              <input v-model="course.name" type="text" placeholder="请输入课程名称" required />
            </div>
            <div class="form-group">
              <label>课程代码 <span class="required">*</span></label>
              <input v-model="course.code" type="text" placeholder="请输入课程代码" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>课程类型 <span class="required">*</span></label>
              <select v-model="course.course_type">
                <option value="必修">必修</option>
                <option value="选修">选修</option>
                <option value="通识">通识</option>
              </select>
            </div>
            <div class="form-group">
              <label>学分 <span class="required">*</span></label>
              <input v-model.number="course.credits" type="number" placeholder="请输入学分" min="0.5" max="6" step="0.5" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>总课时 <span class="required">*</span></label>
              <input v-model.number="course.total_hours" type="number" placeholder="请输入总课时" min="16" max="128" step="8" required />
            </div>
            <div class="form-group">
              <label>教学方式 <span class="required">*</span></label>
              <select v-model="course.teaching_method" @change="updateClassroomSelection">
                <option value="online">线上</option>
                <option value="offline">线下</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>学期 <span class="required">*</span></label>
              <input v-model="course.semester" type="text" placeholder="请输入学期" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>教室 <span v-if="course.teaching_method === 'offline'" class="required">*</span></label>
              <select v-model="course.classroom_id" :disabled="course.teaching_method === 'online'" :required="course.teaching_method === 'offline'">
                <option value="">请选择教室</option>
                <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">{{ classroom.name }} (容量: {{ classroom.capacity }})</option>
              </select>
              <span v-if="course.teaching_method === 'online'" class="online-course-note">线上课程无需选择教室，容量自动设置为1000人</span>
            </div>
          </div>
        </div>
        <div class="dialog-actions">
          <el-button type="primary" plain @click="handleSubmit">保存</el-button>
          <el-button plain @click="$emit('cancel')">取消</el-button>
        </div>
      </div>
    </div>
  `,
  methods: {
    updateClassroomSelection() {
      if (this.course.teaching_method === 'online') {
        this.course.classroom_id = null;
      }
    },
    handleSubmit() {
      // 进行基本的表单验证
      if (!this.course.name || !this.course.code || !this.course.course_type || 
          this.course.credits === null || this.course.total_hours === null || 
          !this.course.teaching_method || !this.course.semester) {
        alert('请填写所有必填字段');
        return;
      }
      
      if (this.course.teaching_method === 'offline' && !this.course.classroom_id) {
        alert('线下课程必须选择教室');
        return;
      }
      
      // 学分和学时验证
      if (this.course.credits < 0.5 || this.course.credits > 6) {
        alert('学分必须在0.5到6之间');
        return;
      }
      
      if (this.course.total_hours < 16 || this.course.total_hours > 128 || this.course.total_hours % 8 !== 0) {
        alert('总课时必须是8的倍数，且在16到128之间');
        return;
      }
      
      this.$emit('update-course');
    }
  }
});

export default defineComponent({
  name: 'Course',
  components: {
    AddCourseForm,
    CourseDetailDialog,
    EditCourseDialog
  },
  setup() {
    // 使用CourseManager中的所有功能
    const courseManager = CourseManager();
    
    // 确保所有函数在模板中可用
    return {
      ...courseManager,
      formatTeachingMethod,
      formatCourseType
    };
  }
});
</script>

<style scoped>
.course-container {
  width: 100%;
}

.required {
  color: #ff4d4f;
}

.online-course-note {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.status-full {
  color: #ff4d4f;
  font-weight: 500;
}

.status-available {
  color: #67c23a;
  font-weight: 500;
}
</style>

<style scoped src="../styles/Course.css"></style>
