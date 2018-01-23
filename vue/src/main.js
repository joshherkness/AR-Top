// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/store'
import VModal from 'vue-js-modal'
import VeeValidate from 'vee-validate'

Vue.config.productionTip = false

Vue.use(VModal)
Vue.use(VeeValidate)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
