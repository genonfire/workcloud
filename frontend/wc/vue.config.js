module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true
    }
  },
  devServer: {
    https: false,
    hot: true,
    disableHostCheck: true
  },
  outputDir: 'dist',
  productionSourceMap: false
}
