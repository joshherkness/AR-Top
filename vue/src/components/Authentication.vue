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
      password: ''
    }
  },
  methods: {
    signin: function () {
      axios.post('http://localhost:5000/api/auth',
        qs.stringify({
          'email': this.email,
          'password': this.password
        }))
        .then(function (response) {
          router.push('/') // Redirect home
        })
        .catch(function (error) {
          console.log(error)
        })
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
</style>
