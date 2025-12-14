import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import { useAuthStore } from './stores/auth'
import { useUIStore } from './stores/ui'
import './style.css'

// 创建路由
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresAuth: false }
    }
  ]
})

// 创建应用
const app = createApp(App)
const pinia = createPinia()

// 使用插件
app.use(pinia)
app.use(router)

// 初始化认证状态
const authStore = useAuthStore()
authStore.initAuth()

// 初始化 UI 状态
const uiStore = useUIStore()
uiStore.initUI()

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.meta.requiresAuth
  const isAuthenticated = authStore.isAuthenticated

  // 如果路由需要认证
  if (requiresAuth) {
    if (!isAuthenticated) {
      // 未登录，跳转到登录页
      next('/login')
      return
    }
    
    // 已登录，验证 token 是否有效
    try {
      // 尝试获取用户信息来验证 token
      await authStore.fetchCurrentUser()
      next()
    } catch (error) {
      // token 无效，清除认证状态并跳转到登录页
      authStore.logout()
      next('/login')
    }
  } else if (to.path === '/login' && isAuthenticated) {
    // 已登录用户访问登录页，跳转到首页
    next('/')
  } else {
    next()
  }
})

// 挂载应用
app.mount('#app')

