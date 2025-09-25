<template>
  <div class="register-container">
    <div class="register-form">
      <h2>注册</h2>
      <el-form
        ref="registerFormRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱"
            :prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item label="名字" prop="first_name">
          <el-input
            v-model="form.first_name"
            placeholder="请输入名字"
          />
        </el-form-item>
        <el-form-item label="姓氏" prop="last_name">
          <el-input
            v-model="form.last_name"
            placeholder="请输入姓氏"
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
        <el-form-item label="确认密码" prop="password2">
          <el-input
            v-model="form.password2"
            type="password"
            placeholder="请再次输入密码"
            :prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item label="用户类型" prop="user_type">
          <el-select v-model="form.user_type" placeholder="请选择用户类型">
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="w-full"
            @click="handleRegister"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>
      <p class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
      <el-message
        v-if="error"
        type="error"
        :message="error"
        :show-close="true"
      />
      <el-message
        v-if="success"
        type="success"
        :message="success"
        :show-close="true"
      />
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { User, Message, Lock } from '@element-plus/icons-vue'

export default {
  name: 'Register',
  components: {
    User,
    Message,
    Lock
  },
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
    
    // 自定义密码确认验证规则
    const validatePassword2 = (rule, value, callback) => {
      if (value !== form.value.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应在3到20个字符之间', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
      ],
      first_name: [
        { required: true, message: '请输入名字', trigger: 'blur' }
      ],
      last_name: [
        { required: true, message: '请输入姓氏', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
      ],
      password2: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        { validator: validatePassword2, trigger: 'blur' }
      ],
      user_type: [
        { required: true, message: '请选择用户类型', trigger: 'change' }
      ]
    }
    
    async function handleRegister() {
      loading.value = true
      error.value = ''
      success.value = ''
      
      try {
        // 表单验证
        await this.$refs.registerFormRef.validate()
        
        await authStore.register(form.value)
        
        success.value = '注册成功，请登录'
        
        // 3秒后跳转到登录页
        setTimeout(() => {
          router.push('/login')
        }, 3000)
      } catch (err) {
        if (err.name === 'Error' && err.message) {
          // 处理表单验证错误
          error.value = err.message
        } else if (err.response && err.response.data) {
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
      rules,
      handleRegister,
      validatePassword2
    }
  }
}
</script>

<style scoped src="../styles/Register.css"></style>