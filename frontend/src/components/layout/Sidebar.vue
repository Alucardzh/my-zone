<template>
  <aside 
    :class="[
      'sticky top-0 h-screen flex-shrink-0 border-r border-slate-200 dark:border-slate-800 bg-background-light dark:bg-background-dark transition-all duration-300 flex flex-col',
      uiStore.isSidebarCollapsed ? 'w-16 px-2' : 'w-64 px-4'
    ]"
  >
    <!-- Logo 和折叠按钮 - 固定在顶部 -->
    <div class="flex items-center justify-between px-2 py-6 flex-shrink-0">
      <div v-if="!uiStore.isSidebarCollapsed" class="flex items-center gap-3">
        <!-- <div class="text-primary size-7">
          <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path 
              clip-rule="evenodd" 
              d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z" 
              fill="currentColor" 
              fill-rule="evenodd"
            />
            <path 
              clip-rule="evenodd" 
              d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z" 
              fill="currentColor" 
              fill-rule="evenodd"
            />
          </svg>
        </div> -->
        <h1 class="text-lg font-bold text-slate-900 dark:text-white">麦粽</h1>
      </div>
      
      <!-- 折叠/展开按钮 -->
      <button
        class="flex items-center justify-center size-8 rounded-lg hover:bg-slate-200/50 dark:hover:bg-slate-800/50 text-slate-600 dark:text-slate-400 transition-colors"
        @click="uiStore.toggleSidebar()"
        :title="uiStore.isSidebarCollapsed ? '展开侧边栏' : '收起侧边栏'"
      >
        <span class="material-symbols-outlined text-xl">
          {{ uiStore.isSidebarCollapsed ? 'menu_open' : 'menu' }}
        </span>
      </button>
    </div>

    <!-- Navigation - 可滚动区域 -->
    <nav class="space-y-2 flex-1 overflow-y-auto px-2 py-2">
      <div
        v-for="category in websitesStore.categories"
        :key="category.id"
        class="group relative"
      >
        <a
          :href="`#category-${category.id}`"
          :class="[
            'flex items-center rounded-lg px-3 py-2 transition-colors',
            uiStore.isSidebarCollapsed ? 'justify-center' : 'gap-3',
            activeCategory === category.id
              ? 'bg-primary/10 text-primary dark:bg-primary/20'
              : 'text-slate-600 hover:bg-slate-200/50 dark:text-slate-400 dark:hover:bg-slate-800/50'
          ]"
          :title="uiStore.isSidebarCollapsed ? category.name : ''"
          @click.prevent="scrollToCategory(category.id)"
        >
          <span class="material-symbols-outlined text-xl">
            {{ category.icon || 'folder' }}
          </span>
          <span v-if="!uiStore.isSidebarCollapsed" class="flex-1 font-medium">{{ category.name }}</span>
          
          <!-- Eye Icon Toggle (visible when not collapsed) -->
          <button
            v-if="!uiStore.isSidebarCollapsed"
            :class="[
              'flex items-center justify-center size-6 rounded transition-colors opacity-0 group-hover:opacity-100',
              websitesStore.isCategoryHidden(category.id)
                ? 'text-slate-400 hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-300'
                : 'text-slate-600 hover:text-primary dark:text-slate-400 dark:hover:text-primary'
            ]"
            :title="websitesStore.isCategoryHidden(category.id) ? '显示分类' : '隐藏分类'"
            @click.prevent.stop="websitesStore.toggleCategoryVisibility(category.id)"
          >
            <span class="material-symbols-outlined text-base">
              {{ websitesStore.isCategoryHidden(category.id) ? 'visibility_off' : 'visibility' }}
            </span>
          </button>
        </a>
      </div>
    </nav>

    <!-- Theme Toggle and Card Mode Toggle - 固定在底部 -->
    <div class="flex-shrink-0 px-2 py-4 space-y-2">
      <!-- 按钮容器：并排显示 -->
      <div class="flex gap-2">
        <!-- Theme Toggle Button -->
        <button
          :class="[
            'flex items-center rounded-lg bg-slate-200/50 text-sm font-medium text-slate-600 hover:bg-slate-200 dark:bg-slate-800/50 dark:text-slate-400 dark:hover:bg-slate-800 transition-colors',
            uiStore.isSidebarCollapsed 
              ? 'flex-1 justify-center px-2 py-2' 
              : 'flex-1 justify-center gap-2 px-2 py-2 sm:px-3'
          ]"
          :title="getThemeTitle()"
          @click="themeStore.toggleTheme()"
        >
          <!-- Light Mode Icon -->
          <span v-if="themeStore.themeMode === 'light'" class="material-symbols-outlined text-xl">
            light_mode
          </span>
          <!-- Dark Mode Icon -->
          <span v-else-if="themeStore.themeMode === 'dark'" class="material-symbols-outlined text-xl">
            dark_mode
          </span>
          <!-- Auto Mode Icon -->
          <span v-else class="material-symbols-outlined text-xl">
            brightness_auto
          </span>
          
          <!-- Text Labels (隐藏在小屏幕) -->
          <span v-if="!uiStore.isSidebarCollapsed && themeStore.themeMode === 'light'" class="hidden sm:inline">
            浅色
          </span>
          <span v-else-if="!uiStore.isSidebarCollapsed && themeStore.themeMode === 'dark'" class="hidden sm:inline">
            深色
          </span>
          <span v-else-if="!uiStore.isSidebarCollapsed && themeStore.themeMode === 'auto'" class="hidden sm:inline">
            自动
          </span>
        </button>

        <!-- Card Mode Toggle Button -->
        <button
          :class="[
            'flex items-center rounded-lg bg-slate-200/50 text-sm font-medium text-slate-600 hover:bg-slate-200 dark:bg-slate-800/50 dark:text-slate-400 dark:hover:bg-slate-800 transition-colors',
            uiStore.isSidebarCollapsed 
              ? 'flex-1 justify-center px-2 py-2' 
              : 'flex-1 justify-center gap-2 px-2 py-2 sm:px-3'
          ]"
          :title="getCardModeTitle()"
          @click="uiStore.toggleCardDisplayMode()"
        >
          <!-- Card Mode Icon -->
          <span v-if="uiStore.cardDisplayMode === 'card'" class="material-symbols-outlined text-xl">
            grid_view
          </span>
          <!-- Mini Card Mode Icon -->
          <span v-else-if="uiStore.cardDisplayMode === 'mini'" class="material-symbols-outlined text-xl">
            view_compact
          </span>
          <!-- Aggregate Mode Icon -->
          <span v-else class="material-symbols-outlined text-xl">
            apps
          </span>
          
          <!-- Text Labels (隐藏在小屏幕) -->
          <span v-if="!uiStore.isSidebarCollapsed && uiStore.cardDisplayMode === 'card'" class="hidden sm:inline">
            常规
          </span>
          <span v-else-if="!uiStore.isSidebarCollapsed && uiStore.cardDisplayMode === 'mini'" class="hidden sm:inline">
            迷你
          </span>
          <span v-else-if="!uiStore.isSidebarCollapsed && uiStore.cardDisplayMode === 'aggregate'" class="hidden sm:inline">
            聚合
          </span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useWebsitesStore } from '@/stores/websites'
import { useUIStore } from '@/stores/ui'

const themeStore = useThemeStore()
const websitesStore = useWebsitesStore()
const uiStore = useUIStore()

const activeCategory = ref<number | null>(null)

const scrollToCategory = (categoryId: number) => {
  activeCategory.value = categoryId
  const element = document.getElementById(`category-${categoryId}`)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const getThemeTitle = () => {
  const modeMap = {
    light: '切换主题（当前：浅色）',
    dark: '切换主题（当前：深色）',
    auto: '切换主题（当前：自动）'
  }
  return modeMap[themeStore.themeMode]
}

const getCardModeTitle = () => {
  const modeMap = {
    card: '切换显示模式（当前：常规卡片）',
    mini: '切换显示模式（当前：迷你卡片）',
    aggregate: '切换显示模式（当前：聚合模式）'
  }
  return modeMap[uiStore.cardDisplayMode]
}

onMounted(() => {
  uiStore.initUI()
})
</script>

