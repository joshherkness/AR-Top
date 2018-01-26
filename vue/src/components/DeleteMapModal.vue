<template>
  <modal name="delete-map-modal"
    transition="pop-out"
    :height="'auto'"
    :width="modalWidth"
    :adaptive="true"
    :pivotY="0.5"
    :scrollable="true"
    :reset="true"
    @before-open="beforeOpened"
    @before-close="beforeClosed">
    <div class="card">
      <div class="card-content">
        <h1 class="title is-4">Delete map</h1>

        <!-- Content field -->
        <div class="field content">
          <article class="message is-warning">
            <div class="message-body">
              Unexpected bad things will happen if you don't read this!
            </div>
          </article>
          <p class="m-b-10">This action <b>CANNOT</b> be undone. 
          This will delete the <b>{{params.name}}</b> map perminently.</p>
          <p>Please type in the name of the map to confirm.</p>
        </div>

        <!-- Confirm name-->
        <div class="field">
          <div class="control">
            <input
              name="map name"
              v-model="name"
              type="text"
              placeholder="Type the map name"
              class="input">
          </div>
        </div>

        <!-- Buttons -->
        <div class="field is-grouped is-grouped-right">
          <p class="control">
            <button 
              v-on:click="submit" 
              class="button is-danger" 
              type="submit"
              :disabled="!isSubmitEnabled">Delete</button>
            <button v-on:click="cancel" class="button is-white">Cancel</button>
          </p>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
// Specifies the width of this modal
const MODAL_WIDTH = 500

export default {
  name: 'DeleteMapModal',
  data: function () {
    return {
      name: '',
      params: {},
      modalWidth: MODAL_WIDTH
    }
  },
  created: function () {
    this.modalWidth =
      window.innerWidth < MODAL_WIDTH ? MODAL_WIDTH / 2 : MODAL_WIDTH
  },
  computed: {
    isSubmitEnabled: function () {
      return this.name === this.params.name
    }
  },
  methods: {
    beforeOpened (event) {
      this.params = event.params || {}
      this.$emit('before-opened', event)
    },
    beforeClosed (event) {
      this.params = {}
      this.$emit('before-closed', event)
    },
    submit: function () {
      // Delete map here
      console.log('Delete')
    },
    cancel: function () {
      this.$modal.hide('delete-map-modal')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>


