// 网站数据管理
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Website, Category } from '@/types'
import { ConnectionStatus } from '@/types'
import { 
  getCategoriesApi, 
  createCategoryApi,
  updateCategoryApi,
  deleteCategoryApi 
} from '@/api/categories'
import {
  getWebsitesApi,
  createWebsiteApi,
  updateWebsiteApi,
  deleteWebsiteApi
} from '@/api/websites'
import { handleApiError } from '@/api/common'

export const useWebsitesStore = defineStore('websites', () => {
  const websites = ref<Website[]>([])
  const categories = ref<Category[]>([])
  const collapsedCategories = ref<Set<number>>(new Set())
  const hiddenCategories = ref<Set<number>>(new Set())
  const searchQuery = ref('')
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 获取过滤后的网站列表
  const filteredWebsites = computed(() => {
    if (!searchQuery.value) return websites.value
    
    const query = searchQuery.value.toLowerCase()
    return websites.value.filter(site => 
      site.name.toLowerCase().includes(query)
    )
  })

  // 按分类分组网站
  const websitesByCategory = computed(() => {
    const grouped: Record<number, Website[]> = {}
    
    categories.value.forEach(cat => {
      grouped[cat.id] = filteredWebsites.value
        .filter(site => site.category_id === cat.id)
        .sort((a, b) => (b.sort_order || 0) - (a.sort_order || 0)) // 按sort_order降序排列
    })
    
    return grouped
  })

  // 切换分类折叠状 
  const toggleCategory = (categoryId: number) => {
    if (collapsedCategories.value.has(categoryId)) {
      collapsedCategories.value.delete(categoryId)
    } else {
      collapsedCategories.value.add(categoryId)
    }
  }

  // 检查分类是否折 
  const isCategoryCollapsed = (categoryId: number) => {
    return collapsedCategories.value.has(categoryId)
  }

  // 切换分类可见 
  const toggleCategoryVisibility = (categoryId: number) => {
    if (hiddenCategories.value.has(categoryId)) {
      hiddenCategories.value.delete(categoryId)
    } else {
      hiddenCategories.value.add(categoryId)
    }
    // 保存 localStorage
    saveCategoryVisibility()
  }

  // 判断分类是否隐藏
  const isCategoryHidden = (categoryId: number) => {
    return hiddenCategories.value.has(categoryId)
  }

  // 获取可见的分类列 
  const visibleCategories = computed(() => {
    return categories.value.filter(cat => !hiddenCategories.value.has(cat.id))
  })

  // 获取有搜索结果的可见分类列表（用于搜索时隐藏空分类）
  const visibleCategoriesWithResults = computed(() => {
    // 如果没有搜索，返回所有可见分 
    if (!searchQuery.value) {
      return visibleCategories.value
    }
    
    // 有搜索时，只返回有匹配结果的分类
    return visibleCategories.value.filter(cat => {
      const websites = websitesByCategory.value[cat.id] || []
      return websites.length > 0
    })
  })

  // 保存分类可见性到 localStorage
  const saveCategoryVisibility = () => {
    const hiddenArray = Array.from(hiddenCategories.value)
    localStorage.setItem('hiddenCategories', JSON.stringify(hiddenArray))
  }

  //  localStorage 加载分类可见 
  const loadCategoryVisibility = () => {
    try {
      const saved = localStorage.getItem('hiddenCategories')
      if (saved) {
        const hiddenArray = JSON.parse(saved) as number[]
        hiddenCategories.value = new Set(hiddenArray)
      }
    } catch (err) {
      console.error('Failed to load category visibility:', err)
    }
  }

  // 添加分类
  const addCategory = async (category: Omit<Category, 'id'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const newCategory = await createCategoryApi({
        name: category.name,
        icon: category.icon,
        description: category.description,
        sort_order: category.sort_order || 0
      })
      categories.value.push(newCategory)
      return newCategory
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // 更新分类
  const updateCategory = async (categoryId: number, updates: Partial<Category>) => {
    // 不显示全局loading，使用乐观更新
    error.value = null
    
    try {
      const updatedCategory = await updateCategoryApi(categoryId, updates)
      const index = categories.value.findIndex(cat => cat.id === categoryId)
      if (index !== -1) {
        // 合并服务器返回的数据
        categories.value[index] = { ...categories.value[index], ...updatedCategory }
      }
      return updatedCategory
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    }
  }

  // 删除分类
  const deleteCategory = async (categoryId: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await deleteCategoryApi(categoryId)
      // 删除分类下的所有网 
      websites.value = websites.value.filter(site => site.category_id !== categoryId)
      // 删除分类
      categories.value = categories.value.filter(cat => cat.id !== categoryId)
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // 添加网站
  const addWebsite = async (website: Omit<Website, 'id'>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const newWebsite = await createWebsiteApi({
        name: website.name,
        url: website.url,
        back_url: website.back_url,
        description: website.description,
        category_id: website.category_id,
        sort_order: website.sort_order || 0,
        icon: website.icon,
      })
      websites.value.push(newWebsite)
      return newWebsite
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // 更新网站
  const updateWebsite = async (websiteId: number, updates: Partial<Website>) => {
    // 不显示全局loading，使用乐观更新
    error.value = null
    
    try {
      const updatedWebsite = await updateWebsiteApi(websiteId, {
        name: updates.name,
        url: updates.url,
        back_url: updates.back_url,
        description: updates.description,
        category_id: updates.category_id,
        sort_order: updates.sort_order,
        icon: updates.icon,
      })
      
      const index = websites.value.findIndex(site => site.id === websiteId)
      if (index !== -1) {
        // 合并服务器返回的数据
        websites.value[index] = { ...websites.value[index], ...updatedWebsite }
      }
      return updatedWebsite
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    }
  }

  // 删除网站
  const deleteWebsite = async (websiteId: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await deleteWebsiteApi(websiteId)
      websites.value = websites.value.filter(site => site.id !== websiteId)
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // 加载分类数据
  const fetchCategories = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const data = await getCategoriesApi()
      categories.value = data
    } catch (err) {
      error.value = handleApiError(err)
      console.error('Failed to fetch categories:', err)
    } finally {
      isLoading.value = false
    }
  }

  // 加载网站数据
  const fetchWebsites = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const data = await getWebsitesApi()
      websites.value = data
    } catch (err) {
      error.value = handleApiError(err)
      console.error('Failed to fetch websites:', err)
    } finally {
      isLoading.value = false
    }
  }

  // 检测单 URL 的连接状 
  const checkUrlConnection = async (url: string, timeout = 3000): Promise<boolean> => {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), timeout)
    
    try {
      // 使用 HEAD 请求检测（更快 
      await fetch(url, {
        method: 'HEAD',
        mode: 'no-cors', // 避免 CORS 问题
        signal: controller.signal,
        cache: 'no-cache'
      })
      clearTimeout(timeoutId)
      return true // no-cors 模式下只要不抛错就算成功
    } catch (err) {
      clearTimeout(timeoutId)
      return false
    }
  }

  // 检测网站连接状 
  const checkWebsiteConnection = async (website: Website) => {
    const websiteIndex = websites.value.findIndex(w => w.id === website.id)
    if (websiteIndex === -1) return

    // 初始化状 
    if (!websites.value[websiteIndex].connectionStatus) {
      websites.value[websiteIndex].connectionStatus = {
        websiteId: website.id,
        urlStatus: ConnectionStatus.CHECKING,
        backUrlStatus: ConnectionStatus.UNTESTED,
        preferredUrl: null
      }
    }

    const status = websites.value[websiteIndex].connectionStatus!

    // 检测主 URL
    status.urlStatus = ConnectionStatus.CHECKING
    const urlAvailable = await checkUrlConnection(website.url)

    // 如果URL 不可用且有备URL，检测备URL
    if (!urlAvailable && website.back_url) {
      status.backUrlStatus = ConnectionStatus.CHECKING
      const backUrlAvailable = await checkUrlConnection(website.back_url)
      
      if (backUrlAvailable) {
        // 主URL不可用，备用URL可用 蓝灯
        status.urlStatus = ConnectionStatus.BACKUP_AVAILABLE
        status.backUrlStatus = ConnectionStatus.AVAILABLE
        status.preferredUrl = 'back_url'
      } else {
        // 都不可用  红灯
        status.urlStatus = ConnectionStatus.UNAVAILABLE
        status.backUrlStatus = ConnectionStatus.UNAVAILABLE
        status.preferredUrl = 'url'
      }
    } else {
      // 主URL可用  绿灯
      status.urlStatus = urlAvailable ? ConnectionStatus.AVAILABLE : ConnectionStatus.UNAVAILABLE
      status.preferredUrl = 'url'
      if (website.back_url) {
        status.backUrlStatus = ConnectionStatus.UNTESTED
      }
    }

    status.lastChecked = new Date()
  }

  // 批量检测所有网站（按排序顺序）
  const checkAllWebsitesConnection = async () => {
    //  sort_order 排序
    const sortedWebsites = [...websites.value].sort((a, b) => {
      return (b.sort_order || 0) - (a.sort_order || 0)
    })

    // 依次检测（避免并发过多）
    for (const website of sortedWebsites) {
      await checkWebsiteConnection(website)
      // 小延迟避免请求过 
      await new Promise(resolve => setTimeout(resolve, 100))
    }
  }

  // 获取网站的优先访 URL
  const getPreferredUrl = (website: Website): string => {
    if (!website.connectionStatus) {
      return website.url
    }

    const { urlStatus } = website.connectionStatus
    
    // 只有蓝灯（备用可用）时才跳转备用URL
    if (urlStatus === ConnectionStatus.BACKUP_AVAILABLE && website.back_url) {
      return website.back_url
    }
    
    // 其他所有状态都跳转主URL
    return website.url
  }

  // 初始化数据（加载分类和网站）
  const initData = async () => {
    // 先加载可见性设 
    loadCategoryVisibility()
    
    await Promise.all([
      fetchCategories(),
      fetchWebsites()
    ])

    // 等待页面完全加载后再开始检测连接状态
    const startConnectionCheck = () => {
      // 使用 requestIdleCallback 在浏览器空闲时执行，如果浏览器不支持则使用 setTimeout
      if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
          checkAllWebsitesConnection()
        }, { timeout: 2000 })
      } else {
        // 降级方案：延迟执行，确保页面渲染完成
        setTimeout(() => {
          checkAllWebsitesConnection()
        }, 1000)
      }
    }

    // 检查页面是否已经完全加载
    if (document.readyState === 'complete') {
      // 页面已完全加载，直接延迟执行
      startConnectionCheck()
    } else {
      // 等待页面完全加载
      window.addEventListener('load', startConnectionCheck, { once: true })
    }
  }

  return {
    websites,
    categories,
    searchQuery,
    isLoading,
    error,
    filteredWebsites,
    websitesByCategory,
    visibleCategories,
    visibleCategoriesWithResults,
    toggleCategory,
    isCategoryCollapsed,
    toggleCategoryVisibility,
    isCategoryHidden,
    addCategory,
    updateCategory,
    deleteCategory,
    addWebsite,
    updateWebsite,
    deleteWebsite,
    fetchCategories,
    fetchWebsites,
    initData,
    checkWebsiteConnection,
    checkAllWebsitesConnection,
    getPreferredUrl
  }
})

