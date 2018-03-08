// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/store'
import VModal from 'vue-js-modal'
import VeeValidate from 'vee-validate'
import moment from 'moment'

Vue.config.productionTip = false

Vue.use(VModal)
Vue.use(VeeValidate)

Vue.filter('uppercase', function (value) {
  if (!value) {
    return ''
  }
  value = value.toString()
  return value.toUpperCase()
})

moment().calendar(null, {
  sameDay: '[Today]',
  nextDay: '[Tomorrow]',
  nextWeek: 'dddd',
  lastDay: '[Yesterday]',
  lastWeek: '[Last] dddd',
  sameElse: 'MM/DD/YYYY h:mm a'
})

Vue.filter('date', function (value) {
  if (value) {
    return moment(value).calendar()
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
