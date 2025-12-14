<template>
  <div class="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark px-4">
    <div class="w-full max-w-md">
      <!-- Logo 和标题 -->
      <div class="text-center mb-8">
        <div class="flex justify-center mb-4">
          <!-- <div class="text-primary size-16">
            <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path 
                clip-rule="evenodd" 
                d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z" 
                fill="currentColor" 
                fill-rule="evenodd"
              />
              <path 
                clip-rule="evenodd" 
                d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z" 
                fill="currentColor" 
                fill-rule="evenodd"
              />
            </svg>
          </div> -->
        </div>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">
          欢迎回来
        </h1>
        <p class="text-slate-500 dark:text-slate-400">
          登录到您的个人导航页
        </p>
      </div>

      <!-- 表单卡片 -->
      <div class="bg-white dark:bg-slate-900 rounded-xl shadow-lg border border-slate-200 dark:border-slate-800 p-8">
        <form @submit.prevent="handleSubmit">
          <!-- 用户名输入 -->
          <div class="mb-6">
            <label 
              for="username" 
              class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2"
            >
              用户名
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder-slate-500 focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="请输入用户名"
              :disabled="authStore.isLoading"
            />
          </div>

          <!-- 密码输入 -->
          <div class="mb-6">
            <label 
              for="password" 
              class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2"
            >
              密码
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder-slate-500 focus:ring-2 focus:ring-primary focus:border-transparent pr-10"
                placeholder="请输入密码"
                :disabled="authStore.isLoading"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                @click="showPassword = !showPassword"
              >
                <span class="material-symbols-outlined text-xl">
                  {{ showPassword ? 'visibility_off' : 'visibility' }}
                </span>
              </button>
            </div>
          </div>

          <!-- 错误提示 -->
          <div 
            v-if="authStore.error || validationError" 
            class="mb-6 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-sm"
          >
            {{ validationError || authStore.error }}
          </div>

          <!-- 提交按钮 -->
          <button
            type="submit"
            class="w-full bg-primary hover:bg-primary/90 text-white font-medium py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            :disabled="authStore.isLoading"
          >
            <span v-if="authStore.isLoading" class="material-symbols-outlined animate-spin text-xl">
              progress_activity
            </span>
            <span>登录</span>
          </button>
        </form>
      </div>

      <!-- 主题切换（与MainLayout保持一致） -->
      <div class="mt-6 flex justify-center">
        <button
          class="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-200/50 text-slate-600 hover:bg-slate-200 dark:bg-slate-800/50 dark:text-slate-400 dark:hover:bg-slate-800 transition-colors text-sm"
          @click="themeStore.toggleTheme()"
        >
          <!-- Light Mode Icon -->
          <span v-if="themeStore.themeMode === 'light'" class="material-symbols-outlined text-lg">
            light_mode
          </span>
          <!-- Dark Mode Icon -->
          <span v-else-if="themeStore.themeMode === 'dark'" class="material-symbols-outlined text-lg">
            dark_mode
          </span>
          <!-- Auto Mode Icon -->
          <span v-else-if="themeStore.themeMode === 'auto'" class="material-symbols-outlined text-lg">
            auto_mode
          </span>
          
          <!-- Text Labels -->
          <span v-if="themeStore.themeMode === 'light'">浅色模式</span>
          <span v-else-if="themeStore.themeMode === 'dark'">深色模式</span>
          <span v-else-if="themeStore.themeMode === 'auto'">自动模式</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const showPassword = ref(false)
const validationError = ref<string | null>(null)

const formData = ref({
  username: '',
  password: ''
})

// 表单验证
const validateForm = (): boolean => {
  validationError.value = null

  if (formData.value.username.length < 3) {
    validationError.value = '用户名至少需要 3 个字符'
    return false
  }

  if (formData.value.password.length < 6) {
    validationError.value = '密码至少需要 6 个字符'
    return false
  }

  return true
}

// 提交表单
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  const success = await authStore.login({
    username: formData.value.username,
    password: formData.value.password
  })

  if (success) {
    // 登录成功，跳转到首页
    router.push('/')
  }
}

onMounted(() => {
  themeStore.initTheme()
  
  // 如果已登录，直接跳转到首页
  if (authStore.isAuthenticated) {
    router.push('/')
  }
})
</script>

<style scoped>
/* 自定义动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>

