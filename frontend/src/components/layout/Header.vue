<template>
  <header class="flex-shrink-0 z-10 flex items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-background-light dark:bg-background-dark px-4 py-3 sm:px-6 lg:px-8">
    <!-- Search -->
    <div class="flex items-center gap-2">
      <!-- Search Mode Selector -->
      <select
        v-model="searchMode"
        class="form-select rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-900 dark:text-white text-sm py-2 pr-8"
      >
        <option value="local">本地</option>
        <option value="baidu">百度</option>
        <option v-if="searxngAvailable" value="searxng">SearXNG</option>
      </select>
      
      <!-- Search Input -->
      <div class="relative w-full max-w-xs">
        <span class="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500">
          search
        </span>
        <input
          v-model="searchQuery"
          class="form-input w-full rounded-lg border-slate-300 bg-white pl-10 text-slate-900 dark:border-slate-700 dark:bg-slate-900 dark:text-white dark:placeholder-slate-500"
          :placeholder="getSearchPlaceholder()"
          type="search"
          @keyup.enter="handleSearch"
        />
      </div>
    </div>

    <!-- User Actions -->
    <div class="flex items-center gap-4">
      <!-- Settings/Edit Mode Toggle -->
      <button
        :class="[
          'flex h-10 w-10 items-center justify-center rounded-full transition-all',
          uiStore.isEditMode
            ? 'bg-primary text-white hover:bg-primary/90'
            : 'bg-slate-200/50 text-slate-600 hover:bg-slate-200 dark:bg-slate-800/50 dark:text-slate-400 dark:hover:bg-slate-800'
        ]"
        :title="uiStore.isEditMode ? '退出编辑模式' : '进入编辑模式'"
        @click="toggleEditMode"
      >
        <span class="material-symbols-outlined text-xl">
          {{ uiStore.isEditMode ? 'done' : 'edit' }}
        </span>
      </button>
      
      <!-- User Avatar with Menu -->
      <div ref="userMenuRef" class="relative">
        <div
          class="size-10 rounded-full bg-cover bg-center cursor-pointer hover:ring-2 hover:ring-primary transition-all"
          :style="{ backgroundImage: `url(${userAvatar})` }"
          @click="toggleUserMenu"
        />
        
        <!-- User Menu Dropdown -->
        <Transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="showUserMenu"
            class="absolute right-0 mt-2 w-48 rounded-lg bg-white dark:bg-slate-900 shadow-lg border border-slate-200 dark:border-slate-800 py-1 z-50"
          >
            <div class="px-4 py-2 border-b border-slate-200 dark:border-slate-800">
              <p class="text-sm font-medium text-slate-900 dark:text-white">
                {{ authStore.user?.name || 'User' }}
              </p>
              <p class="text-xs text-slate-500 dark:text-slate-400">
                {{ authStore.user?.email || '' }}
              </p>
            </div>
            <button
              class="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-2"
              @click="handleExport"
            >
              <span class="material-symbols-outlined text-lg">download</span>
              <span>导出收藏</span>
            </button>
            <button
              class="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-2"
              @click="triggerFileInput"
            >
              <span class="material-symbols-outlined text-lg">upload</span>
              <span>导入收藏</span>
            </button>
            <button
              class="w-full px-4 py-2 text-left text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-2"
              @click="handleLogout"
            >
              <span class="material-symbols-outlined text-lg">logout</span>
              <span>退出登录</span>
            </button>
            <!-- 隐藏的文件输入框 -->
            <input
              ref="fileInputRef"
              type="file"
              accept=".json"
              class="hidden"
              @change="handleFileChange"
            />
          </div>
        </Transition>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWebsitesStore } from '@/stores/websites'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { useToastStore } from '@/stores/toast'
import { dumpWebsitesApi, loadWebsitesApi } from '@/api/websites'
import { checkSearXNGHealth, getSearXNGConfig } from '@/api/system'
import { useClickOutside } from '@/composables/useClickOutside'

const router = useRouter()
const websitesStore = useWebsitesStore()
const authStore = useAuthStore()
const uiStore = useUIStore()
const toastStore = useToastStore()

// 搜索模式：本地、百度或 SearXNG
const searchMode = ref<'local' | 'baidu' | 'searxng'>('local')

// SearXNG 可用性
const searxngAvailable = ref(false)
const searxngUrl = ref('')

// 外部搜索的独立搜索词
const externalSearchQuery = ref('')

const searchQuery = computed({
  get: () => {
    // 如果是外部搜索模式，使用独立的搜索词
    if (searchMode.value === 'baidu' || searchMode.value === 'searxng') {
      return externalSearchQuery.value
    }
    return websitesStore.searchQuery
  },
  set: (value) => {
    // 如果是外部搜索模式，设置独立的搜索词
    if (searchMode.value === 'baidu' || searchMode.value === 'searxng') {
      externalSearchQuery.value = value
    } else {
      websitesStore.searchQuery = value
    }
  }
})

