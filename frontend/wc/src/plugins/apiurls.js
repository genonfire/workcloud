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
  },
  ACCOUNTS_USER_SEARCH: {
    'method': 'get',
    'url': '/accounts/users/?q='
  },
  ACCOUNTS_STAFF_SEARCH: {
    'method': 'get',
    'url': '/accounts/users/staff/'
  },
  ACCOUNTS_USER_EDIT: {
    'method': 'patch',
    'url': '/accounts/users/{pk}/'
  },
  ACCOUNTS_USER_DELETE: {
    'method': 'delete',
    'url': '/accounts/users/{pk}/'
  },

  FORUM_CREATE: {
    'method': 'post',
    'url': '/communities/forum/'
  },
  FORUM_EDIT: {
    'method': 'patch',
    'url': '/communities/forum/{pk}/'
  },
  FORUM_DELETE: {
    'method': 'delete',
    'url': '/communities/forum/{pk}/'
  },
  FORUM_LIST: {
    'method': 'get',
    'url': 'communities/forums/?q='
  },
  FORUM_RETRIEVE: {
    'method': 'get',
    'url': 'communities/forums/{pk}/'
  },
  THREAD_WRITE: {
    'method': 'post',
    'url': 'communities/f/{forum}/write/'
  },
  THREAD_EDIT: {
    'method': 'patch',
    'url': 'communities/f/{forum}/{pk}/'
  },
  THREAD_DELETE: {
    'method': 'delete',
    'url': 'communities/f/{forum}/{pk}/'
  },
  THREAD_PIN: {
    'method': 'post',
    'url': 'communities/f/{forum}/{pk}/pin/'
  },
  THREAD_UNPIN: {
    'method': 'post',
    'url': 'communities/f/{forum}/{pk}/unpin/'
  },
  THREAD_RESTORE: {
    'method': 'post',
    'url': 'communities/f/{forum}/{pk}/restore/'
  },
  THREAD_RETRIEVE: {
    'method': 'get',
    'url': 'communities/f/{forum}/read/{pk}/'
  },
  THREAD_LIST: {
    'method': 'get',
    'url': 'communities/f/{forum}/?page={page}&q='
  },
  THREAD_TRASH: {
    'method': 'get',
    'url': 'communities/f/{forum}/trash/?q='
  },
  THREAD_REPLIES: {
    'method': 'get',
    'url': 'communities/f/{pk}/replies/?page_size=100'
  },
  THREAD_REPLY: {
    'method': 'post',
    'url': 'communities/f/{pk}/reply/'
  },
  REPLY_EDIT: {
    'method': 'patch',
    'url': 'communities/r/{pk}/'
  },
  REPLY_DELETE: {
    'method': 'delete',
    'url': 'communities/r/{pk}/'
  },

  FILE_UPLOAD: {
    'method': 'post',
    'url': 'things/file/'
  },
  FILE_DELETE: {
    'method': 'delete',
    'url': 'things/file/{pk}/'
  },
  FILE_LIST: {
    'method': 'get',
    'url': 'things/files/?q='
  },
  HOLIDAY_LIST: {
    'method': 'get',
    'url': 'things/holidays/{year}/'
  },
  UPDATE_HOLIDAY: {
    'method': 'post',
    'url': 'things/holidays/{year}/'
  },
  EDIT_HOLIDAY: {
    'method': 'patch',
    'url': 'things/holiday/{pk}/'
  },
  DELETE_HOLIDAY: {
    'method': 'delete',
    'url': 'things/holiday/{pk}/'
  },

  YOUTUBE_OEMBED: {
    'method': 'get',
    'url': 'https://www.youtube.com/oembed?url={url}&format=json&maxwidth=640&maxheight=360'
  }
}

APIs.install = function (Vue) {
  Vue.prototype.$baseURL = () => process.env.VUE_APP_API_SERVER
  Vue.prototype.$apiPrefix = () => process.env.VUE_APP_API_PREFIX
  Vue.prototype.$api = (key) => APIs[key]
};

export default APIs
