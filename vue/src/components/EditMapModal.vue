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
        <div class="field">
          <label class="label">Map name</label>
          <div class="control">
            <input
              name="name"
              v-model="form.name"
              v-validate="nameValidator"
              type="text"
              v-bind:placeholder="params.name"
              :class="{'input': true, 'is-danger': errors.has('name') }">
          </div>
          <span class="help">Think of another cool name for your map</span>
          <span v-show="errors.has('name')" class="help is-danger">{{ errors.first('name') }}</span>
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
              :placeholder="`e.g ${params.color}`"
              :class="{'input': true, 'is-danger': errors.has('color') }">
            <span class="help">Change the color that will be used as the base of your map</span>
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

const MODAL_WIDTH = 500
const DEFAULT_COLOR = '#9B9B9B'

// This validator will be used for the name field
const NAME_VALIDATOR = {
  required: true,
  alpha_spaces: true,
  max: 16
}

// This validator will be used for the color field
const COLOR_VALIDATOR = {
  required: false,
  regex: `^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$` // Hex color without alpha
}

export default {
  name: 'EditMapModal',
  data: function () {
    return {
      form: {
        name: null,
        color: null
      },
      params: {
        id: null,
        name: null,
        color: null,
        onSuccess: (data) => {}
      },
      colorData: {
        hex: DEFAULT_COLOR
      },
      modalWidth: MODAL_WIDTH,
      nameValidator: NAME_VALIDATOR,
      colorValidator: COLOR_VALIDATOR,
      loading: false
    }
  },
  components: {
    'sketch-picker': Sketch
  },
  created: function () {
    this.modalWidth = window.innerWidth < MODAL_WIDTH ? MODAL_WIDTH / 2 : MODAL_WIDTH
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
    },
    params: {
      handler: function (data) {
        this.form.name = data.name
        this.form.color = data.color
      }
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
    validateBeforeSubmit: function () {
      this.$validator.validateAll()
    },
    submit: async function () {
      try {
        // Determine if there are any validation errors
        let result = await this.$validator.validateAll()
        if (!result) return

        this.loading = true

        let data = {
          map: {
            name: this.form.name || this.params.name,
            color: this.form.color || this.params.color
          }
        }

        let url = `http://localhost:5000/api/map/${this.params.id}`
        let response = await axios.post(url, data, generateConfig({
          email: this.$store.state.user.email
        }))

        // Close this modal
        this.close(true)

        let map = response.data.map
        if (this.params.onSuccess) {
          this.params.onSuccess(map)
        }
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

      this.$modal.hide('edit-map-modal')
    }
  }

}
</script>

<style lang="scss">
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

.v--modal-overlay .v--modal-box {
  overflow: visible !important;
}
</style>
