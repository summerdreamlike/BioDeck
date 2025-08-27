<template>
  <div class="profile-container">
    <el-card class="profile-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="title">
            <el-icon><el-icon-user /></el-icon>
            <span>个人中心</span>
          </div>
          <el-button type="primary" size="small" @click="onSave" :disabled="saving">{{ saving ? '保存中...' : '保存' }}</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="6">
          <div class="avatar-wrap">
            <el-avatar :size="96" :src="avatarUrl">{{ initials }}</el-avatar>
            <div class="avatar-hint">（支持后续完善头像上传）</div>
          </div>
        </el-col>
        <el-col :span="18">
          <el-form :model="form" label-width="96px">
            <el-form-item label="姓名">
              <el-input v-model="form.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="角色">
              <el-tag type="success">{{ user?.role === 'teacher' ? '教师' : user?.role }}</el-tag>
            </el-form-item>
            <el-form-item label="工号">
              <el-input v-model="form.teacher_id" disabled />
            </el-form-item>
            <el-form-item label="所属班级">
              <el-space wrap>
                <el-tag type="info">班级{{ user?.class_number ?? '—' }}</el-tag>
              </el-space>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="security-card" shadow="never">
      <template #header>
        <div class="sec-title">账号安全</div>
      </template>
      <div class="sec-item">
        <div class="sec-text">
          <div class="sec-head">登录密码</div>
          <div class="sec-sub">建议定期修改密码，保障账号安全</div>
        </div>
        <el-button size="small" @click="onChangePassword">修改</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useUserStore } from '../store'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const user = computed(() => userStore.getUserInfo)

const form = reactive({
  name: user.value?.name || '',
  teacher_id: user.value?.teacher_id || ''
})

const initials = computed(() => (form.name || 'T').slice(0,1))
const avatarUrl = ref('')
const saving = ref(false)

function onSave() {
  saving.value = true
  setTimeout(() => {
    // 本地同步展示（真实场景应调用后端保存接口）
    const merged = { ...(user.value || {}), name: form.name }
    userStore.setUserInfo(merged)
    ElMessage.success('保存成功')
    saving.value = false
  }, 500)
}

function onChangePassword() {
  ElMessage.info('密码修改功能稍后提供')
}
</script>

<style scoped>
.profile-container { padding: 20px; }
.profile-card { margin-bottom: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { display: inline-flex; align-items: center; gap: 8px; font-weight: 600; }
.avatar-wrap { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.avatar-hint { font-size: 12px; color: #909399; }
.sec-title { font-weight: 600; }
.sec-item { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; }
.sec-text { display: flex; flex-direction: column; }
.sec-head { font-weight: 500; }
.sec-sub { font-size: 12px; color: #909399; }
</style>
