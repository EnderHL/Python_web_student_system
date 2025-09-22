<template>
  <!-- 侧边导航栏组件 -->
  <nav class="sidebar">
    <ul class="nav-menu">
      <li class="nav-item">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
          首页
        </router-link>
      </li>
      <li class="nav-item" v-if="user?.user_type === 'admin'">
        <router-link to="/teacher" class="nav-link" :class="{ active: $route.path === '/teacher' }">
          教师管理
        </router-link>
      </li>
      <li class="nav-item" v-if="user?.user_type === 'admin'">
        <router-link to="/course" class="nav-link" :class="{ active: $route.path === '/course' }">
          课程管理
        </router-link>
      </li>
      <li class="nav-item" v-if="user?.user_type === 'admin'">
        <router-link to="/schedule" class="nav-link" :class="{ active: $route.path === '/schedule' }">
          排课管理
        </router-link>
      </li>
      <li class="nav-item" v-if="user?.user_type === 'admin'">
        <router-link to="/classroom" class="nav-link" :class="{ active: $route.path === '/classroom' }">
          教室管理
        </router-link>
      </li>
      <li class="nav-item" v-if="user?.user_type === 'teacher' || user?.user_type === 'admin'">
        <router-link to="/student" class="nav-link" :class="{ active: $route.path === '/student' }">
          学生管理
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'Navbar',
  setup() {
    const user = ref(null);
    const router = useRouter();

    // 加载用户信息
    const loadUserInfo = () => {
      try {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          // 安全解析用户信息，避免格式错误
          try {
            const parsedUser = JSON.parse(storedUser);
            // 验证用户信息是否包含必要的字段
            if (parsedUser && typeof parsedUser.user_type === 'string') {
              user.value = parsedUser;
              return true; // 加载成功
            }
          } catch (parseError) {
            console.error('解析用户信息失败:', parseError);
          }
        }
        
        // 如果没有有效的用户信息，清除localStorage并返回false
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        return false; // 加载失败
      } catch (error) {
        console.error('加载用户信息失败:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        return false; // 加载失败
      }
    };

    // 组件挂载时加载用户信息
    onMounted(() => {
      const hasValidUser = loadUserInfo();
      
      // 只有当用户信息无效且当前不在登录页时，才重定向到登录页
      if (!hasValidUser && router.currentRoute.value.path !== '/login') {
        router.push('/login');
      }
    });

    return {
      user
    };
  }
};
</script>

<style scoped>
.sidebar {
  width: 220px;
  background-color: #ffffff;
  border-right: 1px solid #e9ecef;
  overflow-y: auto;
  flex-shrink: 0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  height: calc(100vh - 60px); /* 减去头部高度 */
  position: fixed;
  left: 0;
  top: 60px;
  z-index: 100;
}

.nav-menu {
  padding: 16px 0;
  margin: 0;
  list-style: none;
}

.nav-item {
  margin: 4px 0;
}

.nav-link {
  display: block;
  padding: 12px 24px;
  color: #5a6268;
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  font-size: 14px;
}

.nav-link:hover {
  background-color: #f8f9fa;
  color: #3498db;
  border-left-color: #3498db;
}

.nav-link.active {
  background-color: #3498db;
  color: white;
  border-left-color: #2980b9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
    max-height: 200px;
    position: relative;
    top: 0;
  }
  
  .nav-menu {
    display: flex;
    flex-wrap: wrap;
    padding: 8px;
  }
  
  .nav-item {
    margin: 4px;
  }
  
  .nav-link {
    padding: 8px 16px;
    border-radius: 4px;
    border-left: none;
  }
}
</style>