import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/splash'
  },
  {
    path: '/splash',
    name: 'Splash',
    component: () => import('../views/Splash.vue'),
    meta: { fullscreen: true, transition: 'splash' }
  },
  {
    path: '/Login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { fullscreen: true, transition: 'login' }
  },
  {
    path: '/StudentSide',
    name: 'StudentSide',
    component: () => import('../views/student/StudentSide.vue'),
    redirect: '/StudentSide/Home',
    children:[
       { path: 'Home', name: 'Home', alias: '/Home', component: () => import('../views/student/Home.vue') },
       { path: 'profile', name: 'StudentProfile', alias: '/student/profile', component: () => import('../views/UserProfile.vue') },
    ]
  },
  {
    path: '/TeacherSide',
    name: 'TeacherSide',
    component: () => import('../views/TeacherSide.vue'),
    children: [
      { path: 'dashboard', name: 'Dashboard', alias: '/dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'student/:id', name: 'StudentDetail', alias: '/student/:id', component: () => import('../views/StudentDetail.vue') },
      { path: 'exam-center', name: 'ExamCenter', alias: '/exam-center', component: () => import('../views/ExamCenter.vue') },
      { path: 'teaching-materials', name: 'TeachingMaterials', alias: '/teaching-materials', component: () => import('../views/TeachingMaterials.vue') },
      { path: 'messages', name: 'Messages', alias: '/messages', component: () => import('../views/Messages.vue') },
      { path: 'tasks', name: 'Tasks', alias: '/tasks', component: () => import('../views/Tasks.vue') },
      { path: 'feedback', name: 'Feedback', alias: '/feedback', component: () => import('../views/Feedback.vue') },
      { path: 'attendance', name: 'Attendance', alias: '/attendance', component: () => import('../views/Attendance.vue') },
      { path: 'profile', name: 'TeacherProfile', alias: '/profile', component: () => import('../views/UserProfile.vue') },
    ]
  },
  {
      path: '/404',
      name: '404',
      component: () => import('../views/404.vue'),
      meta: { fullscreen: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      redirect: '/404'
    }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router