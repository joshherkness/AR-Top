import * as types from './../mutation-types.js'

const state = {
  session_id: null,
  code: null,
  created_at: null,
  game_map_id: null,
  user_id: null
}

const getters = {
  session_id: state => state.session_id,
  code: state => state.code,
  created_at: state => state.created_at,
  game_map_id: state => state.game_map_id,
  user_id: state => state.user_id
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
    state.session_id = session._id.$oid
    state.code = session.code
    state.created_at = session.created_at.$date
    state.game_map_id = session.game_map_id.$oid
    state.user_id = session.user_id.$oid
  },

  // eslint-disable-next-line
  [types.UPDATE_SESSION](state, session) {
    state.session_id = session._id.$oid
    state.code = session.code
    state.created_at = session.created_at.$date
    state.game_map_id = session.game_map_id.$oid
    state.user_id = session.user_id.$oid
  },

  // eslint-disable-next-line
  [types.REMOVE_SESSION](state) {
    state.session_id = null
    state.code = null
    state.created_at = null
    state.game_map_id = null
    state.user_id = null
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
