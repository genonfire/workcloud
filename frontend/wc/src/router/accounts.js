export default [
  {
    path: '/accounts/signup',
    name: 'accounts.signup',
    component: () => import('@/views/accounts/Signup.vue')
  },
  {
    path: '/accounts/login',
    name: 'accounts.login',
    component: () => import('@/views/accounts/Login.vue')
  },
  {
    path: '/accounts/logout',
    name: 'accounts.logout',
    component: () => import('@/views/accounts/Logout.vue')
  },
  {
    path: '/accounts/device/register',
    name: 'accounts.register_device',
    meta: { requiresAuth: true },
    component: () => import('@/views/accounts/RegisterDevice.vue')
  },
  {
    path: '/accounts/profile',
    name: 'accounts.profile',
    meta: { requiresAuth: true },
    component: () => import('@/views/accounts/Profile.vue')
  },
  {
    path: '/accounts/devices',
    name: 'accounts.devices',
    meta: { requiresAuth: true },
    component: () => import('@/views/accounts/Devices.vue')
  },
  {
    path: '/accounts/change_password',
    name: 'accounts.change_password',
    meta: { requiresAuth: true },
    component: () => import('@/views/accounts/ChangePassword.vue')
  },
  {
    path: '/accounts/password_reset',
    name: 'accounts.password_reset',
    component: () => import('@/views/accounts/PasswordReset.vue')
  },
  {
    path: '/accounts/password_reset_by_link/:uid/:token/',
    name: 'accounts.password_reset_by_link',
    component: () => import('@/views/accounts/PasswordResetLink.vue')
  },
  {
    path: '/accounts/deactivate',
    name: 'accounts.deactivate',
    meta: { requiresAuth: true },
    component: () => import('@/views/accounts/Deactivate.vue')
  }
]