// 检查 SearXNG 健康状态
const checkSearXNGAvailability = async () => {
  try {
    const health = await checkSearXNGHealth()
    searxngAvailable.value = health.available
    
    if (health.available) {
      const config = await getSearXNGConfig()
      if (config) {
        // 使用当前页面的 hostname 而不是后端返回的地址
        // 这样可以避免使用 0.0.0.0 等无法访问的地址
        const currentHost = window.location.hostname
        const protocol = window.location.protocol
        
        // 从配置中提取端口号
        const urlParts = config.external_url.match(/:(\d+)/)
        const port = urlParts ? urlParts[1] : '8080'
        
        // 构建正确的访问地址
        searxngUrl.value = `${protocol}//${currentHost}:${port}`
        
        console.log('SearXNG URL:', searxngUrl.value)
      }
    } else {
      // 如果当前选择了 SearXNG 但不可用，切换回本地
      if (searchMode.value === 'searxng') {
        searchMode.value = 'local'
      }
    }
  } catch (error) {
    console.error('Failed to check SearXNG availability:', error)
    searxngAvailable.value = false
  }
}

// 获取搜索框占位符
const getSearchPlaceholder = () => {
  switch (searchMode.value) {
    case 'local':
      return 'Search links...'
    case 'baidu':
      return '百度搜索...'
    case 'searxng':
      return 'SearXNG 搜索...'
    default:
      return 'Search...'
  }
}

// 监听搜索模式切换，清空搜索框
watch(searchMode, (newMode, oldMode) => {
  if (oldMode === 'local' && (newMode === 'baidu' || newMode === 'searxng')) {
    // 切换到外部搜索时，清空本地搜索
    websitesStore.searchQuery = ''
  } else if ((oldMode === 'baidu' || oldMode === 'searxng') && newMode === 'local') {
    // 切换到本地时，清空外部搜索
    externalSearchQuery.value = ''
  }
})

// 处理搜索（按回车键时触发）
const handleSearch = () => {
  const query = externalSearchQuery.value.trim()
  
  if (searchMode.value === 'baidu' && query) {
    // 跳转到百度搜索
    window.open(`https://www.baidu.com/s?wd=${encodeURIComponent(query)}`, '_blank')
  } else if (searchMode.value === 'searxng' && query) {
    // 跳转到 SearXNG 搜索
    if (searxngUrl.value) {
      window.open(`${searxngUrl.value}/search?q=${encodeURIComponent(query)}`, '_blank')
    }
  }
  // 本地搜索模式不需要处理，已经通过 computed 自动更新了 store
}

// 组件挂载时检查 SearXNG 可用性
onMounted(() => {
  checkSearXNGAvailability()
  
  // 每 30 秒检查一次 SearXNG 状态
  // setInterval(checkSearXNGAvailability, 30000)
})

// 用户头像
const userAvatar = computed(() => {
  return authStore.user?.avatar || 'https://ui-avatars.com/api/?name=User&background=1173d4&color=fff'
})

const showUserMenu = ref(false)
const fileInputRef = ref<HTMLInputElement>()
const userMenuRef = ref<HTMLElement | null>(null)

// 点击外部关闭用户菜单
useClickOutside(userMenuRef, () => {
  showUserMenu.value = false
})

const toggleEditMode = () => {
  uiStore.toggleEditMode()
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  await handleImport(file)
  
  // 重置 input，以便可以再次选择同一个文件
  target.value = ''
}

const handleImport = async (file: File) => {
  try {
    // 验证文件类型
    if (!file.name.endsWith('.json')) {
      toastStore.error('请选择 JSON 格式的文件')
      return
    }
    
    await loadWebsitesApi(file)
    
    toastStore.success('导入成功')
    showUserMenu.value = false
    
    // 刷新网站列表
    await websitesStore.fetchWebsites()
  } catch (error) {
    console.error('导入失败:', error)
    toastStore.error(error instanceof Error ? error.message : '导入失败')
  }
}

const handleExport = async () => {
  try {
    const blob = await dumpWebsitesApi()
    
    // 创建下载链接
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    
    // 生成文件名，包含当前日期
    const date = new Date().toISOString().split('T')[0]
    link.download = `websites_export_${date}.json`
    
    // 触发下载
    document.body.appendChild(link)
    link.click()
    
    // 清理
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    toastStore.success('导出成功')
    showUserMenu.value = false
  } catch (error) {
    console.error('导出失败:', error)
    toastStore.error(error instanceof Error ? error.message : '导出失败')
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

