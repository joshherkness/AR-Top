<template>
  <div class="section">
    <div class="container">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <span class="title is-5">My Library</span>
          </div>
          <!-- Loading spinner -->
          <div v-if="loading" class="level-item">
            <span class="loader"></span>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <p class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                placeholder="search"
                v-model="filter">
              <span class="icon is-small is-left">
                <i class="mdi mdi-magnify" />
              </span>
            </p>
          </div>
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
      <div v-if="!loading">
        <map-grid v-show="layout === 'grid'" v-bind:maps="filteredMaps"/>
        <map-list v-show="layout === 'list'" v-bind:maps="filteredMaps"/>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { API } from '@/api/api'

import MapGrid from '@/components/MapGrid'
import MapList from '@/components/MapList'

export default {
  name: 'Library',
  data: function () {
    return {
      loading: false,
      error: false,
      message: 'You currently have no maps.',
      filter: ''
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
    ]),
    filteredMaps: function () {
      return this.maps.filter(map => {
        return map.name.toLowerCase().includes(this.filter.toLowerCase())
      })
    }
  },
  methods: {
    ...mapActions([
      'setMaps',
      'setLayout'
    ])
  },
  mounted: async function () {
    try {
      // Set as loading
      this.loading = true

      const maps = await API.getMaps()
      if (maps.length === 0) {
        this.error = true
      } else {
        this.setMaps(maps)
      }
    } catch (err) {
      let msg = err.response.data.error
      this.error = true
      if (msg !== 'map error') {
        this.message = msg
      }
    }

    this.loading = false
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
