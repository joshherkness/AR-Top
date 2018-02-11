import * as types from './../mutation-types.js'

const state = {
  session: null
}

const getters = {
  session: state => state.session
}

const actions = {
  // eslint-disable-next-line
  setSession({ commit }, session) {
    commit(types.SET_SESSION, session)
  },

  // eslint-disable-next-line
  updateSession({ commit }, session) {
    commit(types.UPDATE_SESSION, session)
  },

  // eslint-disable-next-line
  removeSession({ commit }) {
    commit(types.REMOVE_SESSION)
  }
}

const mutations = {
  // eslint-disable-next-line
  [types.SET_SESSION](state, session) {
    state.session = session
  },

  // eslint-disable-next-line
  [types.UPDATE_SESSION](state, session) {
    state.session = session
  },

  // eslint-disable-next-line
  [types.REMOVE_SESSION](state) {
    state.session = null
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
