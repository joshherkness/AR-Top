<template>
  <div>
    <edit-map-modal />
    <div class="field has-addons is-right">
      <div class="control">
        <div class="button is-medium is-light"
             aria-haspopup='true'
             :class="{'is-active': gridView}"
             @click="toggle"
             >
             <span class="icon is-medium">
               <i class="mdi mdi-view-grid"></i>
             </span>
             <div class="is-size-7">Grid</div>
        </div>
      </div>
      <div class="control">
        <div class="button is-medium is-light"
          :class="{'is-active': !gridView}"
          @click="toggle"
          >
          <span class="icon is-medium">
            <i class="mdi mdi-view-list"></i>
          </span>
          <div class="is-size-7">List</div>
        </div>
      </div>
    </div>

    <div class="map-cards" v-if="gridView">
      <map-card v-for="map in maps"
        :key="map.name"
        v-bind:name="map.name"
        v-bind:oid="map._id.$oid"
        v-bind:color="map.color"
        v-bind:depth="map.depth"
        v-bind:width="map.width"/>
    </div>
    
    <div v-if="!gridView">
      <table class="table is-fullwidth">
        <thead>
          <tr>
            <th>Name</th>
            <th>Size</th>
            <th>Color</th>
          </tr>
        </thead>
        <tbody>
          <map-list v-for="map in maps"
             v-bind:name="map.name"
             v-bind:oid="map._id.$oid"
             v-bind:color="map.color"
             v-bind:depth="map.depth"
             v-bind:width="map.width"/>
        </tbody>
      </table>
    </div>

    <!-- Error message -->
    <div class="container is-fluid">
      <article class="message is-danger" v-show="error">
        <div class="message-header">
          <p>Error</p>
        </div>
        <div class="message-body has-text-centered">
          {{ message }}
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import MapCard from './MapCard'
import MapList from './MapList'
import EditMapModal from '../EditMapModal'
import { mapActions, mapGetters } from 'vuex'
import { API } from '@/api/api'

export default {
  name: 'MapContainer',
  data: function () {
    return {
      error: false,
      message: 'You currently have no maps.',
      gridView: true
    }
  },
  components: {
    MapCard,
    EditMapModal,
    MapList
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
  },
  computed: {
    ...mapGetters([
      'maps'
    ])
  },
  methods: {
    ...mapActions([
      'setMaps'
    ]),
    toggle: function () {
      this.gridView = !this.gridView
    }
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';

.map-cards {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
}

.is-active .mdi {
  color: $blue;
}

@media (max-width: 32em) {
  .map-cards {
    display: flex;
    flex-direction: column;
  }
}
</style>
