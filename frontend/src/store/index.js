import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false,
  }),
  getters: {
    getUserInfo: (state) => state.user,
    getIsAuthenticated: (state) => state.isAuthenticated,
  },
  actions: {
    setUserInfo(user) {
      this.user = user
      this.isAuthenticated = true
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
    },
  },
})

export const useStudentsStore = defineStore('students', {
  state: () => ({
    students: [],
    studentDetails: {},
    rankings: []
  }),
  getters: {
    getStudents: (state) => state.students,
    getStudentById: (state) => (id) => {
      return state.studentDetails[id] || null
    },
    getStudentRankings: (state) => state.rankings
  },
  actions: {
    setStudents(students) {
      this.students = students
    },
    setStudentDetails(id, details) {
      this.studentDetails[id] = details
    },
    setRankings(rankings) {
      this.rankings = rankings
    }
  }
})

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    taskStatistics: {}
  }),
  getters: {
    getTasks: (state) => state.tasks,
    getTaskStatistics: (state) => state.taskStatistics
  },
  actions: {
    setTasks(tasks) {
      this.tasks = tasks
    },
    setTaskStatistics(statistics) {
      this.taskStatistics = statistics
    }
  }
})

export const useMessagesStore = defineStore('messages', {
  state: () => ({
    messages: [],
    unreadCount: 0
  }),
  getters: {
    getMessages: (state) => state.messages,
    getUnreadCount: (state) => state.unreadCount
  },
  actions: {
    setMessages(messages) {
      this.messages = messages
      this.unreadCount = messages.filter(m => !m.read).length
    },
    markAsRead(id) {
      const message = this.messages.find(m => m.id === id)
      if (message && !message.read) {
        message.read = true
        this.unreadCount--
      }
    }
  }
}) 