<template>
  <div class="hero is-fullheight">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered">
          <div class="column is-4 is-offset-4">

            <!-- Error message, only show this when there is an error -->
            <article class="message is-danger" v-show="error">
              <div class="message-header">
                <p>Error</p>
                <button v-on:click="closeError" class="delete" aria-label="delete"></button>
              </div>
              <div class="message-body">
                {{ error }}
              </div>
            </article>

            <div class="box">
              <h1 class="title is-4">Sign In</h1>

              <form @submit.prevent="validateBeforeSubmit">
                <!-- Email field -->
                <div class="field">
                  <label class="label">Email</label>
                  <div class="control">
                    <input
                      name="email"
                      v-model="email"
                      v-validate="emailValidator"
                      class="input"
                      type="text"
                      placeholder="Enter your email"
                      :class="{'is-danger': errors.has('email')}">
                  </div>
                  <span v-show="errors.has('email')" class="help is-danger">{{ errors.first('email') }}</span>
                </div>

                <!-- Password field -->
                <div class="field">
                  <label class="label">Password</label>
                  <div class="control">
                    <input
                      name="password"
                      v-on:keyup.enter="signin"
                      v-model="password"
                      v-validate="passwordValidator"
                      class="input"
                      type="password"
                      placeholder="Enter your password"
                      :class="{'is-danger': errors.has('password')}">
                  </div>
                  <span v-show="errors.has('password')" class="help is-danger">{{ errors.first('password') }}</span>
                </div>

                <hr>

                <!-- Buttons -->
                <div class="field">
                  <div class="control">
                    <button
                      v-on:click="signin"
                      class="button is-link"
                      type="submit"
                      :disabled="errors.any()"
                      :class="{'is-loading': loading}">
                      Sign In
                    </button>
                  </div>
                </div>
              </form>
            </div>
            <p>Need an account? <router-link :to="{name: 'register'}">Register</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import router from '@/router'
import { API } from '@/api/api'

// Validator used for the email field
const EMAIL_VALIDATOR = {
  required: true,
  email: true,
  max: 255
}

// Validator used for the password field
const PASSWORD_VALIDATOR = {
  required: true,
  min: 8,
  max: 255
}

export default {
  name: 'Authentication',
  data: function () {
    return {
      email: '',
      password: '',
      error: '',
      loading: false,
      emailValidator: EMAIL_VALIDATOR,
      passwordValidator: PASSWORD_VALIDATOR
    }
  },
  methods: {
    ...mapActions([
      'updateUser',
      'setSession'
    ]),
    signin: async function () {
      try {
        // Check for input validation errors before we try to authenticate
        if (this.errors.any()) {
          return
        }

        // Attempt to register the user
        this.loading = true

        // generate payload for JWT
        const payload = {
          email: this.email,
          password: this.password
        }

        let user = await API.authenticate(payload)

        // Update the local user
        this.updateUser(user)

        // Update the local session, if any exist for the current user
        API.getCurrentSession().then((session) => {
          if (session) {
            this.setSession(session)
          }
        // eslint-disable-next-line
        }).catch((err) => {
          // In case the user does not own any sessions, we don't want
          // to throw an error here.
        })

        // Navigate to home route
        router.push('/library')
      } catch (err) {
        this.error = err.response.data.error
      }

      this.loading = false
    },

    closeError: function () {
      this.error = null
    },

    validateBeforeSubmit: function () {
      this.$validator.validateAll()
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
