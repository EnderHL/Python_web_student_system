import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
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
      form: {
        username: '',
        password: ''
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
