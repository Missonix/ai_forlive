import Home from '@/views/Home.vue'
import type { Component } from 'vue'

export interface AIProduct {
  id: string
  name: string
  description: string
  ai_product_id: string
  component: Component
}

export const aiProducts: AIProduct[] = [
  {
    id: 'live_check',
    name: '直播话术违规词AI检测',
    description: '智能检测直播话术中的违规内容，提供优化建议',
    ai_product_id: 'AI_173c4937915142619b5da333996c5f55',
    component: Home
  },
  {
    id: 'test_product1',
    name: '直播话术AI生成',
    description: '根据商品内容生成话术',
    ai_product_id: 'test_173c49333996c5f55',
    component: Home
  }
] 