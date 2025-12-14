<template>
  <div class="w-full">
    <!-- Add Category Button (Edit Mode) -->
    <div v-if="uiStore.isEditMode" :class="[
      uiStore.cardDisplayMode === 'mini' || uiStore.cardDisplayMode === 'aggregate' 
        ? 'mb-4' 
        : 'mb-6'
    ]">
      <button
        :class="[
          'flex items-center gap-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors',
          uiStore.cardDisplayMode === 'mini' || uiStore.cardDisplayMode === 'aggregate'
            ? 'px-3 py-1.5' 
            : 'px-4 py-2'
        ]"
        @click="showAddCategoryDialog = true"
      >
        <span :class="[
          'material-symbols-outlined',
          uiStore.cardDisplayMode === 'mini' || uiStore.cardDisplayMode === 'aggregate'
            ? 'text-lg' 
            : 'text-xl'
        ]">add</span>
        <span :class="[
          'font-medium',
          uiStore.cardDisplayMode === 'mini' || uiStore.cardDisplayMode === 'aggregate'
            ? 'text-sm' 
            : ''
        ]">添加分类</span>
      </button>
    </div>

    <!-- Aggregate Mode: All websites grouped by category -->
    <template v-if="uiStore.cardDisplayMode === 'aggregate'">
      <div class="flex flex-wrap gap-2">
        <template v-for="categoryGroup in aggregateCategoryGroups" :key="categoryGroup.categoryId">
          <div :class="[
            'rounded-lg p-2 inline-flex',
            getCategoryBackgroundClass(categoryGroup.categoryId)
          ]"
          style="min-width: fit-content; max-width: 100%;"
          >
            <draggable
              v-model="categoryGroup.websites"
              :disabled="!uiStore.isEditMode"
              item-key="id"
              class="flex flex-wrap gap-2"
              :animation="200"
              group="websites"
              @change="() => handleCategoryGroupUpdate(categoryGroup.categoryId, categoryGroup.websites)"
            >
              <template #item="{ element: website }">
                <div class="flex-shrink-0" style="width: 80px;">
                  <MiniWebsiteCard
                    :website="website"
                    :is-edit-mode="uiStore.isEditMode"
                    :is-aggregate-mode="true"
                    @edit="handleEditWebsite"
                    @delete="handleDeleteWebsite"
                  />
                </div>
              </template>
              <template #footer>
                <!-- Add Website Button (Edit Mode) -->
                <div v-if="uiStore.isEditMode" class="flex-shrink-0" style="width: 80px;">
                  <button
                    class="group flex aspect-square flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-300 dark:border-slate-700 hover:border-primary dark:hover:border-primary transition-all p-1.5 w-full"
                    :class="getCategoryBackgroundClass(categoryGroup.categoryId)"
                    @click="() => handleAddWebsite(categoryGroup.categoryId)"
                  >
                    <span class="material-symbols-outlined text-2xl text-slate-400 dark:text-slate-600 group-hover:text-primary">
                      add
                    </span>
                  </button>
                </div>
              </template>
            </draggable>
          </div>
        </template>
      </div>
    </template>

    <!-- Normal Mode: Website Sections -->
    <draggable
      v-else
      v-model="sortableCategories"
      :disabled="!uiStore.isEditMode"
      item-key="id"
      :class="[
        uiStore.cardDisplayMode === 'mini' ? 'space-y-6' : 'space-y-12'
      ]"
      :animation="200"
      handle=".category-drag-handle"
      @end="onCategoryDragEnd"
    >
      <template #item="{ element: category }">
        <WebsiteSection
          :category="category"
          :websites="websitesByCategory[category.id] || []"
          :is-draggable="uiStore.isEditMode"
          @add-website="handleAddWebsite"
          @edit-website="handleEditWebsite"
          @update-websites="handleUpdateWebsites"
        />
      </template>
    </draggable>

    <!-- No Results -->
    <div
      v-if="searchQuery && hasNoResults"
      class="flex flex-col items-center justify-center py-20"
    >
      <span class="material-symbols-outlined text-6xl text-slate-300 dark:text-slate-700 mb-4">
        search_off
      </span>
      <h3 class="text-xl font-semibold text-slate-600 dark:text-slate-400 mb-2">
        No results found
      </h3>
      <p class="text-slate-500 dark:text-slate-500">
        Try searching with different keywords
      </p>
    </div>

    <!-- Add Category Dialog -->
    <Teleport to="body">
      <div
        v-if="showAddCategoryDialog"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4"
      >
        <div class="bg-white dark:bg-slate-900 rounded-xl shadow-xl max-w-md w-full p-6">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4">
            添加新分类
          </h3>
          <div class="space-y-4">
            <!-- 分类名称 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                分类名称 <span class="text-red-500">*</span>
              </label>
              <input
                v-model="newCategory.name"
                type="text"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                placeholder="例如：生产力工具"
              />
            </div>
            
            <!-- 选择图标 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                选择图标（可选）
              </label>
              <IconPicker v-model="newCategory.icon" />
              <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
                不选择时默认使用 bookmark 图标
              </p>
            </div>
            
            <!-- 排序 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                排序（数字越大越靠前）
              </label>
              <input
                v-model.number="newCategory.sort_order"
                type="number"
                min="0"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                placeholder="0"
              />
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button
              type="button"
              class="flex-1 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              @click="showAddCategoryDialog = false"
            >
              取消
            </button>
            <button
              type="button"
              class="flex-1 px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!newCategory.name"
              @click="handleCreateCategory"
            >
              创建
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Add/Edit Website Dialog -->
    <Teleport to="body">
      <div
        v-if="showWebsiteDialog"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4"
      >
        <div class="bg-white dark:bg-slate-900 rounded-xl shadow-xl max-w-md w-full p-6 max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4">
            {{ editingWebsite ? '编辑网站' : '添加网站' }}
          </h3>
          <div class="space-y-4">
            <!-- 网站名称 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                网站名称 <span class="text-red-500">*</span>
              </label>
              <input
                v-model="websiteForm.name"
                type="text"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                placeholder="例如：Google"
              />
            </div>
            
            <!-- 主链接 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                网站地址 <span class="text-red-500">*</span>
              </label>
              <input
                v-model="websiteForm.url"
                type="url"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                placeholder="https://example.com"
                @blur="normalizeUrl('url')"
              />
            </div>
            
            <!-- 备用链接 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                备用链接（可选）
              </label>
              <input
                v-model="websiteForm.back_url"
                type="url"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                placeholder="https://backup.example.com"
                @blur="normalizeUrl('back_url')"
              />
              <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
                当主链接无法访问时使用
              </p>
            </div>
            
            <!-- 描述 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                描述（可选）
              </label>
              <textarea
                v-model="websiteForm.description"
                rows="2"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white resize-none"
                placeholder="简短描述这个网站..."
              />
            </div>
            
            <!-- 选择分类 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                所属分类
              </label>
              <select
                v-model="currentCategoryId"
                class="form-select w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              >
                <option :value="0">不改动</option>
                <option
                  v-for="category in websitesStore.categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>
            
            <!-- 排序 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                排序（数字越大越靠前）
              </label>
              <input
                v-model.number="websiteForm.sort_order"
                type="number"
                min="0"
                class="form-input w-full rounded-lg border-slate-300 bg-white text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                placeholder="0"
              />
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button
              type="button"
              class="flex-1 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              @click="closeWebsiteDialog"
            >
              取消
            </button>
            <button
              type="button"
              class="flex-1 px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!websiteForm.name || !websiteForm.url"
              @click="handleSaveWebsite"
            >
              {{ editingWebsite ? '保存' : '添加' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import draggable from 'vuedraggable'
import { useWebsitesStore } from '@/stores/websites'
import { useUIStore } from '@/stores/ui'
import { useToastStore } from '@/stores/toast'
import WebsiteSection from '@/components/website/WebsiteSection.vue'
import MiniWebsiteCard from '@/components/website/MiniWebsiteCard.vue'
import IconPicker from '@/components/common/IconPicker.vue'
import type { Website, Category } from '@/types'

const websitesStore = useWebsitesStore()
const uiStore = useUIStore()
const toastStore = useToastStore()

// 使用带搜索结果的分类列表，搜索时自动隐藏空分类
const categories = computed(() => websitesStore.visibleCategoriesWithResults)
const websitesByCategory = computed(() => websitesStore.websitesByCategory)
const searchQuery = computed(() => websitesStore.searchQuery)

const hasNoResults = computed(() => {
  return Object.values(websitesByCategory.value).every(
    websites => websites.length === 0
  )
})

// 聚合模式：按分类分组网站
interface CategoryGroup {
  categoryId: number
  websites: Website[]
}

const aggregateCategoryGroups = computed<CategoryGroup[]>(() => {
  const groups: CategoryGroup[] = []
  // 按分类顺序创建分组
  categories.value.forEach(category => {
    const websites = websitesByCategory.value[category.id] || []
    if (websites.length > 0 || uiStore.isEditMode) {
      groups.push({
        categoryId: category.id,
        websites: [...websites] // 创建副本以便拖拽时修改
      })
    }
  })
  return groups
})

// 获取分类背景色类（灰白间隔）
const getCategoryBackgroundClass = (categoryId?: number) => {
  if (!categoryId) return 'bg-white dark:bg-slate-900'
  
  const categoryIndex = categories.value.findIndex(cat => cat.id === categoryId)
  if (categoryIndex === -1) return 'bg-white dark:bg-slate-900'
  
  // 灰白间隔：偶数索引为白色，奇数索引为灰色
  return categoryIndex % 2 === 0
    ? 'bg-white dark:bg-slate-900'
    : 'bg-slate-50 dark:bg-slate-800'
}

// 拖拽排序相关
const sortableCategories = computed({
  get() {
    return categories.value
  },
  set(value: Category[]) {
    // 立即更新本地状态（乐观更新）
    websitesStore.categories = value
  }
})

// Category拖拽结束回调
const onCategoryDragEnd = async () => {
  // 批量更新所有分类的 sort_order
  const updates: Promise<any>[] = []
  
  categories.value.forEach((category, index) => {
    const newSortOrder = (categories.value.length - index) * 10
    if (category.sort_order !== newSortOrder) {
      updates.push(
        websitesStore.updateCategory(category.id, { sort_order: newSortOrder })
          .catch((error) => {
            console.error(`Failed to update category ${category.id}:`, error)
          })
      )
    }
  })
  
  if (updates.length > 0) {
    // 显示保存中提示
    toastStore.info('正在保存...', undefined, 1000)
    
    try {
      await Promise.all(updates)
      toastStore.success('分类顺序已保存')
    } catch (error) {
      toastStore.error('部分分类更新失败，请刷新页面')
      // 刷新数据以恢复正确状态
      await websitesStore.fetchCategories()
    }
  }
}

// 聚合模式下更新单个分类的网站顺序
const handleCategoryGroupUpdate = async (categoryId: number, websites: Website[]) => {
  const updates: Promise<any>[] = []
  
  websites.forEach((website, index) => {
    const newSortOrder = (websites.length - index) * 10
    // 检查是否需要更新（顺序变化或分类变化）
    const needsUpdate = website.sort_order !== newSortOrder || website.category_id !== categoryId
    
    if (needsUpdate) {
      updates.push(
        websitesStore.updateWebsite(website.id, {
          sort_order: newSortOrder,
          category_id: categoryId
        }).catch((error) => {
          console.error(`Failed to update website ${website.id}:`, error)
        })
      )
    }
  })
  
  if (updates.length > 0) {
    toastStore.info('正在保存...', undefined, 1000)
    try {
      await Promise.all(updates)
      toastStore.success('网站顺序已保存')
      // 刷新数据以确保所有分类的网站列表都是最新的
      await websitesStore.fetchWebsites()
    } catch (error) {
      toastStore.error('部分网站更新失败，请刷新页面')
      await websitesStore.fetchWebsites()
    }
  }
}

// Website列表更新回调（来自WebsiteSection）
const handleUpdateWebsites = async (categoryId: number, websites: Website[]) => {
  // 立即更新本地状态（乐观更新）
  const newWebsitesArray = [...websitesStore.websites]
  const updates: Promise<any>[] = []
  let hasChanges = false
  
  websites.forEach((website, index) => {
    const newSortOrder = (websites.length - index) * 10
    const needsUpdate = website.sort_order !== newSortOrder || website.category_id !== categoryId
    
    // 找到并立即更新网站
    const websiteIndex = newWebsitesArray.findIndex(w => w.id === website.id)
    if (websiteIndex !== -1) {
      newWebsitesArray[websiteIndex] = {
        ...newWebsitesArray[websiteIndex],
        sort_order: newSortOrder,
        category_id: categoryId
      }
      hasChanges = true
      
      // 如果真的有变化，准备发送请求
      if (needsUpdate) {
        updates.push(
          websitesStore.updateWebsite(website.id, {
            sort_order: newSortOrder,
            category_id: categoryId
          }).catch((error) => {
            console.error(`Failed to update website ${website.id}:`, error)
          })
        )
      }
    }
  })
  
  // 立即更新整个数组以触发响应式
  if (hasChanges) {
    websitesStore.websites = newWebsitesArray
  }
  
  // 异步保存到后端
  if (updates.length > 0) {
    // 显示保存中提示
    toastStore.info('正在保存...', undefined, 1000)
    
    try {
      await Promise.all(updates)
      toastStore.success('网站顺序已保存')
    } catch (error) {
      toastStore.error('部分网站更新失败，请刷新页面')
      // 刷新数据以恢复正确状态
      await websitesStore.fetchWebsites()
    }
  }
}

// 添加分类对话框
const showAddCategoryDialog = ref(false)
const newCategory = ref({
  name: '',
  icon: 'bookmark',
  sort_order: 0
})

// 添加/编辑网站对话框
const showWebsiteDialog = ref(false)
const editingWebsite = ref<Website | null>(null)
const currentCategoryId = ref<number>(0)
const websiteForm = ref({
  name: '',
  url: '',
  back_url: '',
  description: '',
  icon: '',
  sort_order: 0
})

// 创建分类
const handleCreateCategory = async () => {
  if (!newCategory.value.name) return

  try {
    await websitesStore.addCategory({
      name: newCategory.value.name,
      icon: newCategory.value.icon || 'bookmark', // 默认使用 bookmark 图标
      sort_order: newCategory.value.sort_order || 0
    })

    // 重置表单
    newCategory.value = { name: '', icon: 'bookmark', sort_order: 0 }
    showAddCategoryDialog.value = false
    toastStore.success('分类创建成功')
  } catch (error) {
    console.error('Failed to create category:', error)
    toastStore.error('创建分类失败', (error as Error).message)
  }
}

// 自动补全 URL 协议
const normalizeUrl = (field: 'url' | 'back_url') => {
  const value = websiteForm.value[field]
  if (!value) return
  
  // 如果不是以 http:// 或 https:// 开头，自动添加 https://
  if (!/^https?:\/\//i.test(value)) {
    websiteForm.value[field] = `https://${value}`
  }
}

// 打开添加网站对话框
const handleAddWebsite = (categoryId: number) => {
  currentCategoryId.value = categoryId
  editingWebsite.value = null
  websiteForm.value = {
    name: '',
    url: '',
    back_url: '',
    description: '',
    icon: '',
    sort_order: 0
  }
  showWebsiteDialog.value = true
}


// 打开编辑网站对话框
const handleEditWebsite = (website: Website) => {
  editingWebsite.value = website
  currentCategoryId.value = website.category_id || 0
  websiteForm.value = {
    name: website.name,
    url: website.url,
    back_url: website.back_url || '',
    description: website.description || '',
    icon: website.icon || '',
    sort_order: website.sort_order || 0
  }
  showWebsiteDialog.value = true
}

// 删除网站
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

// 保存网站
const handleSaveWebsite = async () => {
  if (!websiteForm.value.name || !websiteForm.value.url) return

  // 确保 URL 有协议
  normalizeUrl('url')
  if (websiteForm.value.back_url) {
    normalizeUrl('back_url')
  }

  try {
    if (editingWebsite.value) {
      // 更新现有网站
      await websitesStore.updateWebsite(editingWebsite.value.id, {
        name: websiteForm.value.name,
        url: websiteForm.value.url,
        back_url: websiteForm.value.back_url || undefined,
        description: websiteForm.value.description || undefined,
        icon: websiteForm.value.icon || undefined,
        category_id: currentCategoryId.value,
        sort_order: websiteForm.value.sort_order || 0
      })
    } else {
      // 添加新网站
      await websitesStore.addWebsite({
        name: websiteForm.value.name,
        url: websiteForm.value.url,
        back_url: websiteForm.value.back_url || undefined,
        description: websiteForm.value.description || undefined,
        icon: websiteForm.value.icon || undefined,
        category_id: currentCategoryId.value,
        sort_order: websiteForm.value.sort_order || 0
      })
    }

    closeWebsiteDialog()
    toastStore.success(editingWebsite.value ? '网站更新成功' : '网站添加成功')
  } catch (error) {
    console.error('Failed to save website:', error)
    toastStore.error('保存网站失败', (error as Error).message)
  }
}

// 关闭网站对话框
const closeWebsiteDialog = () => {
  showWebsiteDialog.value = false
  editingWebsite.value = null
  websiteForm.value = {
    name: '',
    url: '',
    back_url: '',
    description: '',
    icon: '',
    sort_order: 0
  }
}

onMounted(async () => {
  await websitesStore.initData()
})
</script>

