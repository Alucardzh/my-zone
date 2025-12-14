<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="visible"
        class="fixed inset-0 z-[9999] bg-black/30 dark:bg-black/50 flex items-start justify-center px-4 pt-[25vh]"
        @click.self="onCancel"
      >
        <Transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="opacity-0 translate-y-4 scale-95"
          enter-to-class="opacity-100 translate-y-0 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="opacity-100 translate-y-0 scale-100"
          leave-to-class="opacity-0 translate-y-4 scale-95"
        >
          <div
            v-if="visible"
            :class="[
              'max-w-md w-full rounded-lg shadow-xl p-6',
              typeClass
            ]"
            role="alertdialog"
          >
            <!-- Icon and Content -->
            <div class="flex items-start gap-4">
              <!-- Icon -->
              <div class="flex-shrink-0">
                <span :class="['material-symbols-outlined text-3xl', iconColorClass]">
                  {{ icon }}
                </span>
              </div>

              <!-- Content -->
              <div class="flex-1">
                <h3 v-if="title" :class="['text-lg font-semibold mb-2', titleColorClass]">
                  {{ title }}
                </h3>
                <p :class="['text-sm', messageColorClass]">
                  {{ message }}
                </p>
              </div>
            </div>

            <!-- Buttons -->
            <div class="mt-6 flex gap-3 justify-end">
              <button
                type="button"
                class="px-4 py-2 text-sm font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-700 dark:hover:bg-slate-600 dark:text-slate-200 transition-colors"
                @click="onCancel"
              >
                {{ cancelText }}
              </button>
              <button
                type="button"
                :class="[
                  'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                  confirmButtonClass
                ]"
                @click="onConfirm"
              >
                {{ confirmText }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export type ConfirmType = 'success' | 'error' | 'warning' | 'info'

const props = withDefaults(
  defineProps<{
    visible: boolean
    type?: ConfirmType
    title?: string
    message: string
    confirmText?: string
    cancelText?: string
  }>(),
  {
    type: 'warning',
    confirmText: '确认',
    cancelText: '取消'
  }
)

const emit = defineEmits<{
  confirm: []
  cancel: []
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
      return 'help'
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

const confirmButtonClass = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-600 hover:bg-green-700 text-white dark:bg-green-500 dark:hover:bg-green-600'
    case 'error':
      return 'bg-red-600 hover:bg-red-700 text-white dark:bg-red-500 dark:hover:bg-red-600'
    case 'warning':
      return 'bg-yellow-600 hover:bg-yellow-700 text-white dark:bg-yellow-500 dark:hover:bg-yellow-600'
    case 'info':
    default:
      return 'bg-blue-600 hover:bg-blue-700 text-white dark:bg-blue-500 dark:hover:bg-blue-600'
  }
})

const onConfirm = () => {
  emit('confirm')
}

const onCancel = () => {
  emit('cancel')
}
</script>

