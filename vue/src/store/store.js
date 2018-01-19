import Vue from 'vue'
import Vuex from 'vuex'
import user from './models/user.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user
  }
})
