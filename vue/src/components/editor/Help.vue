<template>
  <div class="box">
    <div class="help-container">
      <h1 class="title is-5">Help</h1>
      <hr>
      <div class="content">
        <p><b>Click + drag</b> to adjust angle.</p>
        <p><b>Scroll</b> zoom.</p>
        <p>
          Select 
          <i class="mdi mdi-cube-outline"></i>
          or <b>1</b> to switch to voxel mode. Hover 
          <i class="mdi mdi-cube-outline"></i>
          to switch change voxel color
        </p>
        <p>
          Select 
          <i class="mdi mdi-eraser"></i>
          or <b>2</b> to switch to erase mode.
        </p>
        <p><b>Click</b> on the grid to use a tool.</p>
        <p>Click on <b>Save</b> to save your progress.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Help'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import '~bulma/bulma.sass';

.help-container {
  min-width: 300px;
}
</style>
