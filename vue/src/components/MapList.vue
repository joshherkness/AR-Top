<template>
  <div>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th>Name</th>
          <th>Size</th>
          <th>Color</th>

          <!-- Blank columns used for right aligned controls -->
          <th></th>
          <th></th>
        </tr>
      </thead>

      <!-- For header alignment -->
      <tbody class="empty">
        <td class="is-narrow"></td>
        <td class="is-narrow"></td>
        <td class="is-narrow"></td>
        <td></td>
        <td class="is-narrow"></td>
      </tbody>
    </table>
    <div class="table-content">
      <table class="table is-fullwidth">
        <tbody>
          <map-row v-for="map in maps"
          :key="map._id.$oid"
          v-bind:name="map.name"
          v-bind:oid="map._id.$oid"
          v-bind:color="map.color"
          v-bind:depth="map.depth"
          v-bind:width="map.width"/>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import MapRow from '@/components/MapRow'

export default {
  name: 'MapList',
  props: ['maps'],
  components: {
    MapRow
  }
}
</script>

<style lang="scss" scoped>
.table-content {
  max-height: 465px;
  overflow: auto; 
}

.empty {
  visibility: collapse;
}
</style>
