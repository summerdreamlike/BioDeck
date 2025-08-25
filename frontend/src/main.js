import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// 注册所有图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(`ElIcon${key}`, component)
}

// 开发环境调试信息
if (process.env.NODE_ENV === 'development') {
  console.log('🚀 Vue DevTools 已启用')
  console.log('📦 已注册的图标组件数量:', Object.keys(ElementPlusIconsVue).length)
  console.log('✅ User 图标:', !!ElementPlusIconsVue.User)
  console.log('✅ Reading 图标:', !!ElementPlusIconsVue.Reading)
  console.log('✅ Lock 图标:', !!ElementPlusIconsVue.Lock)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app') 