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
    path: '/communities/f/:forum/:page/:pk/:title',
    name: 'communities.readThread',
    component: () => import('@/views/communities/ReadThread.vue')
  },
  {
    path: '/communities/f/:forum/:page/write',
    name: 'communities.writeThread',
    component: () => import('@/views/communities/WriteThread.vue')
  },
  {
    path: '/communities/f/:forum/:page/edit/:pk',
    name: 'communities.editThread',
    component: () => import('@/views/communities/EditThread.vue')
  },
  {
    path: '/communities/trash/f/:forum/1',
    name: 'communities.trash',
    component: () => import('@/views/communities/Trash.vue')
  },
]
