import axios from 'axios'

const baseURL = 'http://localhost:5000/api/v1'

const api = axios.create({
  baseURL,
  timeout: 5000
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    // 仅在非 FormData 时设置 JSON 头，避免覆盖 multipart 边界
    if (!(config.data instanceof FormData)) {
      config.headers['Content-Type'] = 'application/json'
    } else {
      // 让浏览器自动设置 multipart 边界
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

// Auth API
export const authApi = {
  login: (payload) => api.post('/auth/login', payload),
  register: (payload) => api.post('/auth/register', payload),
  logout: () => api.post('/auth/logout'),
  refresh: () => api.post('/auth/refresh'),
  changePassword: (old_password, new_password) => api.put('/auth/change-password', { old_password, new_password })
}

// Students API
export const studentsApi = {
  getRankings: () => api.get('/students/rankings'),
  getStudentDetails: (id) => api.get(`/students/${id}`),
  getStudents: () => api.get('/students'),
}

// Exam Center API
export const examApi = {
  getQuestions: (params) => api.get('/questions', { params }),
  getRecommendedQuestions: (studentId) => api.get(`/questions/recommended/${studentId}`),
  createPaper: (data) => api.post('/papers', data)
}

// Classroom API
export const classroomApi = {
  getLiveCourses: () => api.get('/classroom/live'),
  getCourseDetails: (id) => api.get(`/classroom/${id}`),
  sendMessage: (id, message) => api.post(`/classroom/${id}/messages`, { message })
}

// Teaching Materials API
export const materialsApi = {
  getMaterials: (params) => api.get('/materials', { params }),
  uploadMaterial: (data) => api.post('/materials', data),
  deleteMaterial: (id) => api.delete(`/materials/${id}`)
}

// Messages API
export const messagesApi = {
  getMessages: () => api.get('/messages'),
  markAsRead: (id) => api.patch(`/messages/${id}`, { read: true }),
  deleteMessage: (id) => api.delete(`/messages/${id}`)
}

// User/Avatar API
export const userApi = {
  // 让 axios 自动设置 multipart 边界，避免 422
  uploadAvatar: (formData) => api.post('/users/avatar', formData),
  deleteAvatar: () => api.delete('/users/avatar'),
  getAvatar: (userId) => api.get(`/users/avatar/${userId}`)
}

// Tasks API
export const tasksApi = {
  getTasks: () => api.get('/tasks'),
  getTaskStatistics: (id) => api.get(`/tasks/${id}/statistics`),
  createTask: (task) => api.post('/tasks', task),
  updateTask: (id, task) => api.put(`/tasks/${id}`, task),
  deleteTask: (id) => api.delete(`/tasks/${id}`)
}

// Feedback API
export const feedbackApi = {
  getFeedbacks: () => api.get('/feedbacks'),
  getFeedbackStatistics: () => api.get('/feedbacks/statistics')
}

// Attendance API
export const attendanceApi = {
  getAttendance: () => api.get('/attendance'),
  createAttendance: (data) => api.post('/attendance', data),
  exportAttendance: (format = 'csv') => api.get(`/attendance/export?format=${format}`)
}

// Card System API
export const cardApi = {
  getUserCollection: () => api.get('/cards/collection'),
  getAllCards: () => api.get('/cards/all'),
  singleDraw: () => api.post('/cards/draw/single'),
  tenDraw: () => api.post('/cards/draw/ten'),
  getDrawHistory: (limit = 50) => api.get(`/cards/draw/history?limit=${limit}`),
  getDrawCosts: () => api.get('/cards/draw/costs'),
  getUserPoints: () => api.get('/cards/user/points'),
  addPoints: (amount) => api.post('/cards/user/points', { points: amount })
} 


// 班级学生管理 API
export const classStudentsApi = {
  // 根据班级获取学生列表
  getStudentsByClass: (classId) => api.get(`/students?class_id=${classId}`),
  // 获取学生作业完成情况
  getStudentTaskStats: (studentId) => api.get(`/study/data/${studentId}`),
  // 获取任务统计信息
  getTaskStatistics: (params) => api.get('/tasks/statistics', { params })
}