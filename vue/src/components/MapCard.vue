<template>
  <div class="wrapper">
    <div class="box">
      <div class="box-header">
        <div class="title is-6">{{ name }}</div>
        <div class="dropdown is-hoverable is-right">
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
              <a class="dropdown-item" @click="$modal.show('edit-map-modal', {id: oid, name: name, color: color})">
                Edit
              </a>
              <a class="dropdown-item has-text-danger" @click="$modal.show('delete-map-modal', {id: oid, name: name})">
                Delete
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        <p class="subtitle is-6">
          Size: <span class="tag is-light"> {{ width }} x {{depth}}</span>
        </p>
        <p>
          Color: <span class="tag is-light"> {{ color }}</span>
        </p>
      </div>
      <div class="level">
        <div class="level-left"></div>
        <div class="level-right">
          <router-link class="button is-link level-item" :to="{ name: 'editor', params: { id: oid }}">Open</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapCard',
  props: ['name', 'oid', 'color', 'width', 'depth']
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';
.wrapper {
  flex: 0 0 25%;
  height: 100%;

  padding: 0.75rem;
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
