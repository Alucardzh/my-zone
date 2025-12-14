// 点击外部关闭的组合式函数
import { onMounted, onUnmounted, Ref } from 'vue'

export function useClickOutside(
  elementRef: Ref<HTMLElement | null>,
  callback: () => void
) {
  const handleClickOutside = (event: MouseEvent) => {
    if (elementRef.value && !elementRef.value.contains(event.target as Node)) {
      callback()
    }
  }

  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
  })

  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
}

