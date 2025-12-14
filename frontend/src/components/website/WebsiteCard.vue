<template>
  <div class="relative group">
    <!-- Delete Button (Edit Mode) -->
    <button
      v-if="isEditMode"
      class="absolute -top-2 -right-2 z-10 flex items-center justify-center size-6 rounded-full bg-red-500 text-white hover:bg-red-600 transition-colors shadow-lg"
      @click.prevent="handleDelete"
    >
      <span class="material-symbols-outlined text-sm">close</span>
    </button>

    <component
      :is="isEditMode ? 'button' : 'button'"
      :class="[
        'w-full flex aspect-square flex-col items-center justify-center rounded-lg bg-white p-4 text-center transition-all dark:bg-slate-900 relative',
        isEditMode 
          ? 'cursor-pointer hover:ring-2 hover:ring-primary' 
          : 'hover:bg-primary/10 dark:hover:bg-primary/20'
      ]"
      @click="handleClick"
      @contextmenu="handleContextMenu"
    >
      <!-- Icon -->
      <div :class="[
        'flex size-12 items-center justify-center rounded-lg transition-colors overflow-hidden',
        isEditMode
          ? 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
          : 'bg-slate-200 text-slate-600 group-hover:bg-primary group-hover:text-white dark:bg-slate-800 dark:text-slate-400 dark:group-hover:bg-primary dark:group-hover:text-white'
      ]">
        <!-- 使用图标 API 显示图标 -->
        <img
          v-if="website.icon && !iconLoadError"
          :src="`/api/icons/${website.icon}`"
          :alt="website.name"
          class="size-8 object-contain"
          @error="iconLoadError = true"
        />
        <!-- 降级显示：使用默认图标 -->
        <span v-else class="material-symbols-outlined text-2xl">
          link
        </span>
      </div>
      
      <!-- Name -->
      <p class="mt-2 flex-1 font-medium text-slate-800 dark:text-slate-200 line-clamp-2 text-sm leading-tight break-all px-1">
        {{ website.name }}
      </p>

      <!-- Connection Status Indicator -->
      <div v-if="!isEditMode" class="absolute bottom-2 left-1/2 -translate-x-1/2">
        <ConnectionStatusIndicator :status="connectionStatus" />
      </div>

      <!-- Edit Indicator -->
      <div v-if="isEditMode" class="absolute inset-0 flex items-center justify-center bg-black/0 group-hover:bg-black/5 dark:group-hover:bg-white/5 rounded-lg transition-colors pointer-events-none">
        <span class="material-symbols-outlined text-primary opacity-0 group-hover:opacity-100 transition-opacity">
          edit
        </span>
      </div>
    </component>

    <!-- Context Menu -->
    <ContextMenu
      :visible="contextMenuVisible"
      :position="contextMenuPosition"
      :items="contextMenuItems"
      @close="closeContextMenu"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useWebsitesStore } from '@/stores/websites'
import type { Website } from '@/types'
import { ConnectionStatus } from '@/types'
import ConnectionStatusIndicator from '@/components/common/ConnectionStatusIndicator.vue'
import ContextMenu, { type ContextMenuItem } from '@/components/common/ContextMenu.vue'

const props = defineProps<{
  website: Website
  isEditMode?: boolean
}>()

const emit = defineEmits<{
  edit: [website: Website]
  delete: [websiteId: number]
}>()

const websitesStore = useWebsitesStore()
const iconLoadError = ref(false)

// 右键菜单相关
const contextMenuVisible = ref(false)
const contextMenuPosition = ref({ x: 0, y: 0 })

const contextMenuItems = computed<ContextMenuItem[]>(() => {
  const items: ContextMenuItem[] = []
  
  // 打开备用链接
  if (props.website.back_url) {
    items.push({
      label: '打开备用链接',
      icon: 'link',
      action: () => window.open(props.website.back_url, '_blank'),
      disabled: false
    })
  }
  
  // 编辑标签
  items.push({
    label: '编辑标签',
    icon: 'edit',
    action: handleEdit,
    disabled: false
  })
  
  // 删除标签
  items.push({
    label: '删除标签',
    icon: 'delete',
    action: handleDelete,
    disabled: false,
    danger: true
  })
  
  return items
})

const handleContextMenu = (e: MouseEvent) => {
  e.preventDefault()
  contextMenuPosition.value = { x: e.clientX, y: e.clientY }
  contextMenuVisible.value = true
}

const closeContextMenu = () => {
  contextMenuVisible.value = false
}

const handleEdit = () => {
  emit('edit', props.website)
}

const handleDelete = () => {
  emit('delete', props.website.id)
}

// 智能跳转：使用优先 URL
const handleClick = () => {
  if (props.isEditMode) {
    handleEdit()
  } else {
    const url = websitesStore.getPreferredUrl(props.website)
    window.open(url, '_blank')
  }
}

// 获取连接状态
const connectionStatus = computed(() => {
  return props.website.connectionStatus?.urlStatus || ConnectionStatus.UNTESTED
})
</script>

