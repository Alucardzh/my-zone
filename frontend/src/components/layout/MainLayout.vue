<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar - 固定，内部可滚动 -->
    <Sidebar />

    <!-- Main Content - 独立滚动区域 -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header - 固定 -->
      <Header />

      <!-- Main Content Area - 可滚动 -->
      <main :class="[
        'flex-1 overflow-y-auto',
        uiStore.cardDisplayMode === 'mini' || uiStore.cardDisplayMode === 'aggregate'
          ? 'px-3 py-4 sm:px-4 lg:px-6' 
          : 'px-4 py-8 sm:px-6 lg:px-8'
      ]">
        <div :class="[
          'mx-auto',
          uiStore.cardDisplayMode === 'mini' || uiStore.cardDisplayMode === 'aggregate' 
            ? 'max-w-[90vw]' 
            : 'max-w-[80vw]'
        ]">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUIStore } from '@/stores/ui'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'

const uiStore = useUIStore()
</script>

