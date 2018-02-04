<template>
  <div class="box">
    <div class="box-header">
      <h5 class="is-size-4 has-text-weight-semibold">{{ name }}</h5>
      <div class="dropdown is-hoverable is-up">
        <div class="dropdown-trigger">
          <p class="field">
          <a class="button is-medium">
            <span class="icon">
              <i class="mdi mdi-dots-vertical" />
            </span>
          </a>
          </p>
        </div>
        <div class="dropdown-menu" id="dropdown-menu" role="menu">
          <div class="dropdown-content">
            <a class="dropdown-item" @click="$modal.show('edit-map-modal', {id: oid, name: name, color: color, onSuccess: onEditSuccess})">
              Edit
            </a>
            <a class="dropdown-item" @click="$modal.show('delete-map-modal', {id: oid, name: name, onSuccess: onDeleteSuccess})">
              Delete
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="content">
      <p>Map size: {{ width *  depth }}</p> 
    </div>
    <div class="buttons is-pulled-right">
      <router-link class="button is-success" :to="{ name: 'Editor', params: { id: oid }}">Open</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapCard',
  props: ['name', 'oid', 'color', 'width', 'depth', 'onDeleteSuccess', 'onEditSuccess']
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
.box {
  flex: 0 0 calc((100% / 3) - 4em);
  height: 100%;
  margin: 0 2em 1em;
}

.box-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.field .button {
  border-color: $white;
}
</style>
