import axios from 'axios'

const cardsApi = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api/v1',
  timeout: 10000
})

// 请求拦截器：添加JWT token
cardsApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 获取用户拥有的卡片
export const getUserCards = () => {
  return cardsApi.get('/cards/user-cards')
}

// 获取所有卡片定义
export const getAllCards = () => {
  return cardsApi.get('/cards/all-cards')
}

// 获取用户收集统计
export const getUserCollectionStats = () => {
  return cardsApi.get('/cards/collection-stats')
}

export default cardsApi 