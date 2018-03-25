<template>
  <div class="editor columns is-gapless">
    <!-- Canvas used to render the three.js map scene-->
    <div v-show="!loading" ref='canvas' id='canvas'/>

    <div class="column">
      <div class="overlay">
        <!-- Top toolbar -->
        <div v-if="!loading"
          class="level"
          style="z-index: 10;">
          <div class="level-left">
            <div class="level-item">
              <span class="tag is-white title is-5">{{ name }}</span>
            </div>
            <div class="level-item">
              <!-- Save button -->
              <div class="control">
                <div class="button is-link"
                    :class="{'is-loading': saving}"
                    v-on:click="save">
                  <span>Save</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Flex child used to seperate top and bottom toolbar -->
        <div style="flex: 1;"></div>

        <!-- Bottom toolbar -->
        <div class="level"
          style="z-index: 10;">
          <div class="level-left"></div>
          <div class="level-right">
            <div class="level-item">
              <div class="control">
                <div class="dropdown is-hoverable is-right is-up"
                    :class="{'is-active': !hasSeenEditorHelp}">
                  <div class="dropdown-trigger">
                    <div class="button is-light"
                      aria-haspopup='true'
                      aria-controls='help-dropdown'
                      v-on:mouseover="setHasSeenEditorHelp">
                      <span class="icon is-medium">
                        <i class="mdi mdi-help"></i>
                      </span>
                    </div>
                    <div class="dropdown-menu" role='menu'>
                      <help></help>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading spinner -->
        <div v-if="loading" class="loading-spinner"/>
      </div>
    </div>

    <div class="column is-narrow"
      style="z-index: 10;">
      <div class="tools">
        <div class="tabs" v-if="toolManager">
          <ul>
            <li v-for="tool in toolManager.tools"
              :key="tool.type"
              :class="{'is-active': toolManager.tool.type === tool.type}">
              <a @click="toolManager.selectTool(tool.type)">
                <span class="icon">
                  <i class="mdi"
                    :class="tool.icon"></i>
                </span>
              </a>
            </li>
          </ul>
        </div>
        <div v-if="toolManager && toolManager.tool.type === 'place'">
          <entity-selector v-bind:entityData="toolManager.tool.options"></entity-selector>
        </div>
      </div>
    </div>

    <!-- here -->
  </div>
</template>

<script>
import { API } from '@/api/api'
import { mapGetters, mapActions } from 'vuex'

import { ToolManager } from '@/components/editor/ToolManager'
import { GridDirector } from './GridDirector'
import { Grid } from './Grid'
import { Sketch } from 'vue-color'
import * as THREE from 'three'
import Help from './Help'
import EntitySelector from './EntitySelector'
var OrbitControls = require('three-orbit-controls')(THREE)

