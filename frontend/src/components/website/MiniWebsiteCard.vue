<template>
  <div 
    ref="cardRef"
    class="relative group"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <!-- Delete Button (Edit Mode) -->
    <button
      v-if="isEditMode"
      class="absolute -top-0.5 -right-0.5 z-10 flex items-center justify-center size-3.5 rounded-full bg-red-500 text-white hover:bg-red-600 transition-colors shadow-lg"
      @click.prevent="handleDelete"
    >
      <span class="material-symbols-outlined" style="font-size: 10px;">close</span>
    </button>

    <component
      :is="isEditMode ? 'button' : 'button'"
      :class="[
        'w-full flex aspect-square flex-col items-center justify-center rounded-lg text-center transition-all relative',
        // 聚合模式下使用透明背景，其他模式使用白色背景
        props.isAggregateMode 
          ? 'bg-transparent p-1.5' 
          : 'bg-white dark:bg-slate-900 p-1.5',
        isEditMode 
          ? 'cursor-pointer hover:ring-2 hover:ring-primary' 
          : props.isAggregateMode
            ? 'hover:opacity-80'
            : 'hover:bg-primary/10 dark:hover:bg-primary/20'
      ]"
      @click="handleClick"
      @contextmenu="handleContextMenu"
    >
      <!-- Icon -->
      <div :class="[
        'flex items-center justify-center rounded-lg transition-colors overflow-hidden',
        isEditMode
          ? 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400 size-7'
          : 'bg-slate-200 text-slate-600 group-hover:bg-primary group-hover:text-white dark:bg-slate-800 dark:text-slate-400 dark:group-hover:bg-primary dark:group-hover:text-white size-7'
      ]">
        <!-- 使用图标 API 显示图标 -->
        <img
          v-if="website.icon && !iconLoadError"
          :src="`/api/icons/${website.icon}`"
          :alt="website.name"
          class="size-5 object-contain"
          @error="iconLoadError = true"
        />
        <!-- 降级显示：使用默认图标 -->
        <span v-else class="material-symbols-outlined text-base">
          link
        </span>
      </div>

      <!-- Edit Indicator -->
      <div v-if="isEditMode" class="absolute inset-0 flex items-center justify-center bg-black/0 group-hover:bg-black/5 dark:group-hover:bg-white/5 rounded-lg transition-colors pointer-events-none">
        <span class="material-symbols-outlined text-primary opacity-0 group-hover:opacity-100 transition-opacity" style="font-size: 14px;">
          edit
        </span>
      </div>
    </component>

    <!-- Tooltip -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-1"
      >
        <div
          v-if="showTooltip && tooltipPosition"
          ref="tooltipRef"
          :style="{
            position: 'fixed',
            left: `${tooltipPosition.x}px`,
            top: `${tooltipPosition.y}px`,
            zIndex: 10000
          }"
          :class="[
            'px-3 py-2 rounded-lg bg-slate-900 dark:bg-slate-700 text-white text-xs whitespace-nowrap shadow-lg pointer-events-none transform -translate-x-1/2',
            tooltipPosition.showAbove ? '-translate-y-full -mb-2' : 'mt-2'
          ]"
        >
          <!-- 网站名称 -->
          <div class="font-medium mb-1">
            {{ website.name }}
          </div>
          <!-- 连接状态 -->
          <div class="text-slate-300 dark:text-slate-400">
            {{ connectionStatusText }}
          </div>
          <!-- 箭头 -->
          <div :class="[
            'absolute left-1/2 -translate-x-1/2',
            tooltipPosition.showAbove 
              ? 'top-full -mt-1' 
              : 'bottom-full -mb-1'
          ]">
            <div class="size-2 rotate-45 bg-slate-900 dark:bg-slate-700"></div>
          </div>
        </div>
      </Transition>
    </Teleport>

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
import { ref, computed, nextTick } from 'vue'
import { useWebsitesStore } from '@/stores/websites'
import type { Website } from '@/types'
import { ConnectionStatus } from '@/types'
import ContextMenu, { type ContextMenuItem } from '@/components/common/ContextMenu.vue'

const props = defineProps<{
  website: Website
  isEditMode?: boolean
  isAggregateMode?: boolean
}>()

const emit = defineEmits<{
  edit: [website: Website]
  delete: [websiteId: number]
}>()

const websitesStore = useWebsitesStore()
const iconLoadError = ref(false)
const showTooltip = ref(false)
const cardRef = ref<HTMLElement | null>(null)
const tooltipRef = ref<HTMLElement | null>(null)
const tooltipPosition = ref<{ x: number; y: number; showAbove: boolean } | null>(null)

// 获取连接状态
const connectionStatus = computed(() => {
  return props.website.connectionStatus?.urlStatus || ConnectionStatus.UNTESTED
})

// 连接状态文本
const connectionStatusText = computed(() => {
  switch (connectionStatus.value) {
    case ConnectionStatus.AVAILABLE:
      return '主链接可连接'
    case ConnectionStatus.BACKUP_AVAILABLE:
      return '备用链接可连接'
    case ConnectionStatus.UNAVAILABLE:
      return '不可连接'
    case ConnectionStatus.CHECKING:
      return '检测中...'
    case ConnectionStatus.UNTESTED:
    default:
      return '未测试'
  }
})

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

// 计算 tooltip 位置
const updateTooltipPosition = async () => {
  if (!cardRef.value) return
  
  await nextTick()
  const rect = cardRef.value.getBoundingClientRect()
  let x = rect.left + rect.width / 2
  let y = rect.top
  let showAbove = true
  
  // 调整位置，避免超出视口
  if (tooltipRef.value) {
    await nextTick()
    const tooltipRect = tooltipRef.value.getBoundingClientRect()
    const tooltipHeight = tooltipRect.height || 60 // 估算高度
    const spaceAbove = rect.top
    const spaceBelow = window.innerHeight - rect.bottom
    
    // 如果上方空间不足，显示在下方
    if (spaceAbove < tooltipHeight + 10 && spaceBelow > spaceAbove) {
      y = rect.bottom
      showAbove = false
    }
    
    // 防止左侧溢出
    if (x - tooltipRect.width / 2 < 10) {
      x = tooltipRect.width / 2 + 10
    }
    // 防止右侧溢出
    if (x + tooltipRect.width / 2 > window.innerWidth - 10) {
      x = window.innerWidth - tooltipRect.width / 2 - 10
    }
  }
  
  tooltipPosition.value = { x, y, showAbove }
}

// 鼠标进入
const handleMouseEnter = async () => {
  showTooltip.value = true
  await updateTooltipPosition()
}

// 鼠标离开
const handleMouseLeave = () => {
  showTooltip.value = false
  tooltipPosition.value = null
}
</script>

