import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/godisnji',
      name: 'godisnji',
      component: () => import('../views/GodisnjiView.vue'),
    },
    {
      path: '/ugovori',
      name: 'ugovori',
      component: () => import('../views/UgovoriView.vue'),
    },
  
  ],
})

export default router
