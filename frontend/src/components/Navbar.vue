<template>
  <!-- 侧边导航栏组件 - Element Plus 风格 -->
  <el-menu
    :default-active="$route.path"
    class="sidebar el-menu-vertical-demo"
    @open="handleOpen"
    @close="handleClose"
    background-color="#ffffff"
    text-color="#5a6268"
    active-text-color="#3498db"
    router
  >
    <el-menu-item index="/">
      <el-icon><House /></el-icon>
      <span>首页</span>
    </el-menu-item>
    <el-menu-item index="/teacher" v-if="user?.user_type === 'admin'">
      <el-icon><User /></el-icon>
      <span>教师管理</span>
    </el-menu-item>
    <el-menu-item index="/course" v-if="user?.user_type === 'admin'">
      <el-icon><Document /></el-icon>
      <span>课程管理</span>
    </el-menu-item>
    <el-menu-item index="/schedule" v-if="user?.user_type === 'admin'">
      <el-icon><Calendar /></el-icon>
      <span>排课管理</span>
    </el-menu-item>
    <el-menu-item index="/classroom" v-if="user?.user_type === 'admin'">
      <el-icon><OfficeBuilding /></el-icon>
      <span>教室管理</span>
    </el-menu-item>
    <el-menu-item index="/student" v-if="user?.user_type === 'teacher' || user?.user_type === 'admin'">
      <el-icon><UserFilled /></el-icon>
      <span>学生管理</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { House, User, Document, Calendar, OfficeBuilding, UserFilled } from '@element-plus/icons-vue';

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

    // 菜单展开/收起事件处理
    const handleOpen = (key, keyPath) => {
      console.log(key, keyPath);
    }

    const handleClose = (key, keyPath) => {
      console.log(key, keyPath);
    }

    return {
      user,
      handleOpen,
      handleClose
    };
  }
};
</script>

<style scoped>
.sidebar {
  width: 220px;
  border-right: 1px solid #e9ecef;
  height: calc(100vh - 60px); /* 减去头部高度 */
  position: fixed;
  left: 0;
  top: 60px;
  z-index: 100;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

/* 确保element的菜单样式正确应用 */
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 220px;
  min-height: 400px;
}

/* 响应式设计 - Element Plus的响应式样式已经处理了大部分情况 */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
    position: relative;
    top: 0;
  }
  
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 100%;
  }
}
</style>