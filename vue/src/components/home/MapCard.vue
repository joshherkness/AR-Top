<template>
  <div class="box">
    <h5 class="title is-5">{{ name }}</h5>
    <div class="content">
      <p>Map size: {{ width *  depth }}</p> 
    </div>
    <div class="buttons is-pulled-right">
      <span class="button is-info" @click="$modal.show('edit-map-modal', {name: name, width: width, depth: depth})">Edit</span>
      <span class="button is-danger" @click="$modal.show('delete-map-modal', {name: name})">Delete</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapCard',
  props: ['name', 'width', 'depth']
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
.box {
  flex: 0 0 calc((100% / 3) - 1em);
  height: 100%;
  margin: 0.5em;
}
</style>
