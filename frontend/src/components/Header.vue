<template>
  <!-- 应用头部组件 -->
  <header class="app-header">
    <div class="header-content">
      <h1>{{ pageTitle }}</h1>
      <div class="user-info">
        <span>{{ user?.username || '未知用户' }}</span>
        <span v-if="user?.user_type" class="user-role">({{ getUserRoleText(user.user_type) }})</span>
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'Header',
  setup() {
    const user = ref(null);
    const router = useRouter();
    const route = useRoute();

    // 根据当前路由计算页面标题
    const pageTitle = computed(() => {
      const titles = {
        '/': '学生管理系统',
        '/teacher': '学生管理系统 - 教师管理',
        '/course': '学生管理系统 - 课程管理',
        '/schedule': '学生管理系统 - 排课管理',
        '/classroom': '学生管理系统 - 教室管理',
        '/student': '学生管理系统 - 学生管理'
      };
      return titles[route.path] || '学生管理系统';
    });

    // 获取用户角色文本
    const getUserRoleText = (role) => {
      const roles = {
        'admin': '管理员',
        'teacher': '教师',
        'student': '学生'
      };
      return roles[role] || '未知角色';
    };

    // 加载用户信息
    const loadUserInfo = () => {
      try {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          user.value = JSON.parse(storedUser);
        }
      } catch (error) {
        console.error('加载用户信息失败:', error);
      }
    };

    // 处理退出登录
    const handleLogout = () => {
      // 清除本地存储的用户信息
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      user.value = null;
      // 重定向到登录页面
      router.push('/login');
    };

    // 组件挂载时加载用户信息
    onMounted(() => {
      loadUserInfo();
    });

    // 监听路由变化，更新页面标题
    watch(() => route.path, () => {
      // 路由变化时不需要额外操作，因为pageTitle已经是计算属性
    });

    return {
      user,
      pageTitle,
      getUserRoleText,
      handleLogout
    };
  }
};
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  padding: 16px 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 60px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 200;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
}

.header-content h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.user-info {
  display: flex;
  gap: 16px;
  align-items: center;
  font-size: 14px;
}

.user-role {
  opacity: 0.8;
}

.logout-btn {
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-header {
    padding: 12px 16px;
  }
  
  .header-content h1 {
    font-size: 20px;
  }
  
  .user-info {
    gap: 8px;
    font-size: 12px;
  }
  
  .logout-btn {
    padding: 4px 8px;
    font-size: 12px;
  }
}
</style>