export default {
  name: 'Editor',
  data: function () {
    return {
      canvas: null,
      camera: null,
      controls: null,
      renderer: null,
      raycaster: null,
      mouse: null,
      grid: null,
      loading: false,
      saving: false,
      toolManager: null
    }
  },
  components: {
    'help': Help,
    'entity-selector': EntitySelector,
    'sketch-picker': Sketch
  },
  computed: {
    ...mapGetters([
      'hasSeenEditorHelp'
    ]),
    name () {
      if (!this.grid) {
        return ''
      }

      return this.grid.name
    },
    toolType () {
      if (!this.toolManager || !this.toolManager.tool) {
        return ''
      }

      return this.toolManager.tool.type
    }
  },
  watch: {
    grid (grid) {
      // Create a new director
      // TODO: Remove the need to create a new director
      if (this.director) {
        this.director.removeEventListener('update')
      }
      this.director = new GridDirector({ scale: 50 })

      this.director.load(grid).then(() => {
        this.setup()
      }).catch(err => {
        console.log(err)
      })
    }
  },

  /**
   * This function is called when the router first navigates to this renderer.
   */
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.load(to.params.id)
    })
  },

  /**
   * This function is called when the particular route is updated, for example
   in the case where only a particular route parameter changes.
   */
  beforeRouteUpdate (to, from, next) {
    this.load(to.params.id)
    next()
  },
  mounted () {
    this.loading = true

    // Create the director
    this.director = new GridDirector({ scale: 16 })

    // Create the renderer
    this.renderer = new THREE.WebGLRenderer()
    this.renderer.setPixelRatio(window.devicePixelRatio)
    this.renderer.setClearColor(0xffffff)

    // Attach to the container
    this.canvas = this.$refs.canvas
    this.canvas.appendChild(this.renderer.domElement)

    // Create the camera
    const cameraFov = 45
    this.camera = new THREE.PerspectiveCamera(cameraFov, window.innerWidth / window.innerHeight, 1, 10000)

    // Create the orbit controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement)
    this.controls.enablePan = false
    this.controls.maxPolarAngle = (Math.PI / 2) + 0.1
    this.controls.zoomSpeed = 1.5
    this.camera.lookAt(new THREE.Vector3())
    this.controls.addEventListener('change', this.render)

    this.raycaster = new THREE.Raycaster()
    this.mouse = new THREE.Vector2()

    // Attach event listeners to the document
    this.canvas.addEventListener('mousemove', this.onDocumentMouseMove, false)
    this.canvas.addEventListener('mousedown', this.onDocumentMouseDown, false)
    this.canvas.addEventListener('mouseup', this.onDocumentMouseUp, false)
    document.addEventListener('keydown', this.onDocumentKeyDown, false)
    window.addEventListener('resize', this.onWindowResize, false)
  },
  methods: {
    ...mapActions([
      'setHasSeenEditorHelp'
    ]),
    load (id) {
      this.loading = true
      API.getMap(id).then(map => {
        this.loading = false
        this.grid = Grid.deserialize(map)
        this.grid.id = map._id.$oid
      }).catch(err => {
        this.loading = false
        console.log(err)
      })
    },
    setup () {
      // Create a new grid director
      this.director.addEventListener('update', (event) => {
        this.render()
      })

      // Update camera properties
      if (this.camera) {
        // Here, we ensure that our entire scene will begin within the bounds of
        // our camera
        const scalar = Math.max(this.director.scene.actualWidth, this.director.scene.actualHeight)
        this.camera.position.copy(new THREE.Vector3(1, 1, 1).multiplyScalar(scalar))

        // Since the camera has not changed, we need to convey this change to
        // the our controls, if there are any.
        if (this.controls) {
          this.controls.update()
        }
      }

      // Update orbit control properties
      if (this.controls) {
        this.controls.minDistance = 2 * this.director.scale || 50
      }

      this.toolManager = ToolManager.getInstance()

      // We need to call this so that the canvas will resize to the window
      this.onWindowResize()
    },
    render () {
      this.renderer.render(this.director.scene, this.camera)
    },
    onWindowResize () {
      this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight)
      this.render()
    },
    onDocumentMouseMove (event) {
      // Update mouse and raycaster
      let mouse = {
        x: (event.offsetX / window.innerWidth) * 2 - 1,
        y: -(event.offsetY / window.innerHeight) * 2 + 1
      }
      this.raycaster.setFromCamera(mouse, this.camera)

      let toolManager = ToolManager.getInstance()

      // Update the cursor position for the selection manager
      toolManager.onMouseMove(event, this.director, this.raycaster)
    },
    onDocumentMouseDown (event) {
      let toolManager = ToolManager.getInstance()
      toolManager.onMouseDown(event, this.director, this.raycaster)
    },
    onDocumentMouseUp (event) {
      let toolManager = ToolManager.getInstance()
      toolManager.onMouseUp(event, this.director, this.raycaster)
    },
    onDocumentKeyDown (event) {
      let toolManager = ToolManager.getInstance()
      toolManager.onKeyPress(event)
    },
    save () {
      if (!this.grid) {
        return
      }

      const id = this.grid.id
      if (!id) {
        throw new Error(`Grid property 'id' must be defined.`)
      }

      const data = {
        map: JSON.parse(this.grid.serialize())
      }

      this.saving = true
      API.updateMap(id, data).then((response) => {
        this.saving = false
        console.log(response)
      }).catch((err) => {
        this.saving = false
        console.log(err.response)
      })
    }
  },
  destroyed () {
    // Remove event listeners from orbit controls
    this.controls.dispose()

    // Remove event listeners from map
    this.director.removeEventListener('update', this.render, false)

    // Remove event listeners
    this.canvas.removeEventListener('mousemove', this.onDocumentMouseMove, false)
    this.canvas.removeEventListener('mousedown', this.onDocumentMouseDown, false)
    this.canvas.removeEventListener('mouseup', this.onDocumentMouseUp, false)
    document.removeEventListener('keydown', this.onDocumentKeyDown, false)
    window.removeEventListener('resize', this.onWindowResize, false)
  }
}
</script>

<style lang="scss" scoped>
@import '~bulma/bulma.sass';

#canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.loading-spinner {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0.5;
  &:after {
    @include loader;
    position: absolute;
    top: calc(50% - 1.0em);
    left: calc(50% - 1.0em);
    width: 2em;
    height: 2em;
    border-width: 0.25em;
  }
}

.overlay {
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-flow: column;
  padding: 30px;
}

.tools {
  border-left: 1px solid $border;
  width: 300px;
  background: white;
  height: 100%;

  .tabs {
    margin: 0;
  }
}
</style>
