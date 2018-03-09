<template>
  <tr v-on:click="onOpen"
    style="cursor: pointer;">
    <td class="is-narrow">
      <div class="color-tag"
        :style="{'background-color': color}">
      </div>
    </td>
    <td class="">{{ name }}</td>
    <td class="">
      {{ updated.$date | date }}
    </td>

    <!-- Blank cell used for padding -->
    <td></td>

    <!-- Controls -->
    <td class="is-narrow">
      <div class="field is-grouped">
        <a class="control button is-link is-small"
          @click="onOpen">
          Open
        </a>
        <div class="dropdown is-hoverable is-right">
          <div class="dropdown-trigger">
            <p class="field">
              <a class="button is-white is-small">
                <span class="icon">
                  <i class="mdi mdi-dots-vertical" />
                </span>
              </a>
            </p>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a class="dropdown-item" @click.stop="onEdit">
                Edit
              </a>
              <a class="dropdown-item has-text-danger" @click.stop="onDelete">
                Delete
              </a>
            </div>
          </div>
        </div>
      </div>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'MapRow',
  props: ['name', 'oid', 'color', 'width', 'depth', 'updated'],
  methods: {
    onOpen: function () {
      this.$router.push({
        name: 'editor',
        params: {
          id: this.oid
        }})
    },
    onEdit: function () {
      this.$modal.show('edit-map-modal', {
        id: this.oid,
        name: this.name,
        color: this.color
      })
    },
    onDelete: function () {
      this.$modal.show('delete-map-modal', {
        id: this.oid,
        name: this.name
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.color-tag {
  border-radius: 50%;
  border: 1px solid #eee;
  margin-top: 0.25rem;
  height: 1rem;
  width: 1rem;
}
</style>