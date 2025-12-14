<template>
  <div class="min-h-screen flex">
    <!-- 左侧装饰区 - 仅在大屏幕显示 -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-primary to-primary/80" />
      
      <!-- 装饰图案 -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-20 left-20 size-64 bg-white rounded-full blur-3xl" />
        <div class="absolute bottom-20 right-20 size-96 bg-white rounded-full blur-3xl" />
      </div>

      <!-- 内容 -->
      <div class="relative z-10 flex flex-col justify-center px-16 text-white">
        <div class="mb-8">
          <div class="size-20 mb-6">
            <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path 
                clip-rule="evenodd" 
                d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z" 
                fill="white" 
                fill-rule="evenodd"
                opacity="0.9"
              />
              <path 
                clip-rule="evenodd" 
                d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z" 
                fill="white" 
                fill-rule="evenodd"
                opacity="0.9"
              />
            </svg>
          </div>
          <h1 class="text-4xl font-bold mb-4">麦粽</h1>
          <p class="text-lg text-white/80">
            您的个人导航页<br />
            收藏和管理您最喜欢的网站
          </p>
        </div>

        <!-- 特性列表 -->
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-2xl">check_circle</span>
            <span>快速访问常用网站</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-2xl">check_circle</span>
            <span>智能分类管理</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-2xl">check_circle</span>
            <span>支持深色模式</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-2xl">check_circle</span>
            <span>多设备同步</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="flex-1 flex items-center justify-center bg-background-light dark:bg-background-dark px-4 py-12">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
// 这是一个可选的增强版布局组件
// 如果想要更丰富的登录页面效果，可以使用这个组件包裹 Login.vue 的内容
</script>

