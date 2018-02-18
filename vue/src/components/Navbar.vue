<template>
  <nav class="navbar has-shadow" style="z-index: 1000">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        AR-Top
      </router-link>
      <router-link 
        class="navbar-item" 
        v-if="token" :to="{'name': 'library'}" replace>
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
        <session-manager/>
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
              <router-link class="button is-link" :to="{ name : 'login'}">
                Sign in
              </router-link>
            </p>
            <p class="control">
              <router-link class="button is-light" :to="{ name : 'register'}">
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
import SessionManager from '@/components/SessionManager'
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
      'token'
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
  },
  components: {
    SessionManager
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
