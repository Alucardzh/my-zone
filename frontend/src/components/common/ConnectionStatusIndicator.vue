<template>
  <div
    :class="[
      'flex items-center justify-center size-2 rounded-full transition-all duration-300',
      statusClass
    ]"
    :title="statusTitle"
  >
    <div
      v-if="status === ConnectionStatus.CHECKING"
      class="size-1.5 rounded-full bg-current animate-pulse"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ConnectionStatus } from '@/types'

const props = defineProps<{
  status: ConnectionStatus
}>()

const statusClass = computed(() => {
  switch (props.status) {
    case ConnectionStatus.AVAILABLE:
      return 'bg-green-500 shadow-green-500/50 shadow-sm'
    case ConnectionStatus.BACKUP_AVAILABLE:
      return 'bg-blue-500 shadow-blue-500/50 shadow-sm'
    case ConnectionStatus.UNAVAILABLE:
      return 'bg-red-500 shadow-red-500/50 shadow-sm'
    case ConnectionStatus.CHECKING:
      return 'bg-yellow-500'
    case ConnectionStatus.UNTESTED:
    default:
      return 'bg-slate-300 dark:bg-slate-600'
  }
})

const statusTitle = computed(() => {
  switch (props.status) {
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
</script>

