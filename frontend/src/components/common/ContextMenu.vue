<template>
  <Teleport to="body">
    <div
      v-if="visible"
      ref="menuRef"
      :style="{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        zIndex: 9999
      }"
      class="min-w-[160px] rounded-lg border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-700 dark:bg-slate-800"
      @click="handleMenuClick"
    >
      <button
        v-for="(item, index) in items"
        :key="index"
        :class="[
          'flex w-full items-center gap-3 px-4 py-2 text-left text-sm transition-colors',
          item.disabled
            ? 'cursor-not-allowed text-slate-400 dark:text-slate-500'
            : 'text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700',
          item.danger && !item.disabled
            ? 'text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20'
            : ''
        ]"
        :disabled="item.disabled"
        @click="handleItemClick(item)"
      >
        <span v-if="item.icon" class="material-symbols-outlined text-base">
          {{ item.icon }}
        </span>
        <span>{{ item.label }}</span>
      </button>
    </div>

    <!-- Overlay to close menu -->
    <div
      v-if="visible"
      class="fixed inset-0"
      style="z-index: 9998"
      @click="close"
      @contextmenu.prevent="close"
    />
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

export interface ContextMenuItem {
  label: string
  icon?: string
  action: () => void
  disabled?: boolean
  danger?: boolean
}

const props = defineProps<{
  visible: boolean
  position: { x: number; y: number }
  items: ContextMenuItem[]
}>()

const emit = defineEmits<{
  close: []
}>()

const menuRef = ref<HTMLElement | null>(null)

const handleItemClick = (item: ContextMenuItem) => {
  if (item.disabled) return
  item.action()
  close()
}

const handleMenuClick = (e: Event) => {
  e.stopPropagation()
}

const close = () => {
  emit('close')
}

// 调整菜单位置，避免超出视口
watch(() => props.visible, async (visible) => {
  if (visible) {
    await nextTick()
    if (menuRef.value) {
      const rect = menuRef.value.getBoundingClientRect()
      const viewportWidth = window.innerWidth
      const viewportHeight = window.innerHeight

      let { x, y } = props.position

      // 防止右侧溢出
      if (x + rect.width > viewportWidth) {
        x = viewportWidth - rect.width - 10
      }

      // 防止底部溢出
      if (y + rect.height > viewportHeight) {
        y = viewportHeight - rect.height - 10
      }

      // 更新位置
      if (menuRef.value) {
        menuRef.value.style.left = `${x}px`
        menuRef.value.style.top = `${y}px`
      }
    }
  }
})
</script>

