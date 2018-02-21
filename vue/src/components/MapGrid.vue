<template>
  <div class="map-cards">
    <map-card v-for="map in maps"
      :key="map._id.$oid"
      v-bind:name="map.name"
      v-bind:oid="map._id.$oid"
      v-bind:color="map.color"
      v-bind:depth="map.depth"
      v-bind:width="map.width"/>
  </div>
</template>

<script>
import MapCard from '@/components/MapCard'

export default {
  name: 'MapGrid',
  props: ['maps'],
  components: {
    MapCard
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
.map-cards {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  max-height: 465px;
  overflow: auto;
}
@media (max-width: 32em) {
  .map-cards {
    display: flex;
    flex-direction: column;
  }
}
</style>
