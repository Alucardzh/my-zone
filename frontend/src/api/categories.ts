// 分类相关 API
import { getAuthHeaders } from './common'

export interface CategoryResponse {
  id: number
  name: string
  description?: string
  icon?: string
  sort_order: number
}

export interface CategoryCreatePayload {
  name: string
  description?: string
  icon?: string
  sort_order?: number
}

export interface CategoryUpdatePayload {
  name?: string
  description?: string
  icon?: string
  sort_order?: number
}

// 获取分类列表
export const getCategoriesApi = async (): Promise<CategoryResponse[]> => {
  const response = await fetch('/api/categories/', {
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('认证已过期，请重新登录')
    }
    throw new Error('获取分类列表失败')
  }

  return response.json()
}

// 创建分类
export const createCategoryApi = async (payload: CategoryCreatePayload): Promise<CategoryResponse> => {
  const response = await fetch('/api/categories/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '创建分类失败')
  }

  return response.json()
}

// 更新分类
export const updateCategoryApi = async (
  categoryId: number,
  payload: CategoryUpdatePayload
): Promise<CategoryResponse> => {
  const response = await fetch(`/api/categories/${categoryId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '更新分类失败')
  }

  return response.json()
}

// 删除分类
export const deleteCategoryApi = async (categoryId: number): Promise<void> => {
  const response = await fetch(`/api/categories/${categoryId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '删除分类失败')
  }
}

