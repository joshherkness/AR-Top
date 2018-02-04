<template>
  <div>
    <div>
      <div class="title is-5">
        <span>My Library</span>
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
    <hr>
    <map-list />
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
