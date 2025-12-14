<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
      enter-to-class="opacity-100 translate-y-0 sm:scale-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100 translate-y-0 sm:scale-100"
      leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
    >
      <div
        v-if="visible"
        class="fixed inset-0 z-[9999] flex items-start justify-center px-4 pt-[25vh] pointer-events-none"
      >
        <div
          :class="[
            'pointer-events-auto max-w-md w-full rounded-lg shadow-xl p-4 flex items-start gap-3',
            typeClass
          ]"
          role="alert"
        >
          <!-- Icon -->
          <div class="flex-shrink-0">
            <span :class="['material-symbols-outlined text-2xl', iconColorClass]">
              {{ icon }}
            </span>
          </div>

          <!-- Content -->
          <div class="flex-1 pt-0.5">
            <h3 v-if="title" :class="['text-sm font-semibold mb-1', titleColorClass]">
              {{ title }}
            </h3>
            <p :class="['text-sm', messageColorClass]">
              {{ message }}
            </p>
          </div>

          <!-- Close Button -->
          <button
            v-if="closable"
            type="button"
            :class="['flex-shrink-0 rounded-lg p-1 hover:bg-black/5 dark:hover:bg-white/5 transition-colors', closeButtonColorClass]"
            @click="close"
          >
            <span class="material-symbols-outlined text-base">close</span>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

const props = withDefaults(
  defineProps<{
    visible: boolean
    type?: ToastType
    title?: string
    message: string
    closable?: boolean
  }>(),
  {
    type: 'info',
    closable: true
  }
)

const emit = defineEmits<{
  close: []
}>()

const icon = computed(() => {
  switch (props.type) {
    case 'success':
      return 'check_circle'
    case 'error':
      return 'error'
    case 'warning':
      return 'warning'
    case 'info':
    default:
      return 'info'
  }
})

const typeClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
    case 'error':
      return 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
    case 'warning':
      return 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800'
    case 'info':
    default:
      return 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
  }
})

const iconColorClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-600 dark:text-green-400'
    case 'error':
      return 'text-red-600 dark:text-red-400'
    case 'warning':
      return 'text-yellow-600 dark:text-yellow-400'
    case 'info':
    default:
      return 'text-blue-600 dark:text-blue-400'
  }
})

const titleColorClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-900 dark:text-green-100'
    case 'error':
      return 'text-red-900 dark:text-red-100'
    case 'warning':
      return 'text-yellow-900 dark:text-yellow-100'
    case 'info':
    default:
      return 'text-blue-900 dark:text-blue-100'
  }
})

const messageColorClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-800 dark:text-green-200'
    case 'error':
      return 'text-red-800 dark:text-red-200'
    case 'warning':
      return 'text-yellow-800 dark:text-yellow-200'
    case 'info':
    default:
      return 'text-blue-800 dark:text-blue-200'
  }
})

const closeButtonColorClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-600 dark:text-green-400'
    case 'error':
      return 'text-red-600 dark:text-red-400'
    case 'warning':
      return 'text-yellow-600 dark:text-yellow-400'
    case 'info':
    default:
      return 'text-blue-600 dark:text-blue-400'
  }
})

const close = () => {
  emit('close')
}
</script>

