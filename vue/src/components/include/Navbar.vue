<template>
  <nav class="navbar has-shadow" style="z-index: 1000">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        AR-Top
      </router-link>
      <router-link 
        class="navbar-item" 
        v-if="token" :to="{'path': '/maps'}" replace>
        My Library
      </router-link>
      <a class="navbar-item" v-if="token" @click="$modal.show('create-map-modal')">
        Editor
      </a>
      <div 
        class="navbar-burger burger" 
        @click="toggleCollapse"
        :class="{ 'is-active': collapseActive }">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
    <div class="navbar-menu" :class="{ 'is-active': collapseActive }">
      <div class="navbar-end">
        <div class="navbar-item has-dropdown is-hoverable" v-if="session">
          <a class="navbar-link is-hidden-touch">
            Session
          </a>
          <div class="navbar-dropdown">
            <a class="navbar-item is-expanded">
              <p>Invite code: <span class="tag is-link">{{ session.code }}</span></p>
            </a>
            <hr class="dropdown-divider">
            <a class="navbar-item is-expanded">
              <p>Displayed map: <span class="tag is-link">{{ session.mapName }}</span></p>
            </a>
            <hr class="dropdown-divider">
            <a class="navbar-item has-text-danger" @click="removeSession">
              Close session
            </a>
          </div>
        </div>
        <div class="navbar-item has-dropdown is-hoverable" v-if="token">
          <a class="navbar-link is-hidden-touch">
            {{ email }}
          </a>
          <div class="navbar-dropdown is-boxed">
            <a class="navbar-item has-text-danger" @click="clearStore">
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
    </div>
  </nav>
</template>

<script>
import store from '@/store/store'
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'Navbar',
  data: function () {
    return {
      collapseActive: false
    }
  },
  computed: {
    ...mapGetters([
      'email',
      'token',
      'session'
    ])
  },
  methods: {
    ...mapActions([
      'removeSession'
    ]),
    toggleCollapse: function () {
      this.collapseActive = !this.collapseActive
    },
    clearStore: function () {
      store.dispatch('signOutUser')
      store.dispatch('removeAllMaps')
    }
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
