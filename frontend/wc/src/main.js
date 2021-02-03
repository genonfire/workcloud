import Vue from 'vue'
import Vuex from 'vuex'
import vuetify from './plugins/vuetify'
import VuetifyDialog from 'vuetify-dialog'
import 'vuetify-dialog/dist/vuetify-dialog.css'
import i18n from './plugins/i18n'
import apiurls from './plugins/apiurls'
import glovue from './plugins/glovue'
import router from './router'
import { store } from './store'
import App from './App.vue'

Vue.use(Vuex)
Vue.use(VuetifyDialog, {
  context: {
    vuetify
  }
});
Vue.use(apiurls);
Vue.use(glovue);
Vue.config.productionTip = false

new Vue({
  vuetify,
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
