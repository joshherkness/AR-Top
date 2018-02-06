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
      <map-list />
    </div>
  </div>
</template>

<script>
import MapList from './MapList'
export default {
  name: 'Maps',
  components: {
    MapList
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
