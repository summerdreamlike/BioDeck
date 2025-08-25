import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/home/index.vue'
import ChatView from '../views/chat/index.vue'
import BiologyView from '../views/biology/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/biology',
      name: 'biology',
      component: BiologyView
    }
  ]
})

export default router 