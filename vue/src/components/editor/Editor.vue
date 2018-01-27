<template>
  <div>
    <!-- Canvas used to render the three.js map scene-->
    <div ref='canvas' id='canvas'></div>

    <span v-if="isModeAdd()" class="info">Hold shift to enter delete mode</span>
    <span v-if="isModeDelete()" class="info">Release shift to enter add mode</span>

    <!-- Color picker dropdown-->
    <div v-if="isModeAdd()" class="dropdown is-hoverable is-right is-pulled-right">
      <div class="dropdown-trigger">
        <button class="button" aria-haspopup="true" aria-controls="color-picker-dropdown-menu">
          <span>Current color</span>
          <div style="height: 16px; width: 16px; margin-left: 16px;" v-bind:style="{'background-color': hexColor}"></div>
        </button>
      </div>

      <!-- Color picker -->
      <div class="dropdown-menu" id="dropdown-menu4" role="menu">
        <sketch-picker v-model="color"></sketch-picker>
      </div>
    </div>
  </div>
</template>

<script>
import { Sketch } from 'vue-color'
import * as THREE from 'three'
import { Map } from './Map'
import { MapUtils } from './MapUtils'
import { VoxelMapModel } from './MapModel'
import { SelectionManager } from './SelectionManager'
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
      map: null,
      selectionManager: null,
      color: defaultColor,
      mode: EditorMode.ADD
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
      return new VoxelMapModel(new THREE.Vector3(), this.map.unitSize, this.hexColor)
    }
  },
  watch: {
    mode (mode) {
      this.updateCursorPosition()
    }
  },
  mounted () {
    this.setup()
    this.onWindowResize()
    this.render()

    // Attach event listeners to the document
    this.canvas.addEventListener('mousemove', this.onDocumentMouseMove, false)
    this.canvas.addEventListener('mouseup', this.onDocumentMouseUp, false)
    document.addEventListener('keydown', this.onDocumentKeyDown, false)
    document.addEventListener('keyup', this.onDocumentKeyUp, false)
    window.addEventListener('resize', this.onWindowResize, false)
  },
  methods: {
    setup () {
      // Create map
      this.map = new Map(16, 1000, 16, 50)
      this.map.addEventListener('redraw', (event) => {
        this.render()
        this.updateCursorPosition()
      })

      // Create selection manager
      this.selectionManager = new SelectionManager(this.map)
      this.selectionManager.addEventListener('change', (event) => {
        this.render()
      })

      // Create the renderer
      this.renderer = new THREE.WebGLRenderer()
      this.renderer.setPixelRatio(window.devicePixelRatio)

      // Create the camera
      let cameraFov = 45
      this.camera = new THREE.PerspectiveCamera(cameraFov, window.innerWidth / window.innerHeight, 1, 10000)
      this.camera.position.copy(new THREE.Vector3(1, 1, 1).multiplyScalar(this.map.getActualWidth()))
      this.camera.lookAt(new THREE.Vector3())

      // Add orbit controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enablePan = false
      this.controls.maxPolarAngle = (Math.PI / 2) + 0.1
      this.controls.addEventListener('change', this.render)

      // Attach to the container
      this.canvas = this.$refs.canvas
      this.canvas.appendChild(this.renderer.domElement)

      this.raycaster = new THREE.Raycaster()
      this.mouse = new THREE.Vector2()
    },
    render () {
      this.renderer.render(this.map.scene, this.camera)
    },
    updateCursorPosition () {
      let data = this.map.getFirstIntersectData(this.raycaster)

      if (!data || !data.object) {
        this.selectionManager.clear()
        return
      }

      // update cursor position
      let actualPosition = new THREE.Vector3()
      if (this.mode === EditorMode.DELETE) {
        if (data.object.name === 'grid-plane') {
          this.selectionManager.clear()
          return
        }
        actualPosition.copy(data.object.position)
      } else if (this.mode === EditorMode.ADD) {
        actualPosition = data.point.add(data.face.normal)
      }

      let unitPosition = MapUtils.convertActualToUnitPosition(this.map, actualPosition)
      this.selectionManager.selectAt(unitPosition, this.model)
    },
    onWindowResize () {
      this.camera.aspect = window.innerWidth / window.innerHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(window.innerWidth, window.innerHeight)
      this.render()
    },
    onDocumentMouseMove (event) {
      // Update mouse and raycaster
      this.mouse.set((event.offsetX / window.innerWidth) * 2 - 1, -(event.offsetY / window.innerHeight) * 2 + 1)
      this.raycaster.setFromCamera(this.mouse, this.camera)

      // Update the cursor position
      this.updateCursorPosition()
    },
    onDocumentMouseUp (event) {
      let data = this.map.getFirstIntersectData(this.raycaster)

      if (!data || !data.object) {
        return
      }

      let interactPosition = new THREE.Vector3()
      if (this.mode === EditorMode.DELETE) {
        // Delete
        interactPosition.copy(data.object.position)
        let unitPosition = MapUtils.convertActualToUnitPosition(this.map, interactPosition)
        this.map.removeAt(unitPosition)
      } else if (this.mode === EditorMode.ADD) {
        // Add
        if (!data.face) return
        interactPosition.copy(data.point.add(data.face.normal))
        let unitPosition = MapUtils.convertActualToUnitPosition(this.map, interactPosition)
        let model = new VoxelMapModel(unitPosition, this.map.unitSize, this.hexColor)
        this.map.add(model)
      }
    },
    onDocumentKeyDown (event) {
      switch (event.keyCode) {
        case 16: this.mode = EditorMode.DELETE
          break
      }
    },
    onDocumentKeyUp (event) {
      switch (event.keyCode) {
        case 16: this.mode = EditorMode.ADD
          break
      }
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
    this.map.removeEventListener('update', this.render, false)

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
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
