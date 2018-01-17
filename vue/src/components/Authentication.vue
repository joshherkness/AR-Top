<template>
  <div class="columns">
    <div class="container column">
      <div class="container is-fluid">
        <div class="card">
          <div class="card-header">
            <h1 class="card-header-title">Authenticate</h1>
          </div>
          <div class="card-content">
            <div class="field">
              <label class="label">Email</label>
              <div class="control">
                <input v-model="email" class="input" type="text" placeholder="e.g johnsmith@google.com">
              </div>
            </div>
            <div class="field">
              <label class="label">Password</label>
              <div class="control">
                <input v-model="password" class="input" type="password" placeholder="Password">
              </div>
            </div>
            <div class="field">
              <p class="control">
              <button  v-on:click="signin" class="button is-info">
                Sign In
              </button>
              </p>
            </div>
          </div>
        </div>
      </div>
      <article class="message is-danger" v-bind:class="{ 'is-invisible': active }">
        <div class="message-header">
          <p>Error</p>
          <button v-on:click="toggle" class="delete" aria-label="delete"></button>
        </div>
        <div class="message-body">
          {{ message }}
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from './../router/index.js'
var qs = require('qs')
export default {
  name: 'Authentication',
  data: function () {
    return {
      email: '',
      password: '',
      message: '',
      active: true
    }
  },
  methods: {
    signin: function () {
      let vue = this
      axios.post('http://localhost:5000/api/auth',
        qs.stringify({
          'email': this.email,
          'password': this.password
        }))
        .then(function (response) {
          router.push('/') // Redirect home
        })
        .catch(function (error) {
          let response = error.response
          vue.active = !vue.active
          vue.message = response.data.error
        })
    },

    toggle: function () {
      this.active = !this.active
    }
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';

.card-header {
  background-color: $cyan;
}

.card-header-title {
  color: $white;
}

.label {
  text-align: left;
}

.input {
  width: 90%;
}

.message {
  margin-top: 1em;
}
</style>
