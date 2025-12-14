<template>
  <!-- 登录页面不使用 MainLayout -->
  <MainLayout v-if="showLayout">
    <RouterView />
  </MainLayout>
  
  <!-- 登录页面直接渲染 -->
  <RouterView v-else />

  <!-- 全局 Toast 提示 -->
  <Toast
    :visible="toastStore.visible"
    :type="toastStore.type"
    :title="toastStore.title"
    :message="toastStore.message"
    :closable="toastStore.closable"
    @close="toastStore.close"
  />

  <!-- 全局确认对话框 -->
  <ConfirmDialog
    :visible="toastStore.confirmVisible"
    :type="toastStore.confirmType"
    :title="toastStore.confirmTitle"
    :message="toastStore.confirmMessage"
    :confirm-text="toastStore.confirmText"
    :cancel-text="toastStore.cancelText"
    @confirm="toastStore.handleConfirm"
    @cancel="toastStore.handleCancel"
  />
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useToastStore } from '@/stores/toast'
import MainLayout from '@/components/layout/MainLayout.vue'
import Toast from '@/components/common/Toast.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const route = useRoute()
const themeStore = useThemeStore()
const toastStore = useToastStore()

// 判断是否显示主布局（登录页不显示）
const showLayout = computed(() => route.path !== '/login')

onMounted(() => {
  themeStore.initTheme()
})
</script>

