<template>
  <div>
    <create-map-modal/>
    <div>
      <button class="button is-light is-pulled-right" @click="$modal.show('create-map-modal')">
        <span class="icon">
          <i class="fa fa-plus"></i>
        </span>
        <span>Create a map</span>
      </button>
    </div>
  </div>
</template>

<script>
import CreateMapModal from '../CreateMapModal'
export default {
  name: 'Maps',
  components: {
    CreateMapModal
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
