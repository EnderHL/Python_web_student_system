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
