<template>
  <div class="section">
    <div class="container">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <span class="title is-5">My Library</span>
          </div>
        </div>
        <div class="level-right">
          <!-- Grid layout control -->
          <div class="level-item">
            <div class="field has-addons">
              <p class="control">
                <a class="button is-light"
                :class="{'is-active': layout === 'grid'}"
                @click="setLayout('grid')">
                  <span class="icon">
                    <i class="mdi mdi-view-grid"></i>
                  </span>
                </a>
              </p>
              <p class="control">
                <a class="button is-light"
                :class="{'is-active': layout === 'list'}"
                @click="setLayout('list')">
                  <span class="icon">
                    <i class="mdi mdi-view-list"></i>
                  </span>
                </a>
              </p>
            </div>
          </div>
          <div class="level-item">
            <button 
              class="button is-light is-pulled-right" 
              @click="$modal.show('create-map-modal')">
              <span class="icon">
                <i class="fa fa-plus"></i>
              </span>
              <span>Create a map</span>
          </button>
          </div>
        </div>
      </div>
      <hr>
      
      <!-- Library content here -->
      <map-grid v-show="layout === 'grid'" v-bind:maps="maps"/>
      <map-list v-show="layout === 'list'" v-bind:maps="maps"/>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { API } from '@/api/api'

import MapGrid from './MapGrid'
import MapList from './MapList'

export default {
  name: 'Library',
  data: function () {
    return {
      error: false,
      message: 'You currently have no maps.'
    }
  },
  components: {
    MapGrid,
    MapList
  },
  computed: {
    ...mapGetters([
      'maps',
      'layout'
    ])
  },
  methods: {
    ...mapActions([
      'setMaps',
      'setLayout'
    ])
  },
  mounted: async function () {
    try {
      const maps = await API.getMaps()
      if (maps.length === 0) {
        this.error = true
      } else {
        this.setMaps(maps)
      }
    } catch (err) {
      let msg = err.response.data.error
      if (msg === 'token expired') {
        this.$store.dispatch('signOutUser')
      } else if (msg === 'map error') {
        this.error = true
      } else {
        this.message = msg
        this.error = true
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
