<template>
  <nav class="navbar has-shadow is-fixed-bottom level is-dark" style="padding: 0 1em; bottom: -1.5em;">
    <div class="level-left">
      <div class="level-item">
        <div class="dropdown is-hoverable is-up">
          <div class="dropdown-trigger">
            <button class="button is-link" aria-haspopup="true" aria-controls="dropdown-menu4">
              <span>{{ name }}</span>
              <span class="icon is-small">
                <i class="mdi mdi-chevron-down" />
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu4" role="menu">
            <div class="dropdown-content">
              <nav class="panel">
                <div class="panel-block">
                  <p class="control has-icons-left">
                  <input class="input" type="text" placeholder="search" v-model="search">
                  <span class="icon is-small is-left">
                    <i class="mdi mdi-magnify" />
                  </span>
                  </p>
                </div>
                <router-link class="panel-block" v-for="map in searchList"
                  :key="map._id.$oid" 
                  @click.native="setOpen(map._id.$oid)"
                  :to="{ name: 'editor', params: { id: map._id.$oid }}">
                  <span class="panel-icon" v-if="map._id.$oid === game_map_id">
                    <i class="mdi mdi-check"/>
                  </span>
                  {{ map.name }}
                </router-link>
              </nav>
            </div>
          </div>
        </div>
      </div>
      <div class="level-item" v-if="$route.name === 'editor'">
        <a class="button is-link is-inverted" @click="showParty">Show party</a>
      </div>
    </div>
    <div class="level-right">
      <div class="level-item">
        <div class="tags has-addons">
          <span class="tag is-medium">Invitation code</span>
          <span class="tag is-medium is-link">{{ code }}</span>
        </div>
      </div>
      <div class="level-item">
        <div class="dropdown is-hoverable is-right is-up">
          <div class="dropdown-trigger">
            <p class="field">
            <a class="button is-light">
              <span class="icon">
                <i class="mdi mdi-dots-vertical" />
              </span>
            </a>
            </p>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a class="dropdown-item has-text-danger" @click="remove">
                Close session
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { API } from '@/api/api'
import store from '@/store/store'
import { mapGetters } from 'vuex'
export default {
  name: 'SessionManager',
  data: function () {
    return {
      search: '',
      queuedID: null
    }
  },
  computed: {
    ...mapGetters([
      'maps',
      'code',
      'session_id',
      'game_map_id'
    ]),
    name: function () {
      const mapID = store.state.session.game_map_id
      return store.state.map.maps.filter(map => map._id.$oid === mapID)[0].name
    },
    searchList: function () {
      return store.state.map.maps.filter(map => {
        return map.name.toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },
  methods: {
    remove: async function () {
      await API.deleteSession(store.state.session.session_id)
      store.dispatch('removeSession')
    },
    showParty: function () {
      // TODO: emit to party
    },
    setOpen: function (id) {
      this.queuedID = id
    }
  }
}
</script>
