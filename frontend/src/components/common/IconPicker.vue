<template>
  <div class="icon-picker">
    <!-- 当前选中的图标 -->
    <div class="selected-icon-display">
      <button
        type="button"
        class="flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-primary transition-colors w-full"
        @click="showPicker = !showPicker"
      >
        <span v-if="modelValue" class="material-symbols-outlined text-2xl text-primary">
          {{ modelValue }}
        </span>
        <span class="flex-1 text-left text-slate-700 dark:text-slate-300">
          {{ modelValue || '点击选择图标' }}
        </span>
        <span class="material-symbols-outlined text-slate-400">
          {{ showPicker ? 'expand_less' : 'expand_more' }}
        </span>
      </button>
    </div>

    <!-- 图标选择器弹出层 -->
    <Teleport to="body">
      <div
        v-if="showPicker"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4"
        @click.self="showPicker = false"
      >
        <div class="bg-white dark:bg-slate-900 rounded-xl shadow-xl max-w-2xl w-full p-6 max-h-[80vh] flex flex-col">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">
              选择图标
            </h3>
            <button
              type="button"
              class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              @click="showPicker = false"
            >
              <span class="material-symbols-outlined text-2xl">close</span>
            </button>
          </div>

          <!-- 搜索框 -->
          <div class="mb-4">
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                search
              </span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索图标..."
                class="form-input w-full rounded-lg border-slate-300 bg-white pl-10 text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder-slate-500"
              />
            </div>
          </div>

          <!-- 分类标签 -->
          <div class="flex gap-2 mb-4 overflow-x-auto pb-2">
            <button
              v-for="cat in categories"
              :key="cat"
              type="button"
              :class="[
                'px-3 py-1 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
                selectedCategory === cat
                  ? 'bg-primary text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
              ]"
              @click="selectedCategory = cat"
            >
              {{ cat }}
            </button>
          </div>

          <!-- 图标网格 -->
          <div class="flex-1 overflow-y-auto">
            <div class="grid grid-cols-6 sm:grid-cols-8 md:grid-cols-10 gap-2">
              <button
                v-for="icon in filteredIcons"
                :key="icon"
                type="button"
                :class="[
                  'aspect-square flex flex-col items-center justify-center p-2 rounded-lg transition-all',
                  modelValue === icon
                    ? 'bg-primary text-white'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 hover:scale-110'
                ]"
                :title="icon"
                @click="selectIcon(icon)"
              >
                <span class="material-symbols-outlined text-2xl">{{ icon }}</span>
                <span class="text-xs mt-1 truncate w-full text-center">{{ icon }}</span>
              </button>
            </div>
            
            <!-- 空状态 -->
            <div
              v-if="filteredIcons.length === 0"
              class="flex flex-col items-center justify-center py-12 text-slate-400"
            >
              <span class="material-symbols-outlined text-5xl mb-2">search_off</span>
              <p class="text-sm">未找到匹配的图标</p>
            </div>
          </div>

          <!-- 底部信息 -->
          <div class="mt-4 text-sm text-slate-500 dark:text-slate-400 text-center">
            共 {{ filteredIcons.length }} 个图标
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  modelValue?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const showPicker = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('全部')

// 图标分类
const categories = ['全部', '常用', '操作', '箭头', '文件', '设备', '社交', '其他']

