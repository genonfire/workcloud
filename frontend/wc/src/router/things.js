export default [
  {
    path: '/things/holiday',
    name: 'things.holiday',
    meta: { requiresAuth: true, StaffOnly: true },
    component: () => import('@/views/things/Holiday.vue')
  },
]
