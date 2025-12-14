// 认证状态管理
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

interface LoginPayload {
  username: string
  password: string
}

interface TokenResponse {
  access_token: string
  token_type?: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 是否已登录
  const isAuthenticated = computed(() => !!token.value)

  // 初始化认证状态（从 localStorage 恢复）
  const initAuth = () => {
    const savedToken = localStorage.getItem('access_token')
    if (savedToken) {
      token.value = savedToken
      // 自动获取用户信息
      fetchCurrentUser()
    }
  }

  // 登录
  const login = async (payload: LoginPayload) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '登录失败')
      }

      const data: TokenResponse = await response.json()
      token.value = data.access_token
      localStorage.setItem('access_token', data.access_token)

      // 获取用户信息
      await fetchCurrentUser()
      
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : '登录失败'
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 获取当前用户信息
  const fetchCurrentUser = async () => {
    if (!token.value) {
      throw new Error('No token available')
    }

    try {
      const { getCurrentUserApi } = await import('@/api/auth')
      const data = await getCurrentUserApi()
      
      user.value = {
        id: data.id,
        name: data.username,
        avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(data.username)}&background=1173d4&color=fff`,
        email: data.email
      }
    } catch (err) {
      console.error('Failed to fetch user:', err)
      // 如果获取用户信息失败，清除 token
      logout()
      throw err
    }
  }

  // 登出
  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
  }

  // 清除错误
  const clearError = () => {
    error.value = null
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    initAuth,
    login,
    logout,
    fetchCurrentUser,
    clearError
  }
})

