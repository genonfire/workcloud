import { createRouter, createWebHistory } from 'vue-router'
import { nextTick } from 'vue'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'landing',
        component: () => import('@/views/Landing.vue'),
      },
      {
        path: '/home',
        name: 'home',
        component: () => import('@/views/Home.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.afterEach((to, from) => { // eslint-disable-line no-unused-vars
  if (to.meta.title) {
    nextTick(() => {
      document.title = to.meta.title
    })
  }
})

export default router
