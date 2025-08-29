<template>
  <section class="auth-page enter">
    <el-card class="auth-card" shadow="hover">
      <div class="card-head">
        <div class="emblem">
          <ElIconUser class="emblem-icon" />
        </div>
        <div class="head-text">
          <h2 class="head-title">欢迎登录</h2>
        </div>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" class="form" @submit.prevent="onSubmit">
        <!-- 仅注册时需要角色选择 -->
        <el-form-item v-if="mode==='register'" label="角色" prop="role">
          <div class="role-toggle">
            <button type="button" :class="['role-btn', { active: form.role==='student' }]" @click="form.role='student'">
              <ElIconReading class="i" /> 学生
            </button>
            <button type="button" :class="['role-btn', { active: form.role==='teacher' }]" @click="form.role='teacher'">
              <ElIconUser class="i" /> 老师
            </button>
          </div>
        </el-form-item>

        <!-- 登录：姓名/学号；注册：姓名 -->
        <el-form-item :label="mode==='login' ? '用户名' : '姓名'" prop="username">
          <el-input 
            v-model="form.username" 
            autocomplete="username" 
            clearable
            :placeholder="mode==='login' ? '请输入姓名或学号/工号' : '请输入真实姓名'"
          >
            <template #prefix>
              <ElIconUser class="ipfx" />
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            show-password 
            autocomplete="current-password" 
            clearable
            placeholder="请输入密码"
          >
            <template #prefix>
              <ElIconLock class="ipfx" />
            </template>
          </el-input>
        </el-form-item>

        <!-- 注册：学生填学号；老师填工号 -->
        <el-form-item v-if="mode==='register'" :label="form.role==='student' ? '学号' : '工号'" prop="identifier">
          <el-input 
            v-model="form.identifier" 
            clearable
            :placeholder="form.role==='student' ? '请输入学号（以1001开头）' : '请输入工号（以2001开头）'"
          >
            <template #prefix>
              <component :is="form.role==='student' ? 'ElIconNotebook' : 'ElIconCollection'" class="ipfx" />
            </template>
          </el-input>
        </el-form-item>

        <el-form-item class="actions" label-width="0">
          <el-button :class="['submit','primary-btn', status]" type="primary" native-type="submit">
            <transition name="scaleFade" mode="out-in">
              <span v-if="status==='idle'" key="idle">{{ mode==='login' ? '登录' : '注册' }}</span>
              <span v-else-if="status==='loading'" key="loading" class="spinner" aria-live="polite" aria-busy="true">
                <svg class="spin" width="18" height="18" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="25" cy="25" r="20" stroke="rgba(255,255,255,.35)" stroke-width="6"/>
                  <path d="M45 25a20 20 0 0 1-20 20" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
                </svg>
              </span>
              <span v-else-if="status==='success'" key="success" class="success"><ElIconCheck class="big-icon" /></span>
              <span v-else key="error" class="error"><ElIconClose class="big-icon" /></span>
            </transition>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 右下角切换链接 -->
      <div class="switch-br">
        <el-button class="submit_link" link @click="toggleMode">{{ mode==='login' ? '没有账号？去注册' : '已有账号？去登录' }}</el-button>
      </div>
    </el-card>
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authApi } from '../api'
import { useUserStore } from '../store'

const router = useRouter()
const userStore = useUserStore()
const mode = ref('login')
const exiting = ref(false)
const status = ref('idle') // idle | loading | success | error
const formRef = ref()
const form = reactive({ role: 'student', username: '', password: '', identifier: '' })

