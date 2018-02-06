<template>
  <div>
    <edit-map-modal />
    <div class="map-cards">
      <map-card v-for="map in maps"
        :key="map.name"
        v-bind:name="map.name"
        v-bind:oid="map._id.$oid"
        v-bind:color="map.color"
        v-bind:depth="map.depth"
        v-bind:width="map.width"/>
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
import EditMapModal from '../EditMapModal'
import { mapActions, mapGetters } from 'vuex'
import { API } from '@/api/api'

export default {
  name: 'MapList',
  data: function () {
    return {
      error: false,
      message: 'You currently have no maps.'
    }
  },
  components: {
    MapCard,
    EditMapModal
  },
  mounted: async function () {
    try {
      this.maps = await API.getMaps()
      if (this.maps.length === 0) {
        this.error = true
      } else {
        this.setMaps(response.data)
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
    ])
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

@media (max-width: 32em) {
  .map-cards {
    display: flex;
    flex-direction: column;
  }
}
</style>
