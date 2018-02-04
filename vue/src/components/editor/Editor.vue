<template>
  <div>
    <!-- Canvas used to render the three.js map scene-->
    <div ref='canvas' id='canvas'
      :class="{'is-loading': loading}"></div>

    <div class="field has-addons" style="position: absolute; bottom: 10px; right: 10px;"
      v-if="!loading">
      <div class="control">
        <div class="dropdown is-hoverable is-up is-right">
          <div class="dropdown-trigger">
            <div class="button is-medium is-light"
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
        <div class="button is-medium is-light"
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
</template>

<script>
import axios from 'axios'
import { generateConfig } from '@/api/api'

import { GridDirector } from './GridDirector'
import { Grid } from './Grid'
import { ModelFactory } from './ModelFactory'
import { Sketch } from 'vue-color'
import * as THREE from 'three'
import { EditorMode } from './EditorMode'
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
      selectionManager: null,
      color: defaultColor,
      mode: EditorMode.ADD,
      loading: false
    }
  },
  components: {
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
    }
  },
  watch: {
    mode (mode) {
      this.updateCursorPosition()
    }
  },
  mounted () {
    this.loading = true

    // Create the director
    this.director = new GridDirector({ scale: 50 })

    let url = 'http://localhost:5000/api/map'
    axios.get(`${url}/${this.$route.params.id}`, generateConfig({
      email: this.$store.state.user.email
    })).then((res) => {
      let mapData = res.data
      mapData.id = mapData._id['$oid']
      this.grid = Grid.deserialize(mapData)
      this.director.load(this.grid).then(() => {
        this.setup()
        this.loading = false
      })
    }).catch((err) => {
      console.log(err)
      throw err
    })
  },
  methods: {
    setup () {
      // Create the renderer
      this.renderer = new THREE.WebGLRenderer()
      this.renderer.setPixelRatio(window.devicePixelRatio)
      this.renderer.setClearColor(0xffffff)

      // Create the camera
      let cameraFov = 45
      this.camera = new THREE.PerspectiveCamera(cameraFov, window.innerWidth / window.innerHeight, 1, 10000)
      this.camera.lookAt(new THREE.Vector3())
      this.camera.position.copy(new THREE.Vector3(1, 1, 1).multiplyScalar(this.director.scene.actualWidth))

      // Add orbit controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enablePan = false
      this.controls.minDistance = 2 * this.director.scale || 50
      this.controls.maxPolarAngle = (Math.PI / 2) + 0.1
      this.controls.addEventListener('change', this.render)

      // Attach to the container
      this.canvas = this.$refs.canvas
      this.canvas.appendChild(this.renderer.domElement)

      this.raycaster = new THREE.Raycaster()
      this.mouse = new THREE.Vector2()

      this.onWindowResize()

      // Attach event listeners to the document
      this.canvas.addEventListener('mousemove', this.onDocumentMouseMove, false)
      this.canvas.addEventListener('mouseup', this.onDocumentMouseUp, false)
      document.addEventListener('keydown', this.onDocumentKeyDown, false)
      document.addEventListener('keyup', this.onDocumentKeyUp, false)
      window.addEventListener('resize', this.onWindowResize, false)

      this.director.addEventListener('update', (event) => {
        this.render()
      })
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

.info {
  position: absolute;
  bottom: 0;
  left: 0;
  padding: 20px;
}

#canvas {
  margin-top: 3em;
  position: absolute;
  top: 1;
  left: 0;
  width: 100%;
  height: 100%;

  &.is-loading {
        position: absolute;
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
}
</style>
