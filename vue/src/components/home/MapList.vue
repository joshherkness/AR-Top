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
import axios from 'axios'
import MapCard from './MapCard'
import EditMapModal from '../EditMapModal'
import { generateConfig } from './../../api/api'
export default {
  name: 'MapList',
  data: function () {
    return {
      maps: [],
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
      const url = 'http://localhost:5000/api/maps/' + this.$store.state.user.token
      const response = await axios.get(url, generateConfig({auth_token: this.$store.state.user.token}))
      if (response.data.length === 0) {
        this.error = true
      } else {
        this.maps = response.data
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
