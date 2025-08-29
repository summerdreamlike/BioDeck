<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <!-- 左侧：基本信息 + 账号安全 -->
      <el-col :xs="24" :md="11" :lg="10">
        <el-card class="profile-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="title">
                <el-icon><el-icon-user /></el-icon>
                <span>个人中心</span>
                <el-tag class="role-tag" :type="roleTagType" round>{{ roleText }}</el-tag>
              </div>
            </div>
          </template>

          <el-row :gutter="20">
            <el-col :span="8">
              <div class="avatar-wrap">
                <el-avatar :size="96" :src="avatarUrl">{{ initials }}</el-avatar>
                <div class="avatar-hint">（支持后续完善头像上传）</div>
              </div>
            </el-col>
            <el-col :span="16">
              <el-form :model="form" label-width="96px">
                <el-form-item label="姓名">
                  <el-input v-model="form.name" placeholder="姓名不可修改" disabled />
                </el-form-item>
                <el-form-item label="角色">
                  <el-space>
                    <el-tag :type="roleTagType" effect="dark">{{ roleText }}</el-tag>
                    <el-tag v-if="isTeacher" type="success" effect="light" round>授课教师</el-tag>
                    <el-tag v-if="isStudent" type="info" effect="light" round>在读学生</el-tag>
                  </el-space>
                </el-form-item>
                <el-form-item v-if="isTeacher" label="工号">
                  <el-input v-model="form.teacher_id" disabled />
                </el-form-item>
                <el-form-item v-if="isStudent" label="学号">
                  <el-input v-model="form.student_id" disabled />
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
      </el-col>

      <!-- 右侧：用户画像 -->
      <el-col :xs="24" :md="13" :lg="14">
        <el-card class="persona-card" shadow="hover">
          <template #header>
            <div class="persona-header">
              <div class="ph-left">
                <el-icon><el-icon-data-board /></el-icon>
                <span>用户画像</span>
                <el-tag :type="persona.badgeType" round class="role-pill">{{ persona.badgeText }}</el-tag>
              </div>
              <el-tag type="info" effect="plain">ID: {{ idText }}</el-tag>
            </div>
          </template>

          <div v-if="isStudent" class="persona-body">
            <el-row :gutter="12">
              <el-col :span="8">
                <el-card class="mini mini--progress" shadow="never">
                  <div class="mini-head">
                    <el-icon class="mini-icon mini-icon--green"><el-icon-trend-charts /></el-icon>
                    <div class="mini-title">学习进度</div>
                  </div>
                  <el-progress :percentage="72" :stroke-width="8" :status="'success'" />
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="mini mini--active" shadow="never">
                  <div class="mini-head">
                    <el-icon class="mini-icon mini-icon--blue"><el-icon-lightning /></el-icon>
                    <div class="mini-title">活跃度</div>
                  </div>
                  <el-progress :percentage="56" :stroke-width="8" />
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="mini mini--tasks" shadow="never">
                  <div class="mini-head">
                    <el-icon class="mini-icon mini-icon--orange"><el-icon-finished /></el-icon>
                    <div class="mini-title">完成任务</div>
                  </div>
                  <div class="mini-number">18</div>
                </el-card>
              </el-col>
            </el-row>
            <el-empty description="更丰富的学习画像即将到来" />
          </div>

          <div v-else-if="isTeacher" class="persona-body">
            <el-row :gutter="12">
              <el-col :span="8">
                <el-card class="mini mini--progress" shadow="never">
                  <div class="mini-head">
                    <el-icon class="mini-icon mini-icon--green"><el-icon-collection /></el-icon>
                    <div class="mini-title">授课班级</div>
                  </div>
                  <div class="mini-number">{{ teacherStats.classes }}</div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="mini mini--active" shadow="never">
                  <div class="mini-head">
                    <el-icon class="mini-icon mini-icon--blue"><el-icon-user /></el-icon>
                    <div class="mini-title">学生数量</div>
                  </div>
                  <div class="mini-number">{{ teacherStats.students }}</div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="mini mini--tasks" shadow="never">
                  <div class="mini-head">
                    <el-icon class="mini-icon mini-icon--orange"><el-icon-tickets /></el-icon>
                    <div class="mini-title">布置任务</div>
                  </div>
                  <div class="mini-number">{{ teacherStats.tasks }}</div>
                </el-card>
              </el-col>
            </el-row>
            <el-empty description="教学画像组件建设中" />
          </div>

          <div v-else>
            <el-empty description="暂无画像信息" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watchEffect } from 'vue'
