// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import { DatePicker, Input, Select } from 'element-ui'
import i18n from 'vue-i18n'
import locale from 'element-ui/lib/locale/lang/en'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(i18n)
Vue.use(ElementUI, { locale })
Vue.use(DatePicker)
Vue.use(Input)
Vue.use(Select)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false
Vue.config.lang = 'en'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
