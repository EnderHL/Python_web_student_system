<template>
  <div class="register-container">
    <div class="register-form">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            required
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            class="form-control"
            placeholder="请输入邮箱"
          />
        </div>

        <div class="form-group">
          <label for="first_name">名字</label>
          <input
            type="text"
            id="first_name"
            v-model="form.first_name"
            class="form-control"
            placeholder="请输入名字"
          />
        </div>

        <div class="form-group">
          <label for="last_name">姓氏</label>
          <input
            type="text"
            id="last_name"
            v-model="form.last_name"
            class="form-control"
            placeholder="请输入姓氏"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            class="form-control"
            placeholder="请输入密码"
          />
        </div>
        <div class="form-group">
          <label for="password2">确认密码</label>
          <input
            type="password"
            id="password2"
            v-model="form.password2"
            required
            placeholder="请再次输入密码"
          />
        </div>
        <div class="form-group">
          <label for="user_type">用户类型</label>
          <select id="user_type" v-model="form.user_type" required>
            <option value="student">学生</option>
            <option value="teacher">教师</option>
          </select>
        </div>
        <button type="submit" :disabled="loading" class="register-btn">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

export default {
  name: 'Register',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const form = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
      password2: '',
      user_type: 'student'
    })
    const loading = ref(false)
    const error = ref('')
    const success = ref('')
    
    async function handleRegister() {
      // 检查密码是否一致
      if (form.value.password !== form.value.password2) {
        error.value = '两次输入的密码不一致'
        return
      }
      
      loading.value = true
      error.value = ''
      success.value = ''
      
      try {
        await authStore.register(form.value)
        
        success.value = '注册成功，请登录'
        
        // 3秒后跳转到登录页
        setTimeout(() => {
          router.push('/login')
        }, 3000)
      } catch (err) {
        if (err.response && err.response.data) {
          const errorData = err.response.data
          // 处理各种可能的错误信息
          if (errorData.username) {
            error.value = errorData.username[0]
          } else if (errorData.email) {
            error.value = errorData.email[0]
          } else if (errorData.password) {
            error.value = errorData.password[0]
          } else if (errorData.detail) {
            error.value = errorData.detail
          } else {
            error.value = '注册失败，请稍后再试'
          }
        } else {
          error.value = '注册失败，请检查网络连接'
        }
        console.error('Register error:', err)
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      error,
      success,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.register-form {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

input:focus,
select:focus {
  outline: none;
  border-color: #4CAF50;
}

.register-btn {
  width: 100%;
  padding: 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-btn:hover:not(:disabled) {
  background-color: #0b7dda;
}

.register-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 15px;
}

.login-link a {
  color: #2196F3;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.error-message {
  color: #f44336;
  margin-top: 10px;
  text-align: center;
}

.success-message {
  color: #4CAF50;
  margin-top: 10px;
  text-align: center;
}
</style>