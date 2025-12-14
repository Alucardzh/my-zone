// 网站相关 API
import { getAuthHeaders } from './common'

export interface WebsiteResponse {
  id: number
  name: string
  url: string
  back_url?: string
  description?: string
  sort_order: number
  category_id?: number
  icon?: string
}

export interface WebsiteCreatePayload {
  name: string
  url: string
  back_url?: string
  description?: string
  category_id?: number
  sort_order?: number
  icon?: string
}

export interface WebsiteUpdatePayload {
  name?: string
  url?: string
  back_url?: string
  description?: string
  category_id?: number
  sort_order?: number
  icon?: string
}

export interface WebsiteListParams {
  q?: string
  category_id?: number
}

// 获取网站列表
export const getWebsitesApi = async (params?: WebsiteListParams): Promise<WebsiteResponse[]> => {
  const queryParams = new URLSearchParams()
  if (params?.q) queryParams.append('q', params.q)
  if (params?.category_id) queryParams.append('category_id', params.category_id.toString())

  const url = `/api/websites/${queryParams.toString() ? '?' + queryParams.toString() : ''}`
  const response = await fetch(url, {
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('认证已过期，请重新登录')
    }
    throw new Error('获取网站列表失败')
  }

  return response.json()
}

// 创建网站
export const createWebsiteApi = async (payload: WebsiteCreatePayload): Promise<WebsiteResponse> => {
  const response = await fetch('/api/websites/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '创建网站失败')
  }

  return response.json()
}

// 更新网站
export const updateWebsiteApi = async (
  websiteId: number,
  payload: WebsiteUpdatePayload
): Promise<WebsiteResponse> => {
  const response = await fetch(`/api/websites/${websiteId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '更新网站失败')
  }

  return response.json()
}

// 删除网站
export const deleteWebsiteApi = async (websiteId: number): Promise<void> => {
  const response = await fetch(`/api/websites/${websiteId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '删除网站失败')
  }
}

// 导出收藏数据
export const dumpWebsitesApi = async (): Promise<Blob> => {
  const token = localStorage.getItem('access_token')
  const headers: Record<string, string> = {}
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const response = await fetch('/api/data/dump', {
    method: 'POST',
    headers: headers,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '导出收藏失败')
  }

  return response.blob()
}

// 导入收藏数据
export const loadWebsitesApi = async (file: File): Promise<void> => {
  const formData = new FormData()
  formData.append('file', file)

  const token = localStorage.getItem('access_token')
  const headers: Record<string, string> = {}
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch('/api/data/load', {
    method: 'POST',
    headers,
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '导入收藏失败')
  }
}

