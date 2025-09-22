import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Home',
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
      user: null
    }
  },
  mounted() {
    // 获取用户信息
    this.loadUserInfo()
  },
  methods: {
    async loadUserInfo() {
      try {
        await this.authStore.fetchUserInfo()
        this.user = this.authStore.user
      } catch (error) {
        console.error('Failed to load user info:', error)
      }
    },
    async handleLogout() {
      try {
        await this.authStore.logout()
        this.router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  }
}
