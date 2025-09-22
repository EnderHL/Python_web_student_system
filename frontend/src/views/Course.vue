<template>
  <div class="course-container">
    <!-- 主内容区域 -->
    <main class="main-content">
        <!-- 课程管理标题和添加按钮 -->
        <div class="course-header">
          <h2>课程管理</h2>
          <button class="add-btn" @click="showAddCourseForm = true">添加课程</button>
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
                <th>任课教师</th>
                <th>上课教室</th>
                <th>已选人数/总人数</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in filteredCourses" :key="course.id">
                <td>{{ course.name }}</td>
                <td>{{ course.code }}</td>
                <td>
                  <span class="course-type-tag" :class="course.type">
                    {{ course.type }}
                  </span>
                </td>
                <td>{{ course.credit }}</td>
                <td>{{ course.totalHours }}</td>
                <td>{{ getTeacherName(course.teacherId) }}</td>
                <td>{{ getClassName(course.classroomId) }}</td>
                <td>{{ course.enrolledStudents }}/{{ course.maxStudents }}</td>
                <td>
                  <button class="view-btn" @click="viewCourseDetails(course.id)">查看</button>
                  <button class="edit-btn" @click="editCourse(course.id)">编辑</button>
                  <button class="delete-btn" @click="deleteCourse(course.id)">删除</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 分页 -->
        <div class="pagination">
          <button :disabled="currentPage <= 1" @click="currentPage > 1 && (currentPage--)">上一页</button>
          <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
          <button :disabled="currentPage >= totalPages" @click="currentPage < totalPages && (currentPage++)">下一页</button>
        </div>
        
        <!-- 课程详情弹窗 -->
        <CourseDetailDialog 
          v-if="showCourseDetails"
          :course="selectedCourse"
          :getTeacherName="getTeacherName"
          :getClassName="getClassName"
          :formatDate="formatDate"
          @close="showCourseDetails = false"
        />
        
        <!-- 编辑课程弹窗 -->
        <EditCourseDialog 
          v-if="showEditCourseForm"
          :course="editingCourse"
          :teachers="teachers"
          :classrooms="classrooms"
          @update-course="updateCourse"
          @cancel="showEditCourseForm = false"
        />
      </main>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import CourseManager from '../scripts/Course.js';

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
          <label>课程名称</label>
          <input v-model="newCourse.name" type="text" placeholder="请输入课程名称" />
        </div>
        <div class="form-group">
          <label>课程代码</label>
          <input v-model="newCourse.code" type="text" placeholder="请输入课程代码" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>课程类型</label>
          <select v-model="newCourse.type">
            <option value="必修">必修</option>
            <option value="选修">选修</option>
            <option value="通识">通识</option>
          </select>
        </div>
        <div class="form-group">
          <label>学分</label>
          <input v-model="newCourse.credit" type="number" placeholder="请输入学分" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>总课时</label>
          <input v-model="newCourse.totalHours" type="number" placeholder="请输入总课时" />
        </div>
        <div class="form-group">
          <label>最大选课人数</label>
          <input v-model="newCourse.maxStudents" type="number" placeholder="请输入最大选课人数" />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>任课教师</label>
          <select v-model="newCourse.teacherId">
            <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
              {{ teacher.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>上课教室</label>
          <select v-model="newCourse.classroomId">
            <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
              {{ classroom.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="form-actions">
        <button class="submit-btn" @click="$emit('add-course')">提交</button>
        <button class="cancel-btn" @click="$emit('cancel')">取消</button>
      </div>
    </div>
  `
});

const CourseDetailDialog = defineComponent({
  name: 'CourseDetailDialog',
  props: {
    course: Object,
    getTeacherName: Function,
    getClassName: Function,
    formatDate: Function
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
            <div class="detail-value">{{ course.type }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">学分：</div>
            <div class="detail-value">{{ course.credit }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">总课时：</div>
            <div class="detail-value">{{ course.totalHours }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">任课教师：</div>
            <div class="detail-value">{{ getTeacherName(course.teacherId) }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">上课教室：</div>
            <div class="detail-value">{{ getClassName(course.classroomId) }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">最大选课人数：</div>
            <div class="detail-value">{{ course.maxStudents }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">已选人数：</div>
            <div class="detail-value">{{ course.enrolledStudents }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">创建时间：</div>
            <div class="detail-value">{{ formatDate(course.createdAt) }}</div>
          </div>
        </div>
        <div class="dialog-actions">
          <button class="close-btn" @click="$emit('close')">关闭</button>
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
              <label>课程名称</label>
              <input v-model="course.name" type="text" placeholder="请输入课程名称" />
            </div>
            <div class="form-group">
              <label>课程代码</label>
              <input v-model="course.code" type="text" placeholder="请输入课程代码" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>课程类型</label>
              <select v-model="course.type">
                <option value="必修">必修</option>
                <option value="选修">选修</option>
                <option value="通识">通识</option>
              </select>
            </div>
            <div class="form-group">
              <label>学分</label>
              <input v-model="course.credit" type="number" placeholder="请输入学分" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>总课时</label>
              <input v-model="course.totalHours" type="number" placeholder="请输入总课时" />
            </div>
            <div class="form-group">
              <label>最大选课人数</label>
              <input v-model="course.maxStudents" type="number" placeholder="请输入最大选课人数" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>任课教师</label>
              <select v-model="course.teacherId">
                <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
                  {{ teacher.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>上课教室</label>
              <select v-model="course.classroomId">
                <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
                  {{ classroom.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div class="dialog-actions">
          <button class="submit-btn" @click="$emit('update-course')">保存</button>
          <button class="cancel-btn" @click="$emit('cancel')">取消</button>
        </div>
      </div>
    </div>
  `
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
    return CourseManager();
  }
});
</script>

<style scoped>
.course-container {
  width: 100%;
}
</style>

<style scoped src="../styles/Course.css"></style>
