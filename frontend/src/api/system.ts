// 系统相关 API
import { getAuthHeaders } from './common'

export interface SearXNGHealthResponse {
  status: 'healthy' | 'unhealthy' | 'timeout' | 'unavailable' | 'error'
  available: boolean
  url?: string
  error?: string
}

export interface SearXNGConfigResponse {
  internal_url: string
  external_url: string
  search_path: string
}

// 检查 SearXNG 健康状态
export const checkSearXNGHealth = async (): Promise<SearXNGHealthResponse> => {
  try {
    const response = await fetch('/api/system/searxng/health', {
      headers: getAuthHeaders(),
    })

    if (!response.ok) {
      return {
        status: 'error',
        available: false,
        error: 'Failed to check SearXNG health'
      }
    }

    return response.json()
  } catch (error) {
    return {
      status: 'error',
      available: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    }
  }
}

// 获取 SearXNG 配置
export const getSearXNGConfig = async (): Promise<SearXNGConfigResponse | null> => {
  try {
    const response = await fetch('/api/system/searxng/config', {
      headers: getAuthHeaders(),
    })

    if (!response.ok) {
      return null
    }

    return response.json()
  } catch (error) {
    console.error('Failed to get SearXNG config:', error)
    return null
  }
}

