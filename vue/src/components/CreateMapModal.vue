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
          <div class="field">
            <label class="label">Map name</label>
            <div class="control">
              <input
                name="name"
                v-model="form.name"
                v-validate="nameValidator"
                type="text"
                placeholder="e.g Exandria"
                :class="{'input': true, 'is-danger': errors.has('name') }">
            </div>
            <span class="help">Think of a name for your map</span>
            <span v-show="errors.has('name')" class="help is-danger">{{ errors.first('name') }}</span>
          </div>

          <!-- Map size -->
          <div class="field">
            <label class="label">Map size (optional)</label>
            <div class="control">
              <input
                name="size"
                v-model="form.size"
                v-validate="sizeValidator"
                type="number"
                placeholder="e.g 32"
                :class="{'input': true, 'is-danger': errors.has('size') }" >
            </div>
            <span class="help">This specifies how large your map will be</span>
            <span v-show="errors.has('size')" class="help is-danger">{{ errors.first('size') }}</span>
          </div>

          <!-- Map color -->
          <label class="label">Map color (optional)</label>
          <div class="field has-addons">
            <div class="control is-expanded">
              <input
                name="color"
                v-model="form.color"
                v-validate="colorValidator"
                class="input"
                type="text"
                :placeholder="`e.g ${defaultColor}`"
                :class="{'input': true, 'is-danger': errors.has('color') }">
              <span class="help">This specifies the color that will be used as the base of your map</span>
              <span v-show="errors.has('color')" class="help is-danger">{{ errors.first('color') }}</span>
            </div>
            <!-- Color picker dropdown -->
            <div class="control">
              <div class="dropdown is-hoverable is-up is-right is-pulled-right">
                <div class="dropdown-trigger">
                  <button class="button is-static">
                    <span class="color-swatch" :style="{'background-color': colorData.hex}"></span>
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
                <input v-model="form.private" class="checkbox" type="checkbox">
                Private
              </label>
            </div>
          </div>

          <!-- Buttons -->
          <div class="field is-grouped is-grouped-right">
            <p class="control">
              <button v-on:click="submit"
                class="button is-link" 
                :class="{'is-loading': loading}"
                :disabled="errors.any()">Submit</button>
              <button v-on:click="close" 
              class="button is-white">Cancel</button>
            </p>
          </div>
      </div>
    </div>
  </modal>
</template>

<script>
import { Sketch } from 'vue-color'
import axios from 'axios'
import { generateConfig } from '@/api/api'
import { mapActions } from 'vuex'
import router from '@/router/index'

const DEFAULT_COLOR = '#9B9B9B'
const DEFAULT_SIZE = 32
const DEFAULT_HEIGHT = 48

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
  max_value: 48
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
      form: {
        name: '',
        size: '',
        color: '',
        private: true
      },
      modalWidth: MODAL_WIDTH,
      nameValidator: NAME_VALIDATOR,
      sizeValidator: SIZE_VALIDATOR,
      colorValidator: COLOR_VALIDATOR,
      colorData: {
        hex: DEFAULT_COLOR
      },
      defaultColor: DEFAULT_COLOR,
      loading: false
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
      this.form.color = _colorData.hex
    },
    form: {
      handler: function (data) {
        if (!data.color) {
          this.colorData.hex = DEFAULT_COLOR
          return
        }
        this.colorData.hex = data.color
      },
      deep: true
    }
  },
  methods: {
    ...mapActions([
      'addMap'
    ]),
    /**
     * Submit the form, creating the map
     */
    submit: async function () {
      try {
        // Determine if there are any validation errors
        let result = await this.$validator.validateAll()
        if (!result) return

        this.loading = true

        let data = {
          map: {
            name: this.form.name,
            width: this.form.size || DEFAULT_SIZE,
            height: DEFAULT_HEIGHT,
            depth: this.form.size || DEFAULT_SIZE,
            color: this.form.color || DEFAULT_COLOR,
            private: this.form.private,
            models: []
          }
        }

        let url = 'http://localhost:5000/api/map'
        let response = await axios.post(url, data, generateConfig({
          email: this.$store.state.user.email
        }))

        // Close this modal
        this.close(true)

        // Route the user to their newly created map
        let map = response.data.map
        this.addMap(map)
        router.push({name: 'editor', params: {id: map._id.$oid}})

        // Navigate to the editor here
      } catch (err) {
        throw err
      }

      this.loading = false
    },

    /**
     * Close this modal
     */
    close: function (clear = false) {
      if (clear) {
        Object.assign(this.$data, this.$options.data())
      }

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


