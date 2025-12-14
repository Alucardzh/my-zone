// 主题状态管理
import { defineStore } from 'pinia'
import { ref, computed, watch, onMounted } from 'vue'

export type ThemeMode = 'light' | 'dark' | 'auto'

export const useThemeStore = defineStore('theme', () => {
  const themeMode = ref<ThemeMode>('auto')
  const systemPrefersDark = ref(false)

  // 计算实际是否应用深色主题
  const isDark = computed(() => {
    if (themeMode.value === 'auto') {
      return systemPrefersDark.value
    }
    return themeMode.value === 'dark'
  })

  // 监听系统主题变化
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  
  const updateSystemTheme = (e: MediaQueryList | MediaQueryListEvent) => {
    systemPrefersDark.value = e.matches
  }

  // 初始化主题
  const initTheme = () => {
    // 获取系统主题偏好
    systemPrefersDark.value = mediaQuery.matches
    
    // 监听系统主题变化
    mediaQuery.addEventListener('change', updateSystemTheme)

    // 读取保存的主题模式
    const savedMode = localStorage.getItem('themeMode') as ThemeMode | null
    if (savedMode && ['light', 'dark', 'auto'].includes(savedMode)) {
      themeMode.value = savedMode
    } else {
      themeMode.value = 'auto'
    }
    
    applyTheme()
  }

  // 应用主题
  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // 切换主题（循环：light -> dark -> auto -> light）
  const toggleTheme = () => {
    if (themeMode.value === 'light') {
      themeMode.value = 'dark'
    } else if (themeMode.value === 'dark') {
      themeMode.value = 'auto'
    } else {
      themeMode.value = 'light'
    }
    localStorage.setItem('themeMode', themeMode.value)
    applyTheme()
  }

  // 设置特定主题模式
  const setThemeMode = (mode: ThemeMode) => {
    themeMode.value = mode
    localStorage.setItem('themeMode', mode)
    applyTheme()
  }

  // 监听计算属性变化
  watch(isDark, () => {
    applyTheme()
  })

  return {
    themeMode,
    isDark,
    systemPrefersDark,
    initTheme,
    toggleTheme,
    setThemeMode
  }
})

