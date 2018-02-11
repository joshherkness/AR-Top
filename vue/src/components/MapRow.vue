<template>
  <tr>
    <td class="is-narrow">{{ name }}</td>
    <td class="is-narrow">
      <span class="tag is-light">{{ width }} x {{depth}}</span>
    </td>
    <td class="is-narrow">
      <span class="tag is-light">{{ color }}</span>
    </td>

    <!-- Blank cell used for padding -->
    <td></td>

    <!-- Controls -->
    <td class="is-narrow">
      <div class="field is-grouped">
        <p class="control">
          <router-link class="button is-link level-item" :to="{ name: 'editor', params: { id: oid }}">Open</router-link>
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
    </td>
  </tr>
</template>

<script>
export default {
  name: 'MapRow',
  props: ['name', 'oid', 'color', 'width', 'depth']
}
</script>
