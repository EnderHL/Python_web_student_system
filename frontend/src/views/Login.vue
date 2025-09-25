<template>
  <div class="login-container">
    <div class="login-form">
      <h2>登录</h2>
      <el-form
        ref="loginFormRef"
        :model="form"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="w-full"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      <p class="register-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
      <el-message
        v-if="error"
        type="error"
        :message="error"
        :show-close="true"
      />
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

export default {
  name: 'Login',
  components: {
    User,
    Lock
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    return {
      authStore,
      router,
      ElMessage
    }
  },
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        // 表单验证
        const valid = await this.$refs.loginFormRef.validate()
        if (!valid) return
        
        await this.authStore.login(this.form)
        
        // 登录成功后，重定向到首页
        this.router.push('/')
      } catch (error) {
        this.error = '登录失败，请检查用户名和密码是否正确'
        console.error('Login error:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped src="../styles/Login.css"></style>
