import { defineStore } from 'pinia'
import api from '../utils/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  actions: {
    // 登录
    async login(credentials) {
      try {
        const response = await api.post('/auth/login/', credentials)
        const data = response.data
        
        if (data.tokens?.access) {
          this.token = data.tokens.access
          this.user = data.user
          this.isAuthenticated = true
          
          // 保存到localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('user', JSON.stringify(this.user))
        }
        
        return data
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },

    // 注册
    async register(userData) {
      try {
        const response = await api.post('/auth/register/', userData)
        const data = response.data
        return data
      } catch (error) {
        console.error('注册失败:', error)
        throw error
      }
    },

    // 登出
    async logout() {
      try {
        // 清除状态
        this.token = null
        this.user = null
        this.isAuthenticated = false
        
        // 清除localStorage
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      } catch (error) {
        console.error('登出失败:', error)
      }
    },

    // 获取用户信息
    async fetchUserInfo() {
      if (!this.token) return
      
      try {
        const response = await api.get('/auth/profile/')
        const data = response.data
        
        this.user = data
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (error) {
        console.error('获取用户信息失败:', error)
        // 如果获取失败，可能是token过期，执行登出
        this.logout()
      }
    }
  }
})