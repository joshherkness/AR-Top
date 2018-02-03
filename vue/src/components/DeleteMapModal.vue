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
              name="name"
              v-model="form.name"
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
              :disabled="!isSubmitEnabled">Delete</button>
            <button v-on:click="close" class="button is-white">Cancel</button>
          </p>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import axios from 'axios'
import { generateConfig } from '@/api/api'

// Specifies the width of this modal
const MODAL_WIDTH = 500

export default {
  name: 'DeleteMapModal',
  data: function () {
    return {
      modalWidth: MODAL_WIDTH,
      params: {
        id: '',
        name: '',
        onSuccess: (id) => {}
      },
      form: {
        name: ''
      }
    }
  },
  created: function () {
    this.modalWidth =
      window.innerWidth < MODAL_WIDTH ? MODAL_WIDTH / 2 : MODAL_WIDTH
  },
  computed: {
    isSubmitEnabled: function () {
      return this.form.name === this.params.name
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

    /**
     * Function is called when the form is submitted
     */
    submit: async function () {
      try {
        // Ensure that name and id params have been passed
        if (!this.params.name || !this.params.id) {
          throw new Error(`Params must be defined on component 'DeleteMapModal'`)
        }

        // Ensure that the name field and param match
        if (!this.isSubmitEnabled) {
          throw new Error(`Provided name field and actual name do not match`)
        }

        // Issue the request
        let url = `http://localhost:5000/api/map/${this.params.id}`
        axios.delete(url, generateConfig({
          email: this.$store.state.user.email
        }))

        // Successful callback
        if (this.params.onSuccess) {
          this.params.onSuccess(this.params.id)
        }

        // Close this modal
        this.close()
      } catch (err) {
        throw err
      }
    },

    /**
     * Close this modal
     */
    close: function (clear = false) {
      if (clear) {
        Object.assign(this.$data, this.$options.data())
      }

      this.$modal.hide('delete-map-modal')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
