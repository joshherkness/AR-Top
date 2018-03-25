<template>
  <div style="display: flex; flex-flow: column; margin: 10px;">
    <label class="label">Type</label>
    <div style="flex: 1; display: flex; flex-flow: column;">
      <!-- Search bar -->
      <nav class="panel is-marginless">
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
        style="flex: 1; overflow: scroll;">
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
    <hr>
    <div style="flex: 0 1 auto;">
      <!-- Color -->
      <div class="field">
        <label class="label">Color</label>
        <!-- Color picker dropdown -->
        <div class="dropdown is-hoverable is-up is-right is-pulled-right"
          style="width: 100%;">
          <div class="dropdown-trigger"
            style="width: 100%;">
            <button class="button is-static" style="width: 100%;">
              <span class="color-swatch" :style="{'background-color': entityData.color.hex}"></span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu4" role="menu">
            <sketch-picker v-model="entityData.color"></sketch-picker>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Sketch } from 'vue-color'
import { ENTITY_DATA, MODEL_DATA } from '@/components/editor/PreloadedObjects'

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
      return ENTITY_DATA.concat(MODEL_DATA).filter((data) => {
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
