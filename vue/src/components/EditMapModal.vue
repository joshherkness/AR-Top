<template>
  <modal
    name="edit-map-modal"
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
        <h1 class="title is-4">Edit map</h1>

        <!-- Map name -->
        <form @submit.prevent="validateBeforeSubmit">
          <div class="field">
            <label class="label">Map name</label>
            <div class="control">
              <input
                name="map name"
                v-model="name"
                v-validate="nameValidator"
                type="text"
                v-bind:placeholder="params.name"
                :class="{'input': true, 'is-danger': errors.has('map name') }">
            </div>
            <span class="help">Think of a cool name for your map</span>
            <span v-show="errors.has('map name')" class="help is-danger">{{ errors.first('map name') }}</span>
          </div>

          <!-- Map size -->
          <div class="field">
            <label class="label">Map size (optional)</label>
            <div class="control">
              <input
                name="map size"
                v-model="size"
                v-validate="sizeValidator"
                type="text"
                v-bind:placeholder="params.depth * params.width"
                :class="{'input': true, 'is-danger': errors.has('map size') }" >
            </div>
            <span class="help">This specifies how large your map will be</span>
            <span v-show="errors.has('map size')" class="help is-danger">{{ errors.first('map size') }}</span>
          </div>

          <!-- Buttons -->
          <div class="field is-grouped is-grouped-right">
            <p class="control">
              <button v-on:click="submit" class="button is-link" type="submit" :disabled="errors.any()">Submit</button>
              <button v-on:click="cancel" class="button is-white">Cancel</button>
            </p>
          </div>
        </form>
      </div>
    </div>
  </modal>
</template>

<script>
import { Sketch } from 'vue-color'

const MODAL_WIDTH = 500

// This validator will be used for the name field
const NAME_VALIDATOR = {
  required: true,
  alpha_spaces: true,
  max: 16
}

// This validator will be used for the size field
const SIZE_VALIDATOR = {
  required: false,
  numeric: true,
  min_value: 1,
  max_value: 64
}

export default {
  name: 'EditMapModal',
  data: function () {
    return {
      name: '',
      size: '',
      color: '',
      params: {},
      modalWidth: MODAL_WIDTH,
      nameValidator: NAME_VALIDATOR,
      sizeValidator: SIZE_VALIDATOR
    }
  },
  components: {
    'sketch-picker': Sketch
  },
  created: function () {
    this.modalWidth =
      window.innerWidth < MODAL_WIDTH ? MODAL_WIDTH / 2 : MODAL_WIDTH
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
    validateBeforeSubmit: function () {
      this.$validator.validateAll()
    },
    submit: function () {
    },
    cancel: function () {
      this.$modal.hide('edit-map-modal')
    }
  }

}
</script>
