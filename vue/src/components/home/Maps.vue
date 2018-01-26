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
      <button class="button is-light is-pulled-right" @click="$modal.show('delete-map-modal', {name: 'Exandria'})">
        <span class="icon">
          <i class="fa fa-trash"></i>
        </span>
        <span>Delete a map</span>
      </button>
    </div>
  </div>
</template>

<script>
import CreateMapModal from '../CreateMapModal'
import DeleteMapModal from '../DeleteMapModal'
export default {
  name: 'Maps',
  components: {
    CreateMapModal,
    DeleteMapModal
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
