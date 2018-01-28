<template>
  <div>
    <edit-map-modal />
    <div class="map-cards">
      <map-card v-for="map in maps"
        :key="map.name"
        v-bind:name="map.name"
        v-bind:depth="map.depth"
        v-bind:width="map.width" />
    </div>

    <!-- Error message -->
    <article class="message is-danger" v-show="error">
      <div class="message-header">
        <p>Error</p>
      </div>
      <div class="message-body">
        You currently have no maps.
      </div>
    </article>
  </div>
</template>

<script>
import axios from 'axios'
import MapCard from './MapCard'
import EditMapModal from '../EditMapModal'
export default {
  name: 'MapList',
  data: function () {
    return {
      maps: [],
      error: false
    }
  },
  components: {
    MapCard,
    EditMapModal
  },
  created: async function () {
    try {
      // Still need correct URL
      const response = await axios.get('http://localhost:5000/api/maps/' + this.$store.state.user.token)
      if (response.data.maps.length === 0) {
        this.error = true
      } else {
        this.maps = response.data.maps
      }
    } catch (err) {
      console.error(err)
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

@media (max-width: 32em) {
  .map-cards {
    display: flex;
    flex-direction: column;
  }
}
</style>
