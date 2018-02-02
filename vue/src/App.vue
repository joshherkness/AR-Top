<template>
  <div id="app">
    <create-map-modal/>
    <delete-map-modal/>
    <router-view/>
  </div>
</template>

<script>
import CreateMapModal from '@/components/CreateMapModal'
import DeleteMapModal from '@/components/DeleteMapModal'

export default {
  name: 'app',
  components: {
    CreateMapModal,
    DeleteMapModal
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
  color: #2c3e50;
}
</style>
