<template>
  <el-container class="layout-container">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <img :src="logoImage" alt="logo" class="logo-img">
      </div>
      <div class="user-info">
        <el-avatar :size="36" class="user-avatar" :src="userAvatar">
          {{ currentStudentName ? currentStudentName.charAt(0) : 'S' }}
        </el-avatar>
        <el-dropdown @command="handleCommand" class="user-dropdown">
          <span class="dropdown-link">
            {{ currentStudentName || '学生' }}
            <el-icon><el-icon-arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <!-- 主内容区域 -->
    <el-main class="main-content">
      <router-view />
      <BottomNav v-if="!$route.meta?.hideBottomNav" />
      <AiAssistant v-if="!$route.meta?.hideAiAssistant" />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../store'
import { ElMessage, ElMessageBox } from 'element-plus'
import LogoImage from '../../assets/img/Logo.png'
import AiAssistant from '../../components/AiAssistant.vue'
import BottomNav from '../../components/BottomNav.vue'

const router = useRouter()
const userStore = useUserStore()

const currentStudentName = computed(() => {
  const user = userStore.getUserInfo
  return user ? (user.name || user.username) : ''
})

const userAvatar = ref('')
const logoImage = ref(LogoImage)

const handleCommand = async (command) => {
  if (command === 'profile') {
    router.push('/StudentSide/profile')
  } else if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      userStore.logout()
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      ElMessage.success('退出登录成功')
      router.push('/Login')
    } catch (e) {
      // 用户取消或出现错误时不做进一步处理
    }
  }
}

onMounted(() => {
  // 若刷新后 store 为空，从 localStorage 恢复
  let user = userStore.getUserInfo
  if (!user) {
    const stored = localStorage.getItem('user')
    if (stored) {
      try {
        userStore.setUserInfo(JSON.parse(stored))
      } catch (e) {
        // 恢复失败忽略
      }
    }
  }
  const token = localStorage.getItem('token')
  // if (!userStore.getUserInfo || !token) {
  //   router.push('/Login')
  // }
})
</script>

<style scoped>
.layout-container { height: 100vh; display: flex; flex-direction: column; }

.header { 
  background: #fff; border-bottom: 1px solid #e6e6e6; padding: 0 1px; 
  display: flex; align-items: center; justify-content: space-between; height: 75px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.header-left { display: flex; align-items: center; gap: 8px; }
.logo-img { margin-left: 20px; height: 60px; width: auto; object-fit: contain; cursor: pointer; transition: transform 0.15s ease; }
.logo-img:hover { transform: scale(1.05); }

.user-info { display: flex; align-items: center; gap: 12px; }
.user-avatar { border: 2px solid #e6e6e6; cursor: pointer; transition: all 0.3s ease; }
.user-avatar:hover { border-color: #409EFF; transform: scale(1.05); }
.user-dropdown { display: flex; align-items: center; }
.dropdown-link { display: flex; align-items: center; cursor: pointer; color: #333; padding: 8px 12px; border-radius: 6px; transition: all 0.3s ease; user-select: none; outline: none; }
.dropdown-link:hover { background-color: #f5f7fa; color: #409EFF; }
.dropdown-link:focus { outline: none; box-shadow: none; }

.main-content { 
  flex: 1; 
  background: rgba(245, 247, 250, 0.6); 
  backdrop-filter: blur(8px) saturate(120%);
  -webkit-backdrop-filter: blur(8px) saturate(120%);
  padding: 0px; 
  overflow: auto; 
}
</style>
