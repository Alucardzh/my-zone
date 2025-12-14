// Toast 提示管理
import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface ToastOptions {
  type?: ToastType
  title?: string
  message: string
  duration?: number
  closable?: boolean
}

export interface ConfirmOptions {
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
  type?: ToastType
}

export const useToastStore = defineStore('toast', () => {
  const visible = ref(false)
  const type = ref<ToastType>('info')
  const title = ref<string>()
  const message = ref('')
  const closable = ref(true)
  
  // 确认对话框状态
  const confirmVisible = ref(false)
  const confirmTitle = ref<string>()
  const confirmMessage = ref('')
  const confirmText = ref('确认')
  const cancelText = ref('取消')
  const confirmType = ref<ToastType>('warning')
  let confirmResolve: ((value: boolean) => void) | null = null
  
  let timeoutId: number | null = null

  const show = (options: ToastOptions) => {
    // 清除之前的定时器
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }

    // 设置新的提示
    type.value = options.type || 'info'
    title.value = options.title
    message.value = options.message
    closable.value = options.closable ?? true
    visible.value = true

    // 自动关闭
    const duration = options.duration ?? 3000
    if (duration > 0) {
      timeoutId = window.setTimeout(() => {
        close()
      }, duration)
    }
  }

  const close = () => {
    visible.value = false
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
  }

  // 便捷方法
  const success = (message: string, title?: string, duration?: number) => {
    show({ type: 'success', message, title, duration })
  }

  const error = (message: string, title?: string, duration?: number) => {
    show({ type: 'error', message, title, duration })
  }

  const warning = (message: string, title?: string, duration?: number) => {
    show({ type: 'warning', message, title, duration })
  }

  const info = (message: string, title?: string, duration?: number) => {
    show({ type: 'info', message, title, duration })
  }

  // 确认对话框方法
  const confirm = (options: ConfirmOptions): Promise<boolean> => {
    return new Promise((resolve) => {
      confirmTitle.value = options.title
      confirmMessage.value = options.message
      confirmText.value = options.confirmText || '确认'
      cancelText.value = options.cancelText || '取消'
      confirmType.value = options.type || 'warning'
      confirmVisible.value = true
      confirmResolve = resolve
    })
  }

  const handleConfirm = () => {
    confirmVisible.value = false
    if (confirmResolve) {
      confirmResolve(true)
      confirmResolve = null
    }
  }

  const handleCancel = () => {
    confirmVisible.value = false
    if (confirmResolve) {
      confirmResolve(false)
      confirmResolve = null
    }
  }

  return {
    visible,
    type,
    title,
    message,
    closable,
    show,
    close,
    success,
    error,
    warning,
    info,
    // 确认对话框
    confirmVisible,
    confirmTitle,
    confirmMessage,
    confirmText,
    cancelText,
    confirmType,
    confirm,
    handleConfirm,
    handleCancel
  }
})