const rules = {
  role: [{ required: () => mode.value==='register', message: '请选择角色', trigger: 'change' }],
  username: [{ required: true, message: () => mode.value==='login' ? '请输入姓名或学号' : '请输入姓名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  identifier: [{ required: () => mode.value==='register', message: () => form.role==='student' ? '请输入学号' : '请输入工号', trigger: 'blur' }]
}

function toggleMode() {
  mode.value = mode.value === 'login' ? 'register' : 'login'
  status.value = 'idle'
  form.username = ''
  form.password = ''
  form.identifier = ''
}

async function onSubmit() {
  // 防重复提交
  if (status.value !== 'idle') return
  try {
    await formRef.value.validate()
  } catch {
    const el = document.querySelector('.form')
    if (el) { el.classList.remove('error-shake'); void el.offsetWidth; el.classList.add('error-shake') }
    return
  }
  status.value = 'loading'
  try {
    if (mode.value === 'register') {
      // 注册逻辑：需要角色、姓名、学号/工号、密码
      const payload = { 
        name: form.username,           // 映射到后端期望的 name 字段
        password: form.password, 
        role: form.role,
        id_number: form.identifier     // 映射到后端期望的 id_number 字段
      }
      const res = await authApi.register(payload)
      const data = res?.data ?? res
      status.value = 'success'
      ElMessage.success('注册成功！请使用您的账号登录')
      
      // 注册成功后切换到登录模式，并清空表单
      setTimeout(() => {
        mode.value = 'login'
        status.value = 'idle'
        form.username = ''
        form.password = ''
        form.identifier = ''
      }, 1500)
    } else {
      // 登录逻辑：支持姓名/学号+密码
      const usernameLower = form.username.trim().toLowerCase()
      const isDigits = /^\d+$/.test(usernameLower)
      let tryRoles
      if (usernameLower === 'admin') {
        tryRoles = ['admin']
      } else if (isDigits && usernameLower.startsWith('1001')) {
        tryRoles = ['student']
      } else if (isDigits && usernameLower.startsWith('2001')) {
        tryRoles = ['teacher']
      } else {
        tryRoles = ['student','teacher']
      }
      let ok = false, lastErr
      
      for (const role of tryRoles) {
        try {
          const res = await authApi.login({ 
            name_or_id: form.username,  // 映射到后端期望的 name_or_id 字段
            password: form.password, 
            role: role 
          })
          const data = res?.data ?? res
          localStorage.setItem('token', data.access_token)
          localStorage.setItem('user', JSON.stringify(data.user))
          
          // 将用户信息存储到store中
          userStore.setUserInfo(data.user)
          
          status.value = 'success'
          ElMessage.success('登录成功，正在跳转...')
          setTimeout(() => redirectByRole(data.user.role), 420)
          ok = true
          break
        } catch (e) { 
          lastErr = e 
        }
      }
      if (!ok) {
        // 所有角色都尝试失败，显示具体的错误信息
        if (lastErr && lastErr.response && lastErr.response.data) {
          const errorData = lastErr.response.data
          const errorMessage = errorData.message
          
          if (errorMessage && errorMessage.includes('不存在') || errorMessage.includes('密码错误')) {
            ElMessage.error('用户名或密码错误，请检查后重试')
          } else {
            ElMessage.error(errorMessage || '登录失败，请检查账号信息')
          }
        } else {
          ElMessage.error('登录失败，请检查账号信息')
        }
        throw lastErr || new Error('登录失败')
      }
    }
  } catch (e) {
    console.error(e)
    status.value = 'error'
    
    // 处理特定的错误情况
    if (e.response && e.response.data) {
      const errorData = e.response.data
      const errorMessage = errorData.message
      
      // 针对账号已存在的情况
      if (errorMessage && (errorMessage.includes('已存在') || errorMessage.includes('学号已存在') || errorMessage.includes('教职工号已存在'))) {
        ElMessage.error(errorMessage)
      } else if (errorMessage && errorMessage.includes('格式')) {
        // 针对格式错误的情况
        ElMessage.error(errorMessage)
      }
    } else {
      // 网络错误或其他未知错误
      ElMessage.error('操作失败，请检查网络连接后重试')
    }
    
    setTimeout(() => (status.value = 'idle'), 1000)
  }
}

function redirectByRole(role, replace = false) {
  if (role === 'student') return replace ? router.replace('/StudentSide/Home') : router.push('/StudentSide/Home')
  if (role === 'teacher') return replace ? router.replace({ name: 'Dashboard' }) : router.push({ name: 'Dashboard' })
  if (role === 'admin')   return replace ? router.replace({ name: 'Dashboard' }) : router.push({ name: 'Dashboard' })
}
</script>

<style scoped>
:root { --ease-smooth: cubic-bezier(.2,.8,.2,1); }

.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%); padding: 24px; position: relative; overflow: hidden; }
.auth-page::before, .auth-page::after { content: ''; position: absolute; border-radius: 50%; filter: blur(30px); opacity: .18; pointer-events: none; }
.auth-page::before { width: 420px; height: 420px; top: -120px; left: -120px; background: radial-gradient(circle at 30% 30%, #34d399, transparent 60%); }
.auth-page::after  { width: 520px; height: 520px; right: -160px; bottom: -160px; background: radial-gradient(circle at 70% 70%, #a7f3d0, transparent 60%); }

.auth-page.enter { animation: slideUp .5s var(--ease-smooth) both; }
.auth-card { width: 100%; max-width: 380px; border: 1px solid rgba(16,185,129,.16); border-radius: 16px; box-shadow: 0 12px 28px rgba(16,185,129,.12), 0 6px 14px rgba(0,0,0,.06); transition: box-shadow .3s var(--ease-smooth); position: relative; }
/* 取消悬停时 body 视觉移动：不再整体上浮 */
.auth-card:hover { box-shadow: 0 16px 32px rgba(16,185,129,.14), 0 8px 18px rgba(0,0,0,.08); }

/* Header visuals */
.card-head { display: flex; align-items: center; gap: 12px; margin: 8px 8px 4px; padding: 8px; border-radius: 12px; background: linear-gradient(180deg, rgba(16,185,129,.06), rgba(16,185,129,.03)); }
.emblem { width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center; background: linear-gradient(135deg, #10b981, #34d399); color: #fff; box-shadow: 0 8px 18px rgba(16,185,129,.25); }
.emblem-icon { font-size: 22px; }
.head-text { display: flex; flex-direction: column; }
.head-title { margin: 0; font-size: 18px; font-weight: 700; color: #065f46; }
.head-sub { margin: 2px 0 0; font-size: 12px; color: #047857; opacity: .8; }

.tabs { display: flex; justify-content: center; margin-bottom: 16px; }
.form { margin-top: 8px; }
.actions:deep(.el-form-item__content) { display: flex; justify-content: center; gap: 14px; width: 100%; }

/* 角色二选一按钮 */
.role-toggle { display: inline-flex; gap: 10px; }
.role-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 999px; border: 1px solid rgba(16,185,129,.22); background: #fff; color: #065f46; transition: transform .18s var(--ease-smooth), box-shadow .18s var(--ease-smooth), border-color .18s var(--ease-smooth); }
.role-btn .i { margin-right: 2px; }
.role-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 14px rgba(16,185,129,.16); }
.role-btn.active { background: linear-gradient(135deg,#10b981,#34d399); color: #fff; border-color: transparent; box-shadow: 0 8px 16px rgba(16,185,129,.22); }

/* Input focus look */
.form :deep(.el-input__wrapper) { border-radius: 12px; transition: box-shadow .24s var(--ease-smooth), transform .24s var(--ease-smooth); }
.form :deep(.el-input__wrapper.is-focus), .form :deep(.el-input.is-focus .el-input__wrapper) { box-shadow: 0 0 0 3px rgba(16,185,129,.15) inset, 0 0 0 2px rgba(16,185,129,.18); transform: translateZ(0); }
.ipfx { color: rgba(6,95,70,.8); }

/* Primary button width/color transitions */
.primary-btn { border: none !important; background-image: linear-gradient(135deg, #10b981, #34d399); color: #fff; border-radius: 999px; padding: 0 22px; height: 44px; font-weight: 700; letter-spacing: .2px; box-shadow: 0 6px 14px rgba(16,185,129,.22); transition: transform .18s var(--ease-smooth), box-shadow .18s var(--ease-smooth), opacity .2s, width .28s var(--ease-smooth), background-color .28s var(--ease-smooth), background-image .28s var(--ease-smooth); width: 100%; }
.primary-btn:hover { transform: translateY(-1px); box-shadow: 0 10px 20px rgba(16,185,129,.26); }
.primary-btn:active { transform: translateY(0); box-shadow: 0 6px 14px rgba(16,185,129,.22); }
.primary-btn.loading { width: 140px; }
.primary-btn.success { background-image: none; background-color: #22c55e; width: 100%; }
.primary-btn.error { background-image: none; background-color: #ef4444; width: 100%; }

/* Spinner */
.spinner { display: inline-flex; align-items: center; gap: 6px; }
.spin { animation: tgs 0.9s linear infinite; }
@keyframes tgs { to { transform: rotate(360deg); } }

@keyframes slideUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
.fadeOut { from { opacity: 1; transform: scale(1); filter: blur(0); } to { opacity: 0; transform: scale(.98); filter: blur(2px); } }
.switch-br { position: absolute; right: 16px; bottom: 12px; }
.submit_link { font-size: 12px; }

.fade-enter-active, .fade-leave-active { transition: opacity .2s var(--ease-smooth); }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 弹性超调的图标过渡（更贴近 Telegram 手感） */
.scaleFade-enter-active { animation: elasticIn .28s cubic-bezier(.2,1.2,.2,1) both; }
.scaleFade-leave-active { animation: elasticOut .18s var(--ease-smooth) both; }
.scaleFade-enter-from, .scaleFade-leave-to { opacity: 0; }
@keyframes elasticIn {
  0%   { opacity: 0; transform: scale(.92); }
  60%  { opacity: 1; transform: scale(1.06); }
  100% { opacity: 1; transform: scale(1); }
}
@keyframes elasticOut {
  0%   { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(.95); }
}

.success, .error { display: inline-flex; align-items: center; }
.big-icon { font-size: 18px; width: 18px; height: 18px; }

/* Error shake and red focus ring */
.form.error-shake { animation: shake .42s var(--ease-smooth); }
@keyframes shake { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-6px); } 40% { transform: translateX(6px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(4px); } }
.form :deep(.is-error .el-input__wrapper) { box-shadow: 0 0 0 3px rgba(239,68,68,.18) inset, 0 0 0 2px rgba(239,68,68,.22); }
</style>
