import axios from 'axios'

// 创建API实例
const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 5000
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    if (!(config.data instanceof FormData)) {
      config.headers['Content-Type'] = 'application/json'
    } else {
      delete config.headers['Content-Type']
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/Login'
    }
    return Promise.reject(error)
  }
)

// 每日签到相关API
export const dailyCheckinApi = {
  // 获取用户签到状态
  getStatus() {
    return api.get('/api/v1/daily-checkin/status')
  },

  // 执行签到
  checkin() {
    return api.post('/api/v1/daily-checkin/checkin')
  },

  // 获取签到历史
  getHistory(limit = 30) {
    return api.get('/api/v1/daily-checkin/history', {
      params: { limit }
    })
  },

  // 获取积分历史
  getPointHistory(limit = 50) {
    return api.get('/api/v1/daily-checkin/point-history', {
      params: { limit }
    })
  },

  // 获取积分排行榜
  getLeaderboard(limit = 20) {
    return api.get('/api/v1/daily-checkin/leaderboard', {
      params: { limit }
    })
  }
} 