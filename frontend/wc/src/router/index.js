import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

import AccountsRoutes from '@/router/accounts'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  ...AccountsRoutes,
]

const router = new VueRouter({
  routes,
})

export default router
