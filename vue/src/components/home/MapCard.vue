<template>
  <div class="box">
    <h5 class="title is-5">{{ name }}</h5>
    <div class="content">
      <p>Map size: {{ width *  depth }}</p> 
    </div>
    <div class="buttons is-pulled-right">
      <span class="button is-info" @click="$modal.show('edit-map-modal', {name: name, width: width, depth: depth})">Edit</span>
      <span class="button" @mouseover="mouseOver" @mouseleave="mouseLeave" v-bind:class="[isHovered ? 'is-danger' : 'is-light']" @click="$modal.show('delete-map-modal', {name: name})">Delete</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapCard',
  props: ['name', 'width', 'depth'],
  data: function () {
    return {
      isHovered: false
    }
  },
  methods: {
    mouseOver: function () {
      this.isHovered = true
    },
    mouseLeave: function () {
      this.isHovered = false
    }
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
.box {
  flex: 0 0 calc((100% / 3) - 4em);
  height: 100%;
  margin: 0 2em 1em;
}
</style>
