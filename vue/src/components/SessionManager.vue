<template>
  <div class="navbar-item has-dropdown is-hoverable">
    <a class="navbar-link is-hidden-touch">
      Session
    </a>
    <div class="navbar-dropdown" v-if="session">
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
    <div class="navbar-dropdown" v-else="session" @click="">
      <a class="navbar-item has-text-link">
        Open session
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'SessionManager',
  computed: {
    ...mapGetters([
      'session'
    ])
  },
  methods: {
    ...mapActions([
      'removeSession'
    ]),
  }
}
</script>
