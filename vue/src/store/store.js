import Vue from 'vue'
import Vuex from 'vuex'
import user from './models/user.js'
import * as Cookies from 'js-cookie'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user
  },
  plugins: [
    createPersistedState({
      storage: {
        getItem: key => Cookies.get(key),
        // expires after 1 day
        setItem: (key, value) => Cookies.set(key, value, { expires: 1 }),
        removeItem: key => Cookies.remove(key)
      }
    })
  ]
})
