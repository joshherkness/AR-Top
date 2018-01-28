<template>
  <div>
    <create-map-modal/>
    <delete-map-modal/>
    <div>
      <button class="button is-light is-pulled-right" @click="$modal.show('create-map-modal', {test: 'josh'})">
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
import CreateMapModal from '../CreateMapModal'
import DeleteMapModal from '../DeleteMapModal'
import MapList from './MapList'
export default {
  name: 'Maps',
  components: {
    CreateMapModal,
    DeleteMapModal,
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
