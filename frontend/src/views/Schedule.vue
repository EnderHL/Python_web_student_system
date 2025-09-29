<template>
  <div class="schedule-container">
        <div class="schedule-header">
          <h2>排课管理</h2>
          <button @click="showAddForm = !showAddForm" class="add-btn">
            {{ showAddForm ? '取消添加' : '添加排课' }}
          </button>
        </div>

        <!-- 添加排课表单 -->
        <div v-if="showAddForm" class="add-schedule-form">
          <h3>添加新排课</h3>
          <form @submit.prevent="addSchedule">
            <div class="form-row">
              <div class="form-group">
                <label>课程</label>
                <select v-model="scheduleForm.course" required @change="onCourseChange">
                  <option value="">请选择课程</option>
                  <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.name }} ({{ course.code }}) - {{ course.teaching_method === 'online' ? '线上' : '线下' }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>教师</label>
                <select v-model="scheduleForm.teaching_assignment" required>
                  <option value="">请选择教师</option>
                  <option v-for="ta in teachingAssignments" :key="ta.id" :value="ta.id">
                    {{ ta.teacher_name }} - {{ ta.course_name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>教室</label>
                <select v-model="scheduleForm.classroom" :required="!isCurrentCourseOnline">
                  <option value="">请选择教室</option>
                  <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id" :disabled="isCurrentCourseOnline">
                    {{ classroom.name }} ({{ classroom.location }}，容量：{{ classroom.capacity }})
                  </option>
                  <option v-if="isCurrentCourseOnline" value="" disabled selected>
                    线上课程无需选择教室
                  </option>
                </select>
                <span v-if="isCurrentCourseOnline" class="online-course-note">线上课程容量固定为1000人</span>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>星期</label>
                <select v-model="scheduleForm.day_of_week" required>
                  <option value="">请选择星期</option>
                  <option value="1">周一</option>
                  <option value="2">周二</option>
                  <option value="3">周三</option>
                  <option value="4">周四</option>
                  <option value="5">周五</option>
                  <option value="6">周六</option>
                  <option value="7">周日</option>
                </select>
              </div>
              <div class="form-group">
                <label>起始节次</label>
                <select v-model="scheduleForm.start_section" required @change="onStartSectionChange">
                  <option value="">请选择起始节次</option>
                  <option v-for="section in courseSections" :key="section" :value="section">{{ section }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>结束节次</label>
                <select v-model="scheduleForm.end_section" required :disabled="!scheduleForm.start_section">
                  <option value="">请选择结束节次</option>
                  <option v-for="section in getAvailableEndSections(scheduleForm.start_section)" :key="section" :value="section">{{ section }}</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>排课模式</label>
                <select v-model="scheduleForm.week_pattern" required>
                  <option value="all">每周</option>
                  <option value="odd">单周</option>
                  <option value="even">双周</option>
                </select>
              </div>
            </div>
            <div class="dialog-actions">
              <button type="button" @click="showAddForm = false" class="cancel-btn">取消</button>
              <button type="submit" :disabled="loading" class="submit-btn">
                {{ loading ? '提交中...' : '添加排课' }}
              </button>
            </div>
          </form>
        </div>

        <!-- 排课筛选 -->
        <div class="filter-container">
          <div class="filter-row">
            <div class="filter-group">
              <label>课程</label>
              <select v-model="courseFilter" @change="handleFilterChange">
                <option value="">全部课程</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>
              </select>
            </div>
            <div class="filter-group">
              <label>星期</label>
              <select v-model="dayFilter" @change="handleFilterChange">
                <option value="">全部星期</option>
                <option value="1">周一</option>
                <option value="2">周二</option>
                <option value="3">周三</option>
                <option value="4">周四</option>
                <option value="5">周五</option>
                <option value="6">周六</option>
                <option value="7">周日</option>
              </select>
            </div>
            <div class="filter-group">
              <label>排课模式</label>
              <select v-model="weekPatternFilter" @change="handleFilterChange">
                <option value="">全部模式</option>
                <option value="all">每周</option>
                <option value="odd">单周</option>
                <option value="even">双周</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 排课列表 -->
        <div class="schedule-list">
          <div class="schedule-stats">
            <div class="stat-item">
              <span class="stat-label">总排课数：</span>
              <span class="stat-value">{{ totalSchedules }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">每周排课：</span>
              <span class="stat-value">{{ weeklySchedulesCount }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">单周排课：</span>
              <span class="stat-value">{{ oddWeekSchedulesCount }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">双周排课：</span>
              <span class="stat-value">{{ evenWeekSchedulesCount }}</span>
            </div>
          </div>

          <table class="schedule-table">
            <thead>
              <tr>
                <th>课程</th>
                <th>教师</th>
                <th>教室</th>
                <th>星期</th>
                <th>节次</th>
                <th>排课模式</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="schedule in schedules" :key="schedule.id" :class="{ 'odd-week': schedule.week_pattern === 'odd', 'even-week': schedule.week_pattern === 'even' }">
                <td>{{ getCourseName(schedule.course) }}</td>
                <td>{{ schedule.teacher_name || '未知' }}</td>
                <td>{{ getClassName(schedule.classroom) }}</td>
                <td>{{ getDayOfWeekText(schedule.day_of_week) }}</td>
                <td>{{ schedule.start_section }}-{{ schedule.end_section }}节</td>
                <td>
                  <span class="week-pattern-badge" :class="schedule.week_pattern">
                    {{ getWeekPatternText(schedule.week_pattern) }}
                  </span>
                </td>
                <td>{{ formatDate(schedule.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <button class="view-btn" @click="viewScheduleDetails(schedule)">查看</button>
                    <button class="edit-btn" @click="editSchedule(schedule)">编辑</button>
                    <button class="delete-btn" @click="deleteSchedule(schedule.id)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 分页 -->
          <div class="pagination">
            <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
            <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
            <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">下一页</button>
          </div>
        </div>

        <!-- 排课详情弹窗 -->
        <el-dialog title="排课详情" v-model="showDetailDialog" width="50%">
          <div class="schedule-details">
            <div class="detail-row">
              <span class="detail-label">课程：</span>
              <span class="detail-value">{{ getCourseName(selectedSchedule.course) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">教师：</span>
              <span class="detail-value">{{ selectedSchedule.teacher_name || '未知' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">教室：</span>
              <span class="detail-value">{{ getClassName(selectedSchedule.classroom) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">星期：</span>
              <span class="detail-value">{{ getDayOfWeekText(selectedSchedule.day_of_week) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">节次：</span>
              <span class="detail-value">{{ selectedSchedule.start_section }}-{{ selectedSchedule.end_section }}节</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">排课模式：</span>
              <span class="detail-value">{{ getWeekPatternText(selectedSchedule.week_pattern) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">创建时间：</span>
              <span class="detail-value">{{ formatDate(selectedSchedule.created_at) }}</span>
            </div>
          </div>
          <div class="dialog-actions">
            <button type="button" @click="showDetailDialog = false" class="cancel-btn">关闭</button>
          </div>
        </el-dialog>

        <!-- 编辑排课弹窗 -->
        <el-dialog title="编辑排课" v-model="showEditDialog" width="50%">
          <form @submit.prevent="updateSchedule">
            <div class="form-row">
              <div class="form-group">
                <label>课程</label>
                <select v-model="editForm.course" required @change="onEditCourseChange">
                  <option value="">请选择课程</option>
                  <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.name }} ({{ course.code }}) - {{ course.teaching_method === 'online' ? '线上' : '线下' }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>教师</label>
                <select v-model="editForm.teaching_assignment" required>
                  <option value="">请选择教师</option>
                  <option v-for="ta in editTeachingAssignments" :key="ta.id" :value="ta.id">
                    {{ ta.teacher_name }} - {{ ta.course_name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>教室</label>
                <select v-model="editForm.classroom" :required="!isEditCourseOnline">
                  <option value="">请选择教室</option>
                  <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id" :disabled="isEditCourseOnline">
                    {{ classroom.name }} ({{ classroom.location }}，容量：{{ classroom.capacity }})
                  </option>
                  <option v-if="isEditCourseOnline" value="" disabled selected>
                    线上课程无需选择教室
                  </option>
                </select>
                <span v-if="isEditCourseOnline" class="online-course-note">线上课程容量固定为1000人</span>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>星期</label>
                <select v-model="editForm.day_of_week" required>
                  <option value="">请选择星期</option>
                  <option value="1">周一</option>
                  <option value="2">周二</option>
                  <option value="3">周三</option>
                  <option value="4">周四</option>
                  <option value="5">周五</option>
                  <option value="6">周六</option>
                  <option value="7">周日</option>
                </select>
              </div>
              <div class="form-group">
                <label>起始节次</label>
                <select v-model="editForm.start_section" required @change="onEditStartSectionChange">
                  <option value="">请选择起始节次</option>
                  <option v-for="section in courseSections" :key="section" :value="section">{{ section }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>结束节次</label>
                <select v-model="editForm.end_section" required :disabled="!editForm.start_section">
                  <option value="">请选择结束节次</option>
                  <option v-for="section in getAvailableEndSections(editForm.start_section)" :key="section" :value="section">{{ section }}</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>排课模式</label>
                <select v-model="editForm.week_pattern" required>
                  <option value="all">每周</option>
                  <option value="odd">单周</option>
                  <option value="even">双周</option>
                </select>
              </div>
            </div>
            <div class="dialog-actions">
              <button type="button" @click="showEditDialog = false" class="cancel-btn">取消</button>
              <button type="submit" :disabled="loading" class="submit-btn">
                {{ loading ? '提交中...' : '保存修改' }}
              </button>
            </div>
          </form>
        </el-dialog>
  </div>
</template>

<script src="../scripts/Schedule.js"></script>

  <style scoped>
  .schedule-container {
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
  }
  </style>
  
  <style scoped src="../styles/Schedule.css"></style>
