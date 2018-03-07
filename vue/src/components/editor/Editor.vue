<template>
  <div>
    <!-- Canvas used to render the three.js map scene-->
    <div v-show="!loading" ref='canvas' id='canvas'/>
   
    <!-- Overlay -->
    <div v-if="!loading"
      class="level" style="position: absolute; padding: 30px; width: 100%;">
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
      <div class="level-right">
        <div class="level-item">
          <div class="field has-addons">
            <div class="control">
              <div class="dropdown is-hoverable is-right">
                <div class="dropdown-trigger">
                  <div class="button is-light"
                    aria-haspopup='true'
                    aria-controls='color-picker-dropdown-menu'
                    :class="{'is-active': isModeAdd()}"
                    :style="{'color': hexColor}"
                    v-on:click="setModeAdd">
                    <span class="icon is-medium">
                      <i class="mdi mdi-cube-outline"></i>
                    </span>
                    <div class="is-size-7">1</div>
                  </div>
                  <div class="dropdown-menu" role='menu'>
                    <sketch-picker v-model="color"></sketch-picker>
                  </div>
                </div>
              </div>
            </div>
            <div class="control">
              <div class="button is-light"
                :class="{'is-active': isModeDelete()}"
                v-on:click="setModeDelete">
                <span class="icon is-medium">
                  <i class="mdi mdi-eraser"></i>
                </span>
                <div class="is-size-7">2</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Help menu -->
    <div class="field help-field">
      <div class="control">
        <div class="dropdown is-hoverable is-right is-up"
             :class="{'is-active': showHelp}">
          <div class="dropdown-trigger">
            <div class="button is-light"
              aria-haspopup='true'
              aria-controls='help-dropdown'
              v-on:click="showHelp = false"
              v-on:mouseover="showHelp = false">
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

    <!-- Loading spinner -->
    <div v-if="loading" class="loading-spinner"/>

  </div>
</template>

<script>
import { API } from '@/api/api'

import { GridDirector } from './GridDirector'
import { Grid } from './Grid'
import { ModelFactory } from './ModelFactory'
import { Sketch } from 'vue-color'
import * as THREE from 'three'
import { EditorMode } from './EditorMode'
import Help from './Help'
var OrbitControls = require('three-orbit-controls')(THREE)

let defaultColor = { hex: '#4A90E2' }

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
      color: defaultColor,
      mode: EditorMode.ADD,
      loading: false,
      saving: false,
      showHelp: true
    }
  },
  components: {
    'help': Help,
    'sketch-picker': Sketch
  },
  computed: {
    hexColor () {
      return this.color.hex
    },
    model () {
      return ModelFactory.createModel({
        type: 'voxel',
        position: new THREE.Vector3(), // Should this be an actual position
        color: this.hexColor
      })
    },
    name () {
      if (!this.grid) {
        return ''
      }

      return this.grid.name
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
    },
    mode (mode) {
      this.updateCursorPosition()
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
    this.camera.lookAt(new THREE.Vector3())
    this.controls.addEventListener('change', this.render)

    this.raycaster = new THREE.Raycaster()
    this.mouse = new THREE.Vector2()

    // Attach event listeners to the document
    this.canvas.addEventListener('mousemove', this.onDocumentMouseMove, false)
    this.canvas.addEventListener('mouseup', this.onDocumentMouseUp, false)
    document.addEventListener('keydown', this.onDocumentKeyDown, false)
    document.addEventListener('keyup', this.onDocumentKeyUp, false)
    window.addEventListener('resize', this.onWindowResize, false)
  },
  methods: {
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

      // We need to call this so that the canvas will resize to the window
      this.onWindowResize()
    },
    render () {
      this.renderer.render(this.director.scene, this.camera)
    },
    updateCursorPosition () {
      let data = this.director.getFirstIntersectData(this.raycaster)

      if (!data || !data.object) {
        this.director.clearSelection()
        return
      }

      // update cursor position
      let actualPosition = new THREE.Vector3()
      if (this.mode === EditorMode.DELETE) {
        if (data.object.name === 'grid-plane') {
          this.director.clearSelection()
          return
        }
        actualPosition.copy(data.object.position)
      } else if (this.mode === EditorMode.ADD) {
        actualPosition = data.point.add(data.face.normal)
      }

      let unitPosition = this.director.convertActualToUnitPosition(actualPosition)
      this.director.setSelection(unitPosition, { model: this.model })
    },
    onWindowResize () {
      this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight)
      this.render()
    },
    onDocumentMouseMove (event) {
      // Update mouse and raycaster
      this.mouse.set((event.offsetX / window.innerWidth) * 2 - 1, -(event.offsetY / window.innerHeight) * 2 + 1)
      this.raycaster.setFromCamera(this.mouse, this.camera)

      // Update the cursor position for the selection manager
      this.updateCursorPosition()
    },
    onDocumentMouseUp (event) {
      let data = this.director.getFirstIntersectData(this.raycaster)

      if (!data || !data.object) {
        return
      }

      let interactPosition = new THREE.Vector3()
      if (this.mode === EditorMode.DELETE) {
        // Delete
        interactPosition.copy(data.object.position)
        let unitPosition = this.director.convertActualToUnitPosition(interactPosition)
        let model = this.grid.at(unitPosition)
        this.director.remove(model)
      } else if (this.mode === EditorMode.ADD) {
        // Add
        if (!data.face) return
        interactPosition.copy(data.point.add(data.face.normal))
        let unitPosition = this.director.convertActualToUnitPosition(interactPosition)
        let model = ModelFactory.createModel({
          type: 'voxel',
          color: this.hexColor,
          position: unitPosition
        })
        this.director.add(model)
      }
    },
    onDocumentKeyDown (event) {
      switch (event.keyCode) {
        case 49: this.mode = EditorMode.ADD
          break
        case 50: this.mode = EditorMode.DELETE
          break
      }
    },
    onDocumentKeyUp (event) {
      console.log(this.director.grid.serialize())
    },
    isModeAdd () {
      return this.mode === EditorMode.ADD
    },
    isModeDelete () {
      return this.mode === EditorMode.DELETE
    },
    setModeAdd () {
      this.mode = EditorMode.ADD
    },
    setModeDelete () {
      this.mode = EditorMode.DELETE
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
    this.canvas.removeEventListener('mouseup', this.onDocumentMouseUp, false)
    document.removeEventListener('keydown', this.onDocumentKeyDown, false)
    document.removeEventListener('keyup', this.onDocumentKeyUp, false)
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

.help-field {
  position: absolute;
  right: 30px;
  bottom: 82px;
}
</style>
