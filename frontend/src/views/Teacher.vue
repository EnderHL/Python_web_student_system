<template>
  <div class="teacher-container">
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

<script src="../scripts/Teacher.js"></script>

<style scoped>
.teacher-container {
  width: 100%;
}
</style>

<style scoped src="../styles/Teacher.css"></style>
