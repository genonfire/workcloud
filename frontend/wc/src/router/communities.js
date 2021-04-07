export default [
  {
    path: '/communities/forum',
    name: 'communities.forum',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/communities/Forum.vue')
  },
  {
    path: '/communities/f/:forum',
    name: 'communities.thread',
    redirect: '/communities/f/:forum/1'
  },
  {
    path: '/communities/f/:forum/:page',
    name: 'communities.threadPage',
    component: () => import('@/views/communities/Thread.vue')
  },
  {
    path: '/communities/f/:forum/:page/:pk',
    name: 'communities.readThread',
    component: () => import('@/views/communities/ReadThread.vue')
  },
]
