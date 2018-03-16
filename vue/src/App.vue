<template>
  <div id="app">
    <create-map-modal/>
    <delete-map-modal/>
    <edit-map-modal/>
    <session-modal/>

    <!-- Only show the navbar for required routes-->
    <Navbar v-if="$route.meta.requiresNavbar"/>

    <!-- Main app content -->
    <div style="flex: 1; overflow: hidden;">
      <router-view style="height: 100%;"/>
    </div>

    <!-- Only show the session manager for routes that require it -->
    <SessionManager v-if="$route.meta.requiresManager && session_id"/>
  </div>
</template>

<script>
import CreateMapModal from '@/components/CreateMapModal'
import DeleteMapModal from '@/components/DeleteMapModal'
import SessionManager from '@/components/SessionManager'
import EditMapModal from '@/components/EditMapModal'
import SessionModal from '@/components/SessionModal'
import { mapGetters } from 'vuex'
import Navbar from '@/components/Navbar'

export default {
  name: 'app',
  components: {
    CreateMapModal,
    DeleteMapModal,
    EditMapModal,
    SessionModal,
    SessionManager,
    Navbar
  },
  computed: {
    ...mapGetters([
      'session_id'
    ])
  }
}
</script>

<style lang="scss">
// Import bulma site wide
@import '~bulma/bulma.sass';
$mdi-font-path: '~mdi/fonts/';
@import '~mdi/scss/materialdesignicons';

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  display: flex;
  flex-flow: column;
}
</style>
