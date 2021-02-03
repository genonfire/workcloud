const APIs = {
  ACCOUNTS_SIGNUP: {
    'method': 'post',
    'url': '/accounts/signup/'
  },
  ACCOUNTS_LOGIN: {
    'method': 'post',
    'url': '/accounts/login/'
  },
  ACCOUNTS_CONNECT: {
    'method': 'post',
    'url': '/accounts/connect/'
  },
  ACCOUNTS_LOGOUT: {
    'method': 'post',
    'url': '/accounts/logout/'
  },
  ACCOUNTS_DEVICE_REGISTER: {
    'method': 'post',
    'url': '/accounts/device/{pk}/register/'
  },
  ACCOUNTS_DEVICE_DELETE: {
    'method': 'delete',
    'url': '/accounts/device/{pk}/delete/'
  },
  ACCOUNTS_DEVICES: {
    'method': 'get',
    'url': '/accounts/devices/'
  },
  ACCOUNTS_PASSWORD_CHANGE: {
    'method': 'post',
    'url': '/accounts/password_change/'
  },
  ACCOUNTS_PASSWORD_RESET: {
    'method': 'post',
    'url': '/accounts/password_reset/'
  },
  ACCOUNTS_PASSWORD_RESET_CONFIRM: {
    'method': 'post',
    'url': '/accounts/password_reset_confirm/'
  },
  ACCOUNTS_SETTING_GET: {
    'method': 'get',
    'url': '/accounts/setting/'
  },
  ACCOUNTS_SETTING_SET: {
    'method': 'patch',
    'url': '/accounts/setting/'
  },
  ACCOUNTS_DEACTIVATE: {
    'method': 'post',
    'url': '/accounts/deactivate/'
  }
}

APIs.install = function (Vue) {
  Vue.prototype.$baseURL = () => process.env.VUE_APP_API_SERVER
  Vue.prototype.$api = (key) => APIs[key]
};

export default APIs
