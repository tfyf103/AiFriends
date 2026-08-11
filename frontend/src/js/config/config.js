// Runtime URL strategy.
//
// In Vite development we now use same-origin relative URLs and let vite.config.js
// proxy /api and /media to Django. This removes most beginner CORS/Cookie confusion.
// The django/cloud modes keep explicit origins for built deployments.
const platform = 'vue' // vue,django,cloud

const CONFIG_API = {
  HTTP_URL: '',
  VAD_URL: '',
}

if (platform === 'vue') {
  CONFIG_API.HTTP_URL = ''
  CONFIG_API.VAD_URL = '/vad/'
} else if (platform === 'django') {
  CONFIG_API.HTTP_URL = 'http://127.0.0.1:8000'
  CONFIG_API.VAD_URL = 'http://127.0.0.1:8000/static/frontend/vad/'
} else if (platform === 'cloud') {
  CONFIG_API.HTTP_URL = 'https://app8056.acapp.acwing.com.cn'
  CONFIG_API.VAD_URL = 'https://app8056.acapp.acwing.com.cn/static/frontend/vad/'
}

export default CONFIG_API
