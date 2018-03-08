<template>
  <div class="wrapper">
    <div class="box">
      <div class="box-header level">
        <div class="level-left">
          <div class="level-item">
            <span class="color-tag"
                :style="{'background-color': color}"/>
            <span class="title is-6">
              {{ name }}
            </span>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
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
        </div>
      </div>
      <div class="content">
        <p>
          <span class="title is-7">Last modified</span>
          <br/>
          <span class="subtitle is-7">{{ updated.$date | date }}</span>
        </p>
      </div>
      <a class="button is-link level-item"
        @click="onOpen">
        Open
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapCard',
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

.color-tag {
  border-radius: 50%;
  border: 1px solid #eee;
  margin-right: 10px;
  height: 1rem;
  width: 1rem;
}
</style>
