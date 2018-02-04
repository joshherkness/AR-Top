<template>
  <nav class="navbar is-transparent">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        AR-Top
      </router-link>
    </div>
    <div class="navbar-start">
      <router-link 
        class="navbar-item" 
        v-if="token" :to="{'path': '/maps'}" replace>
        My Library
      </router-link>
      <a class="navbar-item" v-if="token" @click="$modal.show('create-map-modal')">
        Editor
      </a>
    </div>
    <div class="navbar-end">
      <div class="navbar-item has-dropdown is-hoverable" v-if="token">
        <a class="navbar-link">
          {{ email }}
        </a>
        <div class="navbar-dropdown is-boxed">
          <a class="navbar-item has-text-danger" @click="signOutUser">
            Sign out
          </a>
        </div>
      </div>
      <div class="navbar-item" v-else="token">
        <div class="field is-grouped">
          <p class="control">
            <router-link class="button is-primary" to="/auth">
              Sign in
            </router-link>
          </p>
          <p class="control">
            <router-link class="button is-primary" to="/register">
              Sign up
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'Navbar',
  computed: {
    ...mapGetters([
      'email',
      'token'
    ])
  },
  methods: {
    ...mapActions([
      'signOutUser'
    ])
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
