<template>
  <div class="classroom-container">
    <main class="main-content">
        <div class="classroom-header">
          <h2>教室管理</h2>
          <button @click="showAddForm = !showAddForm" class="add-btn">
            {{ showAddForm ? '取消添加' : '添加教室' }}
          </button>
        </div>

        <!-- 添加教室表单 -->
        <div v-if="showAddForm" class="add-classroom-form">
          <h3>添加新教室</h3>
          <form @submit.prevent="addClassroom">
            <div class="form-row">
              <div class="form-group">
                <label>教室名称</label>
                <input type="text" v-model="classroomForm.name" required placeholder="请输入教室名称">
              </div>
              <div class="form-group">
                <label>位置</label>
                <input type="text" v-model="classroomForm.location" required placeholder="请输入教室位置">
              </div>
              <div class="form-group">
                <label>容量</label>
                <input type="number" v-model="classroomForm.capacity" required placeholder="请输入教室容量" min="1">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>设备配置</label>
                <div class="equipment-list">
                  <label v-for="equipment in equipmentList" :key="equipment.id" class="equipment-checkbox">
                    <input type="checkbox" :value="equipment.id" v-model="classroomForm.equipment_ids">
                    {{ equipment.name }}
                  </label>
                </div>
              </div>
              <div class="form-group">
                <label>描述</label>
                <textarea v-model="classroomForm.description" placeholder="请输入教室描述" rows="4"></textarea>
              </div>
            </div>
            <div class="dialog-actions">
              <button type="button" @click="showAddForm = false" class="cancel-btn">取消</button>
              <button type="submit" :disabled="loading" class="submit-btn">
                {{ loading ? '提交中...' : '添加教室' }}
              </button>
            </div>
          </form>
        </div>

        <!-- 教室筛选 -->
        <div class="filter-container">
          <div class="filter-row">
            <div class="search-group">
              <input type="text" v-model="searchQuery" @input="handleSearch" placeholder="搜索教室名称或位置">
              <button @click="clearSearch" class="clear-btn">清除</button>
            </div>
          </div>
        </div>

        <!-- 教室列表 -->
        <div class="classroom-list">
          <div class="classroom-stats">
            <div class="stat-item">
              <span class="stat-label">总教室数：</span>
              <span class="stat-value">{{ totalClassrooms }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">小教室（<20人）：</span>
              <span class="stat-value">{{ smallClassroomsCount }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">中教室（20-50人）：</span>
              <span class="stat-value">{{ mediumClassroomsCount }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">大教室（>50人）：</span>
              <span class="stat-value">{{ largeClassroomsCount }}</span>
            </div>
          </div>

          <table class="classroom-table">
            <thead>
              <tr>
                <th>教室名称</th>
                <th>位置</th>
                <th>容量</th>
                <th>设备配置</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="classroom in classrooms" :key="classroom.id">
                <td>{{ classroom.name }}</td>
                <td>{{ classroom.location }}</td>
                <td :class="getCapacityBadgeClass(classroom.capacity)">{{ classroom.capacity }}人</td>
                <td>
                  <div class="equipment-tags">
                    <span v-for="equipment in classroom.equipment" :key="equipment.id" class="equipment-tag">
                      {{ equipment.name }}
                    </span>
                  </div>
                </td>
                <td>{{ formatDate(classroom.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <button class="view-btn" @click="viewClassroomDetails(classroom)">查看</button>
                    <button class="edit-btn" @click="editClassroom(classroom)">编辑</button>
                    <button class="delete-btn" @click="deleteClassroom(classroom.id)">删除</button>
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

        <!-- 教室详情弹窗 -->
        <el-dialog title="教室详情" v-model="showDetailDialog" width="50%">
          <div class="classroom-details">
            <div class="detail-row">
              <span class="detail-label">教室名称：</span>
              <span class="detail-value">{{ selectedClassroom.name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">位置：</span>
              <span class="detail-value">{{ selectedClassroom.location }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">容量：</span>
              <span class="detail-value">{{ selectedClassroom.capacity }}人</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">设备：</span>
              <div class="detail-value">
                <div class="equipment-list">
                  <span v-for="equipment in selectedClassroom.equipment" :key="equipment.id" class="equipment-item">
                    {{ equipment.name }}
                  </span>
                </div>
              </div>
            </div>
            <div class="detail-row">
              <span class="detail-label">描述：</span>
              <span class="detail-value">{{ selectedClassroom.description || '无' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">创建时间：</span>
              <span class="detail-value">{{ formatDate(selectedClassroom.created_at) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">更新时间：</span>
              <span class="detail-value">{{ formatDate(selectedClassroom.updated_at) }}</span>
            </div>
          </div>
          <div class="dialog-actions">
            <button type="button" @click="showDetailDialog = false" class="cancel-btn">关闭</button>
          </div>
        </el-dialog>

        <!-- 编辑教室弹窗 -->
        <el-dialog title="编辑教室" v-model="showEditDialog" width="50%">
          <form @submit.prevent="updateClassroom">
            <div class="form-row">
              <div class="form-group">
                <label>教室名称</label>
                <input type="text" v-model="editForm.name" required placeholder="请输入教室名称">
              </div>
              <div class="form-group">
                <label>位置</label>
                <input type="text" v-model="editForm.location" required placeholder="请输入教室位置">
              </div>
              <div class="form-group">
                <label>容量</label>
                <input type="number" v-model="editForm.capacity" required placeholder="请输入教室容量" min="1">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>设备配置</label>
                <div class="equipment-list">
                  <label v-for="equipment in equipmentList" :key="equipment.id" class="equipment-checkbox">
                    <input type="checkbox" :value="equipment.id" v-model="editForm.equipment_ids">
                    {{ equipment.name }}
                  </label>
                </div>
              </div>
              <div class="form-group">
                <label>描述</label>
                <textarea v-model="editForm.description" placeholder="请输入教室描述" rows="4"></textarea>
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
      </main>
  </div>
</template>

<script src="../scripts/Classroom.js"></script>

  <style scoped>
  .classroom-container {
    width: 100%;
  }
  </style>
  
  <style scoped src="../styles/Classroom.css"></style>
