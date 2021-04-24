const Const = {
  LANGUAGES: [
    {
      code: 'en',
      name: 'English'
    },
    {
      code: 'ko',
      name: '한국어'
    },
  ],
  DEFAULT_LANGUAGE: 'ko',
  PASSWORD_MIN: 8,
  SEARCH_ROUTES: {
    // router name from: router name to
    'communities.forum': 'communities.forum',
    'communities.threadPage': 'communities.threadPage',
    'communities.trash': 'communities.trash',
  }
}

Const.install = function (Vue) {
  Vue.prototype.$const = (key) => Const[key]
};

export default Const
