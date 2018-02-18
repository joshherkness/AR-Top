<template>
  <div>
    <section class="hero is-large is-link">
      <div class="hero-body">
        <div class="container">
          <h1 class="title has-text-centered">
            AR Top
          </h1>
          <h2 class="subtitle has-text-centered">
            Let us define our world.
          </h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h1 class="title is-3 has-text-centered">
          How does it work?
        </h1>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="columns is-vcentered is-centered">
          <div class="column is-half">
            <h1 class="title is-4">
              <span class="has-text-info">Step 1:</span> Sign up
            </h1>
            <router-link class="button is-link" :to="{ name : 'register'}">
              Sign up
            </router-link>
          </div>
        </div>
      </div>
    </section>
    <hr>
    <section class="section">
      <div class="container">
        <div class="columns is-vcentered is-centered">
          <div class="column is-half">
            <h1 class="title is-4">
              <span class="has-text-info">Step 2:</span> Create a map
            </h1>
            <p>
              Once you've registered for an account, you can start creating
              maps. This can be done by navigating to your <i><b>Library</b></i>
              and clicking the <i><b>Create a map</b></i> button in the top right.
            </p>
          </div>
        </div>
      </div>
    </section>
    <hr>
    <section class="section">
      <div class="container">
        <div class="columns is-vcentered is-centered">
          <div class="column is-half">
            <h1 class="title is-4">
              <span class="has-text-info">Step 3:</span> Create a session
            </h1>
            <p>
              After your map is created, and you are ready to show it off, create a
              session.
            </p>
          </div>
        </div>
      </div>
    </section>
    <hr>
    <section class="section">
      <div class="container">
        <div class="columns is-vcentered is-centered">
          <div class="column is-half">
            <h1 class="title is-4">
              <span class="has-text-info">Step 4:</span> Print the target image
            </h1>
            <div class="content">
              <p>
                This image will be used by the mobile application to display an
                augmented render of your map, that can be seen by anyone in your
                session.
              </p>
            </div>
            <button class="button is-link" v-on:click="openImageTarget">
              Print image target
            </button>
            <figure class="image is-128x128" style="margin: 1rem;">
              <img src="@/assets/image-target.jpg">
            </figure>
          </div>
        </div>
      </div>
    </section>
    <hr>
    <section class="section">
      <div class="container">
        <div class="columns is-vcentered is-centered">
          <div class="column is-half">
            <h1 class="title is-4">
              <span class="has-text-info">Step 5:</span> Download the mobile app
            </h1>
            <p>
              Your friends can now download the mobile application, and join your
              session using the invitation code that was generated for you.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import imageTarget from '@/assets/image-target.jpg'

export default {
  name: 'Home',
  methods: {
    openImageTarget: function () {
      let imageWindow = window.open(imageTarget)
      imageWindow.print()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import '~bulma/bulma.sass';
</style>