// Material Symbols 常用图标列表
const iconList = {
  常用: [
    'home', 'star', 'favorite', 'settings', 'search', 'menu', 'close',
    'check', 'add', 'remove', 'edit', 'delete', 'refresh', 'more_vert',
    'more_horiz', 'notifications', 'person', 'lock', 'logout', 'login'
  ],
  操作: [
    'add', 'remove', 'edit', 'delete', 'save', 'cancel', 'done', 'close',
    'refresh', 'undo', 'redo', 'copy', 'paste', 'cut', 'download', 'upload',
    'share', 'print', 'visibility', 'visibility_off', 'check_circle', 'error'
  ],
  箭头: [
    'arrow_forward', 'arrow_back', 'arrow_upward', 'arrow_downward',
    'expand_more', 'expand_less', 'chevron_left', 'chevron_right',
    'first_page', 'last_page', 'navigate_next', 'navigate_before',
    'arrow_drop_down', 'arrow_drop_up', 'arrow_right', 'arrow_left'
  ],
  文件: [
    'folder', 'folder_open', 'insert_drive_file', 'description', 'article',
    'note', 'task', 'assignment', 'cloud_upload', 'cloud_download',
    'attach_file', 'link', 'image', 'video_file', 'audio_file', 'picture_as_pdf'
  ],
  设备: [
    'computer', 'phone_iphone', 'tablet', 'watch', 'laptop', 'desktop_windows',
    'keyboard', 'mouse', 'headphones', 'speaker', 'tv', 'camera', 'print',
    'router', 'wifi', 'bluetooth', 'battery_full', 'battery_charging_full'
  ],
  社交: [
    'group', 'person', 'people', 'face', 'mood', 'thumb_up', 'thumb_down',
    'favorite', 'chat', 'comment', 'mail', 'send', 'share', 'public',
    'language', 'forum', 'campaign', 'notifications'
  ],
  工作: [
    'work', 'business', 'cases', 'event', 'schedule', 'today', 'date_range',
    'alarm', 'timer', 'hourglass', 'pending', 'done_all', 'assignment_turned_in',
    'grading', 'analytics', 'trending_up', 'trending_down', 'pie_chart', 'bar_chart'
  ],
  开发: [
    'code', 'terminal', 'bug_report', 'build', 'construction', 'science',
    'developer_mode', 'integration_instructions', 'api', 'webhook', 'storage',
    'database', 'cloud', 'memory', 'dns', 'vpn_key', 'security'
  ],
  媒体: [
    'play_arrow', 'pause', 'stop', 'skip_next', 'skip_previous', 'fast_forward',
    'fast_rewind', 'volume_up', 'volume_down', 'volume_off', 'mic', 'mic_off',
    'videocam', 'videocam_off', 'photo_camera', 'image', 'movie', 'music_note'
  ],
  购物: [
    'shopping_cart', 'shopping_bag', 'store', 'storefront', 'local_mall',
    'add_shopping_cart', 'remove_shopping_cart', 'payment', 'credit_card',
    'local_offer', 'loyalty', 'redeem', 'card_giftcard', 'sell'
  ],
  导航: [
    'home', 'explore', 'place', 'map', 'navigation', 'directions', 'pin_drop',
    'my_location', 'location_on', 'near_me', 'compass_calibration', 'route',
    'trip_origin', 'local_shipping', 'flight', 'train', 'directions_car'
  ],
  其他: [
    'account_circle', 'dashboard', 'bookmark', 'label', 'language', 'help',
    'info', 'lightbulb', 'palette', 'style', 'widgets', 'extension', 'apps',
    'category', 'emoji_objects', 'sports_esports', 'fitness_center', 'restaurant'
  ]
}

// 获取所有图标
const allIcons = computed(() => {
  const icons = new Set<string>()
  Object.values(iconList).forEach(list => {
    list.forEach(icon => icons.add(icon))
  })
  return Array.from(icons).sort()
})

// 过滤图标
const filteredIcons = computed(() => {
  let icons = selectedCategory.value === '全部' 
    ? allIcons.value 
    : iconList[selectedCategory.value as keyof typeof iconList] || []

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    icons = icons.filter(icon => icon.toLowerCase().includes(query))
  }

  return icons
})

// 选择图标
const selectIcon = (icon: string) => {
  emit('update:modelValue', icon)
  showPicker.value = false
  searchQuery.value = ''
}
</script>

<style scoped>
/* 自定义滚动条 */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.5);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.7);
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(71, 85, 105, 0.5);
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(71, 85, 105, 0.7);
}
</style>

