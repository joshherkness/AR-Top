import * as types from './../mutation-types.js'

const state = {
  maps: []
}

const getters = {
  maps: state => state.maps
}

const actions = {
  // eslint-disable-next-line
  setMaps({ commit }, maps) {
    commit(types.SET_MAPS, maps)
  },

  // eslint-disable-next-line
  addMap({ commit }, map) {
    commit(types.ADD_MAP, map)
  },

  // eslint-disable-next-line
  removeMap({ commit }, id) {
    commit(types.REMOVE_MAP, id)
  },

  // eslint-disable-next-line
  updateMap({ commit }, map) {
    commit(types.UPDATE_MAP, map)
  },

  // eslint-disable-next-line
  removeAllMaps({ commit }) {
    commit(types.REMOVE_ALL_MAPS)
  }
}

const mutations = {
  // eslint-disable-next-line
  [types.SET_MAPS](state, maps) {
    state.maps = maps
  },

  // eslint-disable-next-line
  [types.ADD_MAP](state, map) {
    state.maps.push(map)
  },

  // eslint-disable-next-line
  [types.REMOVE_MAP](state, id) {
    state.maps = state.maps.filter(map => {
      return map._id.$oid !== id
    })
  },

  // eslint-disable-next-line
  [types.UPDATE_MAP](state, map) {
    let index = state.maps.findIndex(e => {
      return e._id.$oid === map._id.$oid
    })

    if (index === -1) {
      throw new Error('Map should exist in the state')
    }

    state.maps.splice(index, 1, map)
  },

  // eslint-disable-next-line
  [types.REMOVE_ALL_MAPS](state) {
    state.maps = []
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
