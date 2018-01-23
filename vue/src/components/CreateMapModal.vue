<template>
  <modal name="create-map-modal"
    transition="pop-out"
    :height="'auto'"
    :width="modalWidth"
    :adaptive="true"
    :pivotY="0.5"
    :scrollable="true"
    :reset="true">
    <div class="card">
      <div class="card-content">
        <h1 class="title is-4">Create a new map</h1>
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
                placeholder="e.g Exandria"
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
                placeholder="e.g 32"
                :class="{'input': true, 'is-danger': errors.has('map size') }" >
            </div>
            <span class="help">This specifies how large your map will be</span>
            <span v-show="errors.has('map size')" class="help is-danger">{{ errors.first('map size') }}</span>
          </div>

          <!-- Map color -->
          <label class="label">Map color (optional)</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <input
                name="map color"
                v-model="color"
                v-validate="colorValidator"
                class="input"
                type="text"
                placeholder="e.g #DDDDDD"
                :class="{'input': true, 'is-danger': errors.has('map color') }">
              <span class="help">This specifies the color that will be used as the base of your map</span>
              <span v-show="errors.has('map color')" class="help is-danger">{{ errors.first('map color') }}</span>
            </div>
            <!-- Color picker dropdown -->
            <div class="control">
              <div class="dropdown is-hoverable is-up is-right is-pulled-right">
                <div class="dropdown-trigger">
                  <button class="button is-static">
                    <span class="color-swatch" :style="{'background-color': color}"></span>
                  </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu4" role="menu">
                  <sketch-picker v-model="colorData"></sketch-picker>
                </div>
              </div>

            </div>
          </div>

          <!-- Other settings -->
          <div class="field">
            <label class="label">Other settings</label>
            <div class="control">
              <label class="checkbox">
                <input v-model="public" class="checkbox" type="checkbox">
                Public
              </label>
            </div>
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

// Specifies the width of this modal
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

// This validator will be used for the color field
const COLOR_VALIDATOR = {
  required: false,
  regex: `^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$` // Hex color without alpha
}

export default {
  name: 'CreateMapModal',
  data: function () {
    return {
      name: '',
      size: '',
      color: '',
      public: true,
      modalWidth: MODAL_WIDTH,
      nameValidator: NAME_VALIDATOR,
      sizeValidator: SIZE_VALIDATOR,
      colorValidator: COLOR_VALIDATOR,
      colorData: {hex: '#ffffff'}
    }
  },
  components: {
    'sketch-picker': Sketch
  },
  created: function () {
    this.modalWidth =
      window.innerWidth < MODAL_WIDTH ? MODAL_WIDTH / 2 : MODAL_WIDTH
  },
  watch: {
    colorData: function (_colorData) {
      this.color = _colorData.hex
    }
  },
  methods: {
    validateBeforeSubmit: function () {
      this.$validator.validateAll()
    },
    submit: function () {
      // Ensure there are no errors in any of the fields
      if (this.errors.any()) {
        return
      }

      let mapData = {
        name: this.name,
        size: this.size,
        color: this.color,
        public: this.public
      }

      // Create map here
      console.log(mapData)
    },
    cancel: function () {
      this.$modal.hide('create-map-modal')
    }
  }
}
</script>

<style lang="scss" scoped>
.color-swatch {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #000;
  cursor: pointer;
}

.color-picker {
  position: absolute;
  bottom: 0;
  right: 0;
}
</style>


