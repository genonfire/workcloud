import vuetify from './vuetify'
import router from '@/router'
import i18n from './i18n'

export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(router)
    .use(i18n)
}
