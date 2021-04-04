export default [
  {
    path: '/communities/forum',
    name: 'communities.forum',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/communities/Forum.vue')
  },
]
