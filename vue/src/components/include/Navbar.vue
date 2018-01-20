<template>
  <nav class="navbar is-white">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        AR-Top
      </router-link>
    </div>
    <div class="navbar-end">
      <router-link class="navbar-item" v-if="token" to="editor">
        Editor
      </router-link>
      <router-link class="navbar-item" v-if="token" to="maps">
        Maps
      </router-link>
      <div class="navbar-item has-dropdown is-hoverable" v-if="token">
        <a class="navbar-link">
          {{ email }}
        </a>
        <div class="navbar-dropdown">
          <a class="navbar-item is-danger" @click="signOutUser">
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

<style lang="scss">
@import '~bulma/bulma.sass';

.is-danger {
  color: $red;
}

.navbar-dropdown a.navbar-item.is-danger {
  &:hover {
    color: $red;
  }
}
</style>
