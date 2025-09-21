import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    
    // 如果token存在，添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  error => {
    // 处理请求错误
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 返回完整的响应对象，以便前端代码可以访问response.data
    return response
  },
  error => {
    // 处理响应错误
    console.error('响应错误:', error)
    
    // 处理常见的错误情况
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          window.location.href = '/login'
          break
        case 403:
          alert('您没有权限执行此操作')
          break
        case 404:
          alert('请求的资源不存在')
          break
        case 500:
          alert('服务器错误，请稍后再试')
          break
        default:
          // 其他错误情况
          if (error.response.data.detail) {
            alert(error.response.data.detail)
          } else if (error.response.data.non_field_errors) {
            alert(error.response.data.non_field_errors.join('\n'))
          } else {
            alert('请求失败，请稍后再试')
          }
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      alert('网络错误，请检查您的网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default api