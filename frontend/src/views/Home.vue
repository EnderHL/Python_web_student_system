<template>
  <div class="home-container">
    <header class="app-header">
      <div class="header-content">
        <h1>学生管理系统</h1>
        <div class="user-info">
          <span>{{ user?.username }}</span>
          <button @click="handleLogout" class="logout-btn">退出登录</button>
        </div>
      </div>
    </header>

    <nav class="sidebar">
      <ul class="nav-menu">
        <li class="nav-item">
          <router-link to="/" class="nav-link">首页</router-link>
        </li>
        <li class="nav-item" v-if="user?.user_type === 'admin'">
          <router-link to="/teacher" class="nav-link">教师管理</router-link>
        </li>
        <li class="nav-item" v-if="user?.user_type === 'teacher' || user?.user_type === 'admin'">
          <router-link to="/student" class="nav-link">学生管理</router-link>
        </li>
      </ul>
    </nav>

    <main class="main-content">
      <div class="welcome-section">
        <h2>欢迎使用学生管理系统</h2>
        <p>这是系统的主要功能区域，请从左侧菜单选择您需要的功能。</p>
      </div>

      <div class="dashboard-cards">
        <div class="card">
          <h3>系统功能</h3>
          <p>管理学生信息、教师信息和课程安排</p>
        </div>
        <div class="card">
          <h3>角色管理</h3>
          <p>基于角色的访问控制系统，确保数据安全</p>
        </div>
        <div class="card">
          <h3>数据统计</h3>
          <p>提供全面的数据分析和报表功能</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    return {
      authStore,
      router
    }
  },
  data() {
    return {
      user: null
    }
  },
  mounted() {
    // 获取用户信息
    this.loadUserInfo()
  },
  methods: {
    async loadUserInfo() {
      try {
        await this.authStore.fetchUserInfo()
        this.user = this.authStore.user
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    },
    async handleLogout() {
      try {
        await this.authStore.logout()
        this.router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  background-color: #2196F3;
  color: white;
  padding: 15px 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logout-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.logout-btn:hover {
  background-color: #d32f2f;
}

.sidebar {
  width: 200px;
  background-color: #f5f5f5;
  height: calc(100vh - 64px);
  position: fixed;
  left: 0;
  top: 64px;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  padding: 0;
}

.nav-link {
  display: block;
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  border-bottom: 1px solid #e0e0e0;
}

.nav-link:hover {
  background-color: #e0e0e0;
}

.main-content {
  margin-left: 200px;
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.welcome-section {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.welcome-section h2 {
  margin-top: 0;
  color: #333;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card h3 {
  margin-top: 0;
  color: #333;
}
</style>