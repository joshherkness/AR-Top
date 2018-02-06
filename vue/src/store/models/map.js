import * as types from './../mutation-types.js'

const state = {
  maps: []
}

const getters = {
  maps: state => state.maps
}

const actions = {
  setMaps ({ commit }, maps) {
    commit(types.SET_MAPS, maps)
  },
  addMap ({ commit }, map) {
    commit(types.ADD_MAP, map)
  },
  removeMap ({ commit }, id) {
    commit(types.REMOVE_MAP, id)
  },
  updateMap ({ commit }, map) {
    commit(types.UPDATE_MAP, map)
  }
}

const mutations = {
  [types.SET_MAPS] (state, maps) {
    state.maps = maps
  },
  [types.ADD_MAP] (state, map) {
    state.maps.push(map)
  },
  [types.REMOVE_MAP] (state, id) {
    state.maps = state.maps.filter((map) => {
      return map._id.$oid !== id
    })
  },
  [types.UPDATE_MAP] (state, map) {
    let index = state.maps.findIndex((e) => {
      return e._id.$oid === map._id.$oid
    })

    if (index === -1) {
      throw new Error('Map should exist in the state')
    }

    state.maps.splice(index, 1, map)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
