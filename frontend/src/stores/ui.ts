// UI 状态管理
import { defineStore } from 'pinia'
import { ref } from 'vue'

export type CardDisplayMode = 'card' | 'mini' | 'aggregate'

export const useUIStore = defineStore('ui', () => {
  const isSidebarCollapsed = ref(false)
  const isEditMode = ref(false)
  const cardDisplayMode = ref<CardDisplayMode>('card')

  // 切换侧边栏状态
  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
    // 保存到 localStorage
    localStorage.setItem('sidebarCollapsed', String(isSidebarCollapsed.value))
  }

  // 切换编辑模式
  const toggleEditMode = () => {
    isEditMode.value = !isEditMode.value
  }

  // 开启编辑模式
  const enterEditMode = () => {
    isEditMode.value = true
  }

  // 退出编辑模式
  const exitEditMode = () => {
    isEditMode.value = false
  }

  // 切换卡片显示模式：card -> mini -> aggregate -> card
  const toggleCardDisplayMode = () => {
    if (cardDisplayMode.value === 'card') {
      cardDisplayMode.value = 'mini'
    } else if (cardDisplayMode.value === 'mini') {
      cardDisplayMode.value = 'aggregate'
    } else {
      cardDisplayMode.value = 'card'
    }
    localStorage.setItem('cardDisplayMode', cardDisplayMode.value)
  }

  // 设置卡片显示模式
  const setCardDisplayMode = (mode: CardDisplayMode) => {
    cardDisplayMode.value = mode
    localStorage.setItem('cardDisplayMode', mode)
  }

  // 初始化 UI 状态
  const initUI = () => {
    const saved = localStorage.getItem('sidebarCollapsed')
    if (saved !== null) {
      isSidebarCollapsed.value = saved === 'true'
    }
    
    const savedCardMode = localStorage.getItem('cardDisplayMode') as CardDisplayMode | null
    if (savedCardMode && ['card', 'mini', 'aggregate'].includes(savedCardMode)) {
      cardDisplayMode.value = savedCardMode
    }
  }

  return {
    isSidebarCollapsed,
    isEditMode,
    cardDisplayMode,
    toggleSidebar,
    toggleEditMode,
    enterEditMode,
    exitEditMode,
    toggleCardDisplayMode,
    setCardDisplayMode,
    initUI
  }
})

