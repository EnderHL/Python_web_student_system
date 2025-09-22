<template>
  <div id="app">
    <!-- 应用头部 -->
    <Header v-if="showHeader" />
    
    <!-- 主布局容器 -->
    <div class="main-layout" v-if="showLayout">
      <!-- 侧边导航栏 -->
      <Navbar />
      
      <!-- 主内容区域 -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
    
    <!-- 直接显示路由内容（用于登录、注册等页面） -->
    <div v-if="!showLayout">
      <router-view />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import Header from './components/Header.vue';
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Header,
    Navbar
  },
  setup() {
    const route = useRoute();
    const showHeader = ref(false);
    const showLayout = ref(false);

    // 根据当前路由决定是否显示头部和布局
    const updateLayoutVisibility = () => {
      const hideLayoutRoutes = ['/login', '/register'];
      const shouldShowLayout = !hideLayoutRoutes.includes(route.path);
      
      showHeader.value = shouldShowLayout;
      showLayout.value = shouldShowLayout;
    };

    // 组件挂载时初始化布局
    onMounted(() => {
      updateLayoutVisibility();
    });

    // 监听路由变化，更新布局显示状态
    watch(() => route.path, () => {
      updateLayoutVisibility();
    });

    return {
      showHeader,
      showLayout
    };
  }
};
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

#app {
  height: 100%;
}

/* 主布局样式 */
.main-layout {
  display: flex;
  height: calc(100vh - 60px); /* 减去头部高度 */
  margin-top: 60px; /* 为固定头部留出空间 */
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  margin-left: 220px; /* 为固定侧边栏留出空间 */
  padding: 24px;
  overflow-y: auto;
  background-color: #f5f5f5;
  transition: margin-left 0.3s ease;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
    height: auto;
    margin-top: 60px;
  }
  
  .main-content {
    margin-left: 0;
    padding: 16px;
  }
}
</style>
