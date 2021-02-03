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
  PASSWORD_MIN: 8
}

Const.install = function (Vue) {
  Vue.prototype.$const = (key) => Const[key]
};

export default Const
