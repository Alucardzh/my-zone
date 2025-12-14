// API 通用函数

// 获取认证 header
export const getAuthHeaders = (): Record<string, string> => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  
  const token = localStorage.getItem('access_token')
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  return headers
}

// 全局 fetch 拦截器
const originalFetch = window.fetch

window.fetch = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
  // 添加认证头
  const headers = new Headers(init?.headers)
  const token = localStorage.getItem('access_token')
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  
  const modifiedInit: RequestInit = {
    ...init,
    headers
  }
  
  try {
    const response = await originalFetch(input, modifiedInit)
    
    // 处理 401 未授权错误
    if (response.status === 401) {
      // 清除本地存储的 token
      localStorage.removeItem('access_token')
      
      // 如果不在登录页面，跳转到登录页
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    
    return response
  } catch (error) {
    throw error
  }
}

// 处理 API 错误
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

// 统一的错误处理
export const handleApiError = (error: unknown): string => {
  if (error instanceof ApiError) {
    return error.message
  }
  if (error instanceof Error) {
    return error.message
  }
  return '发生未知错误'
}

