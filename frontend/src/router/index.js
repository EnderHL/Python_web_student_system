import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/teacher',
    name: 'Teacher',
    component: () => import('../views/Teacher.vue'),
    meta: {
      requiresAuth: true,
      adminOnly: true
    }
  },
  {
    path: '/student',
    name: 'Student',
    component: () => import('../views/Student.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/course',
    name: 'Course',
    component: () => import('../views/Course.vue'),
    meta: {
      requiresAuth: true,
      adminOnly: true
    }
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('../views/Schedule.vue'),
    meta: {
      requiresAuth: true,
      adminOnly: true
    }
  },
  {
    path: '/classroom',
    name: 'Classroom',
    component: () => import('../views/Classroom.vue'),
    meta: {
      requiresAuth: true,
      adminOnly: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 检查localStorage中是否有token
    const token = localStorage.getItem('token')
    if (token) {
      // 如果需要管理员权限，检查用户类型
      if (to.meta.adminOnly) {
        const user = JSON.parse(localStorage.getItem('user'))
        if (user && user.user_type === 'admin') {
          next()
        } else {
          alert('您没有权限访问该页面')
          next(from.path || '/')
        }
      } else {
        next()
      }
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router