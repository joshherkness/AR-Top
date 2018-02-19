<template>
  <modal name="session-modal"
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
        <h1 class="title is-4">Create Session</h1>

        <!-- Content field -->
        <div class="field content">
          <p>Create a session to show your map to your party.</p>
        </div>

        <!-- Map dropdown -->
        <div class="field">
          <label class="label">Available Maps</label>
          <div class="control">
            <div class="select">
              <select v-model="selected">
                <option :value="null" disabled>Select Map</option>
                <option v-for="map in maps" :value="map._id.$oid">
                  {{ map.name }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="field is-grouped is-grouped-right">
          <p class="control">
            <button 
              v-on:click="submit" 
              class="button is-link" 
              :disabled="!isSubmitEnabled">Submit</button>
            <button v-on:click="close" class="button is-white">Cancel</button>
          </p>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import { API } from '@/api/api'
import { mapGetters } from 'vuex'
import store from '@/store/store'
// Specifies the width of this modal
const MODAL_WIDTH = 500
export default {
  name: 'SessionModal',
  data: function () {
    return {
      modalWidth: MODAL_WIDTH,
      selected: null
    }
  },
  computed: {
    ...mapGetters([
      'maps'
    ]),
    isSubmitEnabled: function () {
      return this.selected !== null
    }
  },
  methods: {
    beforeOpened (event) {
      this.$emit('before-opened', event)
    },
    beforeClosed (event) {
      this.$emit('before-closed', event)
    },
    submit: async function () {
      const session = await API.createSession(this.selected)
      store.dispatch('setSession', session)
      this.$modal.hide('session-modal')
    },
    close: function () {
      this.$modal.hide('session-modal')
    }
  }
}
</script>
