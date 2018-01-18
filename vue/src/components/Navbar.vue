<template>
  <nav class="navbar is-link">
    <div class="navbar-brand">
      <a class="navbar-item" href="https://bulma.io">
        AR-Top
      </a>
    </div>
    <div class="navbar-end">
      <div class="navbar-item has-dropdown" v-bind:class="{ 'is-active': active }"
           v-on:click="toggle_dropdown()" v-if="token">
        <a class="navbar-link">
          {{ email }}
        </a>
        <div class="navbar-dropdown">
          <a class="navbar-item">
            Editor
          </a>
          <a class="navbar-item">
            Maps
          </a>
          <hr class="navbar-divider">
          <a class="navbar-item">
            Sign out
          </a>
        </div>
      </div>
      <div class="navbar-item" v-else="token">
        <div class="field is-grouped">
          <p class="control">
            <router-link class="button is-primary" to="/auth">
              SIGN IN
            </router-link>
          </p>
          <p class="control">
            <router-link class="button is-primary" to="/register">
              SIGN UP
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Navbar',
  data: function () {
    return {
      active: false
    }
  },
  computed: {
    ...mapGetters([
      'email',
      'token'
    ])
  },
  methods: {
    toggle_dropdown: function () {
      this.active = !this.active
    }
  }
}
</script>

<style lang="scss">
@import '~bulma/bulma.sass';
</style>
