<template>
  <div>
    <div>
      <button class="button is-light is-pulled-right" @click="$modal.show('create-map-modal')">
        <span class="icon">
          <i class="fa fa-plus"></i>
        </span>
        <span>Create a map</span>
      </button>
    </div>
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
.button.is-light.is-pulled-right {
  margin: 3.5em 2em 3em 0;
}
</style>
