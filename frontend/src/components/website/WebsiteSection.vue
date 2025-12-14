<template>
  <section :id="`category-${category.id}`">
    <!-- Section Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <!-- Drag Handle (Edit Mode) -->
        <span
          v-if="isDraggable"
          :class="[
            'category-drag-handle cursor-move material-symbols-outlined text-slate-400 dark:text-slate-600 hover:text-primary dark:hover:text-primary',
            uiStore.cardDisplayMode === 'mini' ? 'text-lg' : 'text-xl'
          ]"
          title="拖动排序"
        >
          drag_indicator
        </span>
        <!-- Category Icon -->
        <button
          v-if="uiStore.isEditMode"
          :class="[
            'flex items-center justify-center rounded-lg bg-primary/10 dark:bg-primary/20 text-primary hover:bg-primary/20 dark:hover:bg-primary/30 transition-colors',
            uiStore.cardDisplayMode === 'mini' ? 'size-8' : 'size-10'
          ]"
          :title="`修改 ${category.name} 图标`"
          @click="showIconPicker = true"
        >
          <span :class="[
            'material-symbols-outlined',
            uiStore.cardDisplayMode === 'mini' ? 'text-xl' : 'text-2xl'
          ]">{{ category.icon || 'bookmark' }}</span>
        </button>
        <span
          v-else
          :class="[
            'flex items-center justify-center rounded-lg bg-primary/10 dark:bg-primary/20 text-primary',
            uiStore.cardDisplayMode === 'mini' ? 'size-8' : 'size-10'
          ]"
        >
          <span :class="[
            'material-symbols-outlined',
            uiStore.cardDisplayMode === 'mini' ? 'text-xl' : 'text-2xl'
          ]">{{ category.icon || 'bookmark' }}</span>
        </span>
        <h3 :class="[
          'font-semibold text-slate-900 dark:text-white',
          uiStore.cardDisplayMode === 'mini' ? 'text-xl' : 'text-2xl'
        ]">
          {{ category.name }}
        </h3>
        <!-- Delete Category Button (Edit Mode) -->
        <button
          v-if="uiStore.isEditMode"
          :class="[
            'flex items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors',
            uiStore.cardDisplayMode === 'mini' ? 'size-5' : 'size-6'
          ]"
          :title="`删除 ${category.name} 分类`"
          @click="handleDeleteCategory"
        >
          <span :class="[
            'material-symbols-outlined',
            uiStore.cardDisplayMode === 'mini' ? 'text-base' : 'text-lg'
          ]">remove</span>
        </button>
      </div>
      <button
        :class="[
          'flex items-center gap-1 font-medium text-primary hover:underline',
          uiStore.cardDisplayMode === 'mini' ? 'text-xs' : 'text-sm'
        ]"
        @click="toggleCollapse"
      >
        <span :class="[
          'material-symbols-outlined',
          uiStore.cardDisplayMode === 'mini' ? 'text-base' : 'text-lg'
        ]">
          {{ isCollapsed ? 'expand_more' : 'expand_less' }}
        </span>
      </button>
    </div>

    <!-- Website Grid -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-[2000px]"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="opacity-100 max-h-[2000px]"
      leave-to-class="opacity-0 max-h-0"
    >
      <draggable
        v-show="!isCollapsed"
        v-model="sortableWebsites"
        :disabled="!isDraggable"
        item-key="id"
        :class="[
          'mt-4 grid',
          uiStore.cardDisplayMode === 'mini' ? 'gap-2' : 'gap-4'
        ]"
        :style="uiStore.cardDisplayMode === 'mini' 
          ? 'grid-template-columns: repeat(auto-fill, minmax(min(80px, 100%), 1fr));'
          : 'grid-template-columns: repeat(auto-fill, minmax(min(120px, 100%), 1fr));'"
        :animation="200"
        group="websites"
        @change="onWebsiteDragEnd"
      >
        <template #item="{ element: website }">
          <component
            :is="uiStore.cardDisplayMode === 'card' ? WebsiteCard : MiniWebsiteCard"
            :website="website"
            :is-edit-mode="uiStore.isEditMode"
            @edit="handleEditWebsite"
            @delete="handleDeleteWebsite"
          />
        </template>
        <template #footer>
          <!-- Add Website Button (Edit Mode) -->
          <button
            v-if="uiStore.isEditMode"
            :class="[
              'group flex aspect-square flex-col items-center justify-center rounded-lg bg-white dark:bg-slate-900 border-2 border-dashed border-slate-300 dark:border-slate-700 hover:border-primary dark:hover:border-primary transition-all',
              uiStore.cardDisplayMode === 'mini' ? 'p-1.5' : 'p-4'
            ]"
            @click="handleAddWebsite"
          >
            <span :class="[
              'material-symbols-outlined text-slate-400 dark:text-slate-600 group-hover:text-primary',
              uiStore.cardDisplayMode === 'mini' ? 'text-2xl' : 'text-4xl'
            ]">
              add
            </span>
            <p v-if="uiStore.cardDisplayMode !== 'mini'" class="mt-2 text-sm font-medium text-slate-500 dark:text-slate-500 group-hover:text-primary">
              添加网站
            </p>
          </button>
        </template>
      </draggable>
    </Transition>

    <!-- Empty State -->
    <div
      v-if="!isCollapsed && websites.length === 0"
      class="mt-4 flex flex-col items-center justify-center py-12 text-slate-400 dark:text-slate-600"
    >
      <span class="material-symbols-outlined text-5xl mb-2">
        folder_open
      </span>
      <p class="text-sm">No websites in this category</p>
    </div>

    <!-- Icon Picker Dialog -->
    <Teleport to="body">
      <div
        v-if="showIconPicker"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4"
        @click.self="showIconPicker = false"
      >
        <div class="bg-white dark:bg-slate-900 rounded-xl shadow-xl max-w-2xl w-full p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">
              修改分类图标 - {{ category.name }}
            </h3>
            <button
              type="button"
              class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
              @click="showIconPicker = false"
            >
              <span class="material-symbols-outlined text-2xl">close</span>
            </button>
          </div>
          
          <IconPicker v-model="selectedIcon" />
          
          <div class="flex gap-3 mt-6">
            <button
              type="button"
              class="flex-1 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              @click="showIconPicker = false"
            >
              取消
            </button>
            <button
              type="button"
              class="flex-1 px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors"
              @click="handleUpdateIcon"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import draggable from 'vuedraggable'
