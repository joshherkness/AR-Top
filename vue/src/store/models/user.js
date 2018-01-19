import * as types from './../mutation-types.js'

const state = {
  email: '',
  token: ''
}

const getters = {
  email: state => state.email,
  token: state => state.token
}

const actions = {
  updateUser ({ commit }, user) {
    commit(types.SET_USER, user)
  },

  signOutUser ({ commit }) {
    commit(types.UNSET_USER)
  }
}

const mutations = {
  [types.SET_USER] ({ commit }, user) {
    state.email = user.email
    state.token = user.auth_token
  },

  [types.UNSET_USER] ({ commit }) {
    state.email = ''
    state.token = ''
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
