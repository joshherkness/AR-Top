<template>
  <tr>
    <td>{{ name }}</td>
    <td><span class="tag is-light">{{ width }} x {{depth}}</span></td>
    <td>
      <div class="wrapper">
        <span class="tag is-light">{{ color }}</span>
        <div class="field is-grouped">
          <p class="control">
            <router-link class="button is-link level-item" :to="{ name: 'Editor', params: { id: oid }}">Open</router-link>
          </p>
          <p class="control">
            <div class="dropdown is-hoverable is-right">
              <div class="dropdown-trigger">
                <p class="field">
                  <a class="button is-white">
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
          </p>
        </div>
      </div>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'MapList',
  props: ['name', 'oid', 'color', 'width', 'depth'],

}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';

.wrapper {
  display: flex;
  justify-content: space-between;
}
</style>
