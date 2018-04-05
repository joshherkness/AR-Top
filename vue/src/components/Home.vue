<template>
  <div style="overflow: scroll;">
    <section class="hero is-large is-link">
      <div class="hero-body">
        <div class="container">
          <div style="display: grid;
              grid-template-columns: 1fr;
              grid-gap: 0px 0px;
              justify-items: center;">
            <figure class="image" style="margin-top: 1rem; width: 25%">
              <img src="@/assets/artop-logo-light.svg">
            </figure>
          </div>
          <br>
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
              <span class="has-text-info icon">
                <i class="mdi mdi-numeric-1-box-outline"></i>
              </span> Register
            </h1>
            <router-link class="button is-link" :to="{ name : 'register'}">
              Register
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
              <span class="has-text-info icon">
                <i class="mdi mdi-numeric-2-box-outline"></i>
              </span> Create a map
            </h1>
            <p>
              Once you've registered for an account, you can start creating
              maps. This can be done by navigating to <i><b>My Library</b></i>
              and clicking <i><b>Create a map</b></i> in the top right.
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
             <span class="has-text-info icon">
                <i class="mdi mdi-numeric-3-box-outline"></i>
              </span> Open a session
            </h1>
            <div class="content">
              <p>
                Once you are ready to have others view your map, you can click
                <i><b>Open session</b></i> in the navigation bar revealing the 
                <i><b>Session manager</b></i> at the bottom of your screen, where
                you can find your invitation code.
              </p>
            </div>
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
              <span class="has-text-info icon">
                <i class="mdi mdi-numeric-4-box-outline"></i>
              </span> Print our logo
            </h1>
            <div class="content">
              <p>
                This image is used as a target on which the mobile application will render 
                your map. You can print this image using the button below.
              </p>
            </div>
            <button class="button is-link" v-on:click="openImageTarget">
              Print image target
            </button>
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
              <span class="has-text-info icon">
                <i class="mdi mdi-numeric-5-box-outline"></i>
              </span> Gather your party
            </h1>
            <div class="content">
              <p>
                Have the members of your party download our mobile application.
              </p>
              <p>
                They can connect to your session by entering your invitation 
                code. Once connected, they can simply focus their cameras on the 
                printed logo to view your map.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import imageTarget from '@/assets/target-image.png'

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