import { useWebsitesStore } from '@/stores/websites'
import { useUIStore } from '@/stores/ui'
import { useToastStore } from '@/stores/toast'
import WebsiteCard from './WebsiteCard.vue'
import MiniWebsiteCard from './MiniWebsiteCard.vue'
import IconPicker from '@/components/common/IconPicker.vue'
import type { Category, Website } from '@/types'

const props = defineProps<{
  category: Category
  websites: Website[]
  isDraggable?: boolean
}>()

const emit = defineEmits<{
  addWebsite: [categoryId: number]
  editWebsite: [website: Website]
  updateWebsites: [categoryId: number, websites: Website[]]
}>()

const websitesStore = useWebsitesStore()
const uiStore = useUIStore()
const toastStore = useToastStore()

// 图标选择器相关
const showIconPicker = ref(false)
const selectedIcon = ref(props.category.icon || 'bookmark')

const isCollapsed = computed(() => 
  websitesStore.isCategoryCollapsed(props.category.id)
)

const toggleCollapse = () => {
  websitesStore.toggleCategory(props.category.id)
}

// 拖拽排序相关
const sortableWebsites = computed({
  get() {
    return props.websites
  },
  set(value: Website[]) {
    // vuedraggable更新时立即通知父组件
    emit('updateWebsites', props.category.id, value)
  }
})

const onWebsiteDragEnd = () => {
  // 拖拽结束回调（v-model的set会自动触发）
}

const handleDeleteCategory = async () => {
  const confirmed = await toastStore.confirm({
    title: '删除分类',
    message: `确定要删除 "${props.category.name}" 分类吗？这将删除该分类下的所有网站。`,
    confirmText: '删除',
    cancelText: '取消',
    type: 'error'
  })
  
  if (confirmed) {
    try {
      await websitesStore.deleteCategory(props.category.id)
      toastStore.success('分类删除成功')
    } catch (error) {
      toastStore.error('删除分类失败', (error as Error).message)
    }
  }
}

const handleAddWebsite = () => {
  emit('addWebsite', props.category.id)
}

const handleEditWebsite = (website: Website) => {
  emit('editWebsite', website)
}

const handleDeleteWebsite = async (websiteId: number) => {
  const confirmed = await toastStore.confirm({
    title: '删除网站',
    message: '确定要删除这个网站吗？',
    confirmText: '删除',
    cancelText: '取消',
    type: 'error'
  })
  
  if (confirmed) {
    try {
      await websitesStore.deleteWebsite(websiteId)
      toastStore.success('网站删除成功')
    } catch (error) {
      toastStore.error('删除网站失败', (error as Error).message)
    }
  }
}

// 更新分类图标
const handleUpdateIcon = async () => {
  if (!selectedIcon.value) {
    toastStore.error('请选择一个图标')
    return
  }

  try {
    await websitesStore.updateCategory(props.category.id, {
      icon: selectedIcon.value
    })
    showIconPicker.value = false
    toastStore.success('分类图标更新成功')
  } catch (error) {
    toastStore.error('更新分类图标失败', (error as Error).message)
  }
}
</script>

