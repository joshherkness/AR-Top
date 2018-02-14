import Vue from 'vue'
import Vuex from 'vuex'
import user from './models/user.js'
import map from './models/map'
import session from './models/session'
import * as Cookies from 'js-cookie'
import createPersistedState from 'vuex-persistedstate'
import * as types from './mutation-types'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    map,
    session
  },
  state: {
    layout: 'grid'
  },
  actions: {
    // eslint-disable-next-line
    setLayout({ commit }, layout) {
      commit(types.SET_LAYOUT, layout)
    }
  },
  mutations: {
    // eslint-disable-next-line
    [types.SET_LAYOUT](state, layout) {
      state.layout = layout
    }
  },
  getters: {
    // eslint-disable-next-line
    layout(state) {
      return state.layout
    }
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
