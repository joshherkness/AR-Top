<template>
  <div class="box" style="display: flex; flex-flow: row; padding: 0; height: 306px;">
    <div style="flex: 1; display: flex; flex-flow: column; ">
      <!-- Search bar -->
      <nav class="panel is-marginless" style="width: 200px;">
        <div class="panel-block">
          <p class="control has-icons-left">
          <input 
            class="input" 
            type="text" 
            placeholder="search"
            v-model="filter">
          <span class="icon is-small is-left">
            <i class="mdi mdi-magnify" />
          </span>
          </p>
        </div>
      </nav>
      <!-- List -->
      <nav class="panel"
        style="flex: 1; overflow: scroll; height: 100%">
        <a class="panel-block" v-for="data in filteredList"
          :key="data.type" 
          @click="setType(data.type)">
          <span v-if="entityData.type && entityData.type === data.type" class="panel-icon">
            <i class="mdi mdi-check"/>
          </span>
          {{ data.display }}
        </a>

        <!-- No results panel -->
        <div v-if="filteredList.length <= 0" class="panel-block is-disabled">
          <i>No results</i>
        </div>
      </nav>
    </div>
    <div style="flex: 0 1 auto;">
      <sketch-picker v-model="entityData.color"></sketch-picker>
    </div>
  </div>
</template>

<script>
import { Sketch } from 'vue-color'
import { ENTITY_DATA } from '@/components/editor/PreloadedObjects'

export default {
  name: 'entity-selector',
  components: {
    'sketch-picker': Sketch
  },
  props: ['entityData', 'entityList'],
  data: function () {
    return {
      filter: ''
    }
  },
  computed: {
    filteredList: function () {
      return ENTITY_DATA.filter((data) => {
        return data.display.toLowerCase().includes(this.filter.toLowerCase())
      })
    }
  },
  methods: {
    setType: function (type) {
      this.entityData.type = type
    }
  }
}
</script>

<style lang="scss">
.box {
  overflow: hidden;
}

.vc-sketch {
  border-radius: 0;
}
</style>
