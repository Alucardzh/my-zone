// 类型定义

// 连接状态枚举
export enum ConnectionStatus {
  UNTESTED = 'untested',        // 未测试（灰色）
  CHECKING = 'checking',        // 检测中（黄色/动画）
  AVAILABLE = 'available',      // 主URL可连接（绿色）
  BACKUP_AVAILABLE = 'backup',  // 主URL不可连，备用URL可连（蓝色）
  UNAVAILABLE = 'unavailable'   // 都不可连接（红色）
}

// 网站连接检测结果
export interface WebsiteConnectionStatus {
  websiteId: number
  urlStatus: ConnectionStatus
  backUrlStatus: ConnectionStatus
  preferredUrl: 'url' | 'back_url' | null  // 优先使用的链接
  lastChecked?: Date
}

// 前端使用的网站类型
export interface Website {
  id: number
  name: string
  url: string
  back_url?: string
  icon?: string
  iconSvg?: string
  category_id?: number
  description?: string
  sort_order?: number
  connectionStatus?: WebsiteConnectionStatus  // 连接状态
}

// 前端使用的分类类型
export interface Category {
  id: number
  name: string
  icon?: string
  description?: string
  sort_order?: number
  collapsed?: boolean
}

// 用户类型
export interface User {
  id: string
  name: string
  avatar: string
  email?: string
}

