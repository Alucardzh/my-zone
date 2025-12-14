// 认证相关 API
import { getAuthHeaders } from './common'

interface LoginPayload {
  username: string
  password: string
}

interface TokenResponse {
  access_token: string
  token_type?: string
}

interface UserResponse {
  id: string
  username: string
  email?: string
}

// 登录
export const loginApi = async (payload: LoginPayload): Promise<TokenResponse> => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '登录失败')
  }

  return response.json()
}

// 获取当前用户信息
export const getCurrentUserApi = async (): Promise<UserResponse> => {
  const response = await fetch('/api/auth/me', {
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    if (response.status === 401) {
      // 清除本地存储的 token
      localStorage.removeItem('access_token')
      throw new Error('认证已过期，请重新登录')
    }
    throw new Error('获取用户信息失败')
  }

  return response.json()
}

