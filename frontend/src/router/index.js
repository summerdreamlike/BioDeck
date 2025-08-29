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
       { path: 'profile', name: 'StudentProfile', alias: '/student/profile', component: () => import('../views/UserProfile.vue'), meta: { hideBottomNav: true, hideAiAssistant: true } },
       { path: 'draw', name: 'Draw', component: () => import('../views/student/Draw.vue') },
       { path: 'atlas', name: 'Atlas', component: () => import('../views/student/Atlas.vue') },
       { path: 'achievements', name: 'Achievements', component: () => import('../views/student/Achievements.vue') },
       // 学生端关卡页面
       { path: 'levelt/level0', name: 'Level0', component: () => import('../views/student/levelt/Level0.vue') },
       { path: 'levelt/level1', name: 'Level1', component: () => import('../views/student/levelt/Level1.vue') },
       { path: 'levelt/level2', name: 'Level2', component: () => import('../views/student/levelt/Level2.vue') },
       { path: 'levelt/level3', name: 'Level3', component: () => import('../views/student/levelt/Level3.vue') },
       { path: 'levelt/level4', name: 'Level4', component: () => import('../views/student/levelt/Level4.vue') },
       { path: 'levelt/level5', name: 'Level5', component: () => import('../views/student/levelt/Level5.vue') },
       { path: 'levelt/level6', name: 'Level6', component: () => import('../views/student/levelt/Level6.vue') },
       { path: 'levelt/level7', name: 'Level7', component: () => import('../views/student/levelt/Level7.vue') },
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
      { path: 'profile', name: 'TeacherProfile', alias: '/profile', component: () => import('../views/UserProfile.vue'), meta: { hideSidebar: true, hideBottomNav: true, hideAiAssistant: true } },
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