import { useUserStore } from '../store'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const user = computed(() => userStore.getUserInfo)

const isTeacher = computed(() => user.value?.role === 'teacher')
const isStudent = computed(() => user.value?.role === 'student')
const roleText = computed(() => isTeacher.value ? '教师' : (isStudent.value ? '学生' : (user.value?.role || '—')))
const roleTagType = computed(() => isTeacher.value ? 'success' : (isStudent.value ? 'info' : ''))

const form = reactive({ name: '', teacher_id: '', student_id: '' })
watchEffect(() => {
  form.name = user.value?.name || ''
  form.teacher_id = user.value?.teacher_id || ''
  form.student_id = user.value?.student_id || ''
})

const initials = computed(() => (form.name || 'U').slice(0,1))
const avatarUrl = ref('')
const saving = ref(false)

// 用户画像：根据身份提供不同标志与假数据占位
const persona = computed(() => ({
  badgeText: isTeacher.value ? '教师画像' : (isStudent.value ? '学生画像' : '访客'),
  badgeType: isTeacher.value ? 'success' : (isStudent.value ? 'info' : 'warning'),
}))

const idText = computed(() => isTeacher.value ? (form.teacher_id || '—') : (isStudent.value ? (form.student_id || '—') : '—'))

const teacherStats = reactive({ classes: 2, students: 60, tasks: 12 })

function onSave() {
  saving.value = true
  setTimeout(() => {
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

/* 统一圆角与阴影，轻毛玻璃质感 */
.profile-card, .security-card, .persona-card {
  border-radius: 16px;
  box-shadow: 0 12px 28px rgba(0,0,0,.08);
  backdrop-filter: blur(8px) saturate(140%);
  -webkit-backdrop-filter: blur(8px) saturate(140%);
}
.profile-card { margin-bottom: 20px; }

.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { display: inline-flex; align-items: center; gap: 8px; font-weight: 600; }
.role-tag{ margin-left: 8px; }

.avatar-wrap { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.avatar-hint { font-size: 12px; color: #909399; }

.sec-title { font-weight: 600; }
.sec-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; }
.sec-text { display: flex; flex-direction: column; }
.sec-head { font-weight: 500; }
.sec-sub { font-size: 12px; color: #909399; }

.persona-card { min-height: 300px; }
.persona-header{ display: flex; align-items: center; justify-content: space-between; }
.persona-header .ph-left{ display: inline-flex; align-items: center; gap: 8px; font-weight: 600; }
.role-pill{ margin-left: 6px; }
.persona-body{ padding-top: 6px; }
.mini{ text-align: center; border-radius: 12px; }
.mini-title{ font-size: 12px; color: #909399; margin-bottom: 6px; }
.mini-number{ font-size: 20px; font-weight: 600; }

/* 交互反馈 */
:deep(.el-card){ transition: transform .18s ease, box-shadow .18s ease; }
:deep(.el-card):hover{ transform: translateY(-2px); box-shadow: 0 16px 36px rgba(0,0,0,.10); }
:deep(.el-button){ transition: transform .14s ease, box-shadow .14s ease; }
:deep(.el-button:hover){ transform: translateY(-1px); }

/* 合理的占比与留白 */
:deep(.el-card__body){ padding: 16px 18px; }

/* 颜色与图标强化 */
.mini-head{ display: flex; align-items: center; gap: 8px; justify-content: center; margin-bottom: 8px; }
.mini-icon{ font-size: 18px; }
.mini--progress{ background: linear-gradient(180deg, rgba(16,185,129,.10), rgba(16,185,129,.04)); }
.mini--active{ background: linear-gradient(180deg, rgba(59,130,246,.10), rgba(59,130,246,.04)); }
.mini--tasks{ background: linear-gradient(180deg, rgba(245,158,11,.12), rgba(245,158,11,.05)); }
.mini-icon--green{ color: #10b981; }
.mini-icon--blue{ color: #3b82f6; }
.mini-icon--orange{ color: #f59e0b; }

/* 进场动画 */
.persona-body :deep(.el-col){ animation: miniIn .36s ease both; }
.persona-body :deep(.el-col:nth-child(1)){ animation-delay: .02s }
.persona-body :deep(.el-col:nth-child(2)){ animation-delay: .08s }
.persona-body :deep(.el-col:nth-child(3)){ animation-delay: .14s }
@keyframes miniIn{
  from{ transform: translateY(8px); opacity: 0; }
  to{ transform: translateY(0); opacity: 1; }
}
</style>
