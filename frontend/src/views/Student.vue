<template>
  <div class="student-container">
    <main class="main-content">
      <div class="student-header">
        <h2>学生管理</h2>
        <button @click="showAddForm = !showAddForm" class="add-btn">
          {{ showAddForm ? '取消添加' : '添加学生' }}
        </button>
      </div>

      <!-- 添加学生表单 -->
      <div v-if="showAddForm" class="add-student-form">
        <h3>添加新学生</h3>
        <form @submit.prevent="addStudent">
          <div class="form-row">
            <div class="form-group">
              <label>姓名</label>
              <input v-model="studentForm.name" required placeholder="请输入姓名" />
            </div>
            <div class="form-group">
              <label>年龄</label>
              <input type="number" v-model="studentForm.age" required placeholder="请输入年龄" />
            </div>
            <div class="form-group">
              <label>性别</label>
              <select v-model="studentForm.gender">
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>班级</label>
              <input v-model="studentForm.class_name" required placeholder="请输入班级" />
            </div>
            <div class="form-group">
              <label>学号</label>
              <input v-model="studentForm.student_id" required placeholder="请输入学号" />
            </div>
            <div class="form-group">
              <label>学院</label>
              <input v-model="studentForm.college" required placeholder="请输入学院" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>电话</label>
              <input v-model="studentForm.phone" placeholder="请输入电话" />
            </div>
          </div>
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? '提交中...' : '添加学生' }}
          </button>
        </form>
      </div>

      <!-- 学生列表 -->
      <div class="student-list">
        <h3>学生列表</h3>
        <div class="search-container">
          <div class="search-input-wrapper">
            <input v-model="searchQuery" placeholder="搜索学生..." class="search-input" />
            <button @click="handleSearch" class="search-btn">搜索</button>
          </div>
        </div>
        <table class="student-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>年龄</th>
              <th>性别</th>
              <th>班级</th>
              <th>学号</th>
              <th>学院</th>
              <th>电话</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in filteredStudents" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.name }}</td>
              <td>{{ student.age }}</td>
              <td>{{ student.gender }}</td>
              <td>{{ student.class_name }}</td>
              <td>{{ student.student_id }}</td>
              <td>{{ student.college }}</td>
              <td>{{ student.phone || '-' }}</td>
              <td>
                <button @click="editStudent(student)" class="edit-btn">编辑</button>
                <button @click="deleteStudent(student.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="students.length === 0" class="no-data">暂无学生数据</div>
      </div>

      <!-- 编辑学生对话框 -->
      <div v-if="editingStudent" class="modal-overlay" @click="closeEditModal">
        <div class="modal-content" @click.stop>
          <h3>编辑学生</h3>
          <form @submit.prevent="updateStudent">
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
                <label>班级</label>
                <input v-model="editForm.class_name" required placeholder="请输入班级" />
              </div>
              <div class="form-group">
                <label>学号</label>
                <input v-model="editForm.student_id" required placeholder="请输入学号" />
              </div>
              <div class="form-group">
                <label>学院</label>
                <input v-model="editForm.college" required placeholder="请输入学院" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>电话</label>
                <input v-model="editForm.phone" placeholder="请输入电话" />
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

      <!-- 错误提示 -->
      <div v-if="error" class="error-message">{{ error }}</div>
    </main>
  </div>
</template>

<script src="../scripts/Student.js"></script>

  <style scoped>
  .student-container {
    width: 100%;
  }
  </style>
  
  <style scoped src="../styles/Student.css"></style>
