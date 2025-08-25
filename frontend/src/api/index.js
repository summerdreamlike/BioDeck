import axios from 'axios'

const baseURL = 'http://localhost:5000/api/v1'

const api = axios.create({
  baseURL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
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