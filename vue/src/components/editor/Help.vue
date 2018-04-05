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
          or <b>1</b> to switch to add mode.
        </p>
        <p>
          Select 
          <i class="mdi mdi-eraser"></i>
          or <b>2</b> to switch to erase mode.
        </p>
        <p>
          Select 
          <i class="mdi mdi-cursor-move"></i>
          or <b>3</b> to switch to move mode.
        </p>
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
