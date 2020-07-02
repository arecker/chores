import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// libs
import libs from './libs.js'

import App from './App.vue'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.prototype.libs = libs

Vue.config.productionTip = false

new Vue({
  render: function (h) { return h(App) }
}).$mount('#app')
