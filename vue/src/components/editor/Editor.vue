<template>
  <div ref='canvas' id='canvas'></div>
</template>

<script>
import * as THREE from 'three'
import { Map } from './Map'
import { MapUtils } from './MapUtils'
import { VoxelMapModel } from './MapModel'
var OrbitControls = require('three-orbit-controls')(THREE)

export default {
  name: 'Editor',
  data: function () {
    return {
      camera: null,
      controls: null,
      renderer: null,
      raycaster: null,
      mouse: null,
      map: null,
      isShiftDown: false,
      selectedColor: null
    }
  },
  watch: {
    selectedColor (color) {
      this.updateCursorModel()
    }
  },
  mounted () {
    this.setup()
    this.onWindowResize()
    this.render()

    // Set current color (random, for now)
    this.selectedColor = (new THREE.Color()).setHex(Math.random() * 0xffffff)

    // Attach event listeners to the document
    document.addEventListener('mousemove', this.onDocumentMouseMove, false)
    document.addEventListener('mousedown', this.onDocumentMouseDown, false)
    document.addEventListener('mouseup', this.onDocumentMouseUp, false)
    document.addEventListener('keydown', this.onDocumentKeyDown, false)
    document.addEventListener('keyup', this.onDocumentKeyUp, false)
    window.addEventListener('resize', this.onWindowResize, false)
  },
  methods: {
    setup () {
      // Create map
      this.map = new Map(16, 3, 50)
      this.map.addEventListener('redraw', (event) => {
        this.render()
        this.updateCursorPosition()
      })

      // Create the renderer
      this.renderer = new THREE.WebGLRenderer()
      this.renderer.setPixelRatio(window.devicePixelRatio)

      // Create the camera
      let cameraFov = 45
      this.camera = new THREE.PerspectiveCamera(cameraFov, window.innerWidth / window.innerHeight, 1, 10000)
      this.camera.position.copy(new THREE.Vector3(1, 1, 1).multiplyScalar(this.map.actualSize))
      this.camera.lookAt(new THREE.Vector3())

      // Add orbit controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enablePan = false
      this.controls.maxPolarAngle = (Math.PI / 2) + 0.1
      this.controls.addEventListener('change', this.render)

      // Attach to the container
      let container = this.$refs.canvas
      container.appendChild(this.renderer.domElement)

      this.raycaster = new THREE.Raycaster()
      this.mouse = new THREE.Vector2()
    },
    render () {
      this.renderer.render(this.map.scene, this.camera)
    },
    updateCursorPosition () {
      let object = this.map.getFirstIntersectObject(this.raycaster)
      
      if (!object || !object.face) return

      // update cursor position
      let actualPosition = object.point.add(object.face.normal)
      this.map.setCursorActualPosition(actualPosition)
    },
    updateCursorModel () {
      let cursorPosition = this.map.cursorModel ? this.map.cursorModel.position : new THREE.Vector3(999, 999, 999)
      let cursorModel = new VoxelMapModel(cursorPosition, this.map.unitSize, this.selectedColor)
      this.map.setCursorModel(cursorModel)
    },
    onWindowResize () {
      this.camera.aspect = window.innerWidth / window.innerHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(window.innerWidth, window.innerHeight)
      this.render()
    },
    onDocumentMouseMove (event) {
      event.preventDefault()

      // Update mouse and raycaster
      this.mouse.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1)
      this.raycaster.setFromCamera(this.mouse, this.camera)

      // Update the cursor position
      this.updateCursorPosition()
    },
    onDocumentMouseDown (event) {
      event.preventDefault()
    },
    onDocumentMouseUp (event) {
      event.preventDefault()

      let object = this.map.getFirstIntersectObject(this.raycaster)
      if (!object || !object.face) return

      let position = object.point.add(object.face.normal)
      let unitPosition = MapUtils.convertActualToUnitPosition(this.map, position)
      let model = new VoxelMapModel(unitPosition, this.map.unitSize, this.selectedColor)
      this.map.add(model)
    },
    onDocumentKeyDown (event) {
      switch (event.keyCode) {
        case 16: this.isShiftDown = true
          break
        case 49: this.selectedColor = new THREE.Color(0xffffff) // White
          break
        case 50: this.selectedColor = new THREE.Color(0x242424) // Black
          break
        case 51: this.selectedColor = new THREE.Color(0x19345A) // Blue
          break
        case 52: this.selectedColor = new THREE.Color(0xFFD966) // Yellow
          break
        case 53: this.selectedColor = new THREE.Color(0x7C9658) // Green
          break
        case 54: this.selectedColor = new THREE.Color(0xBF4E51) // Red
          break
      }
    },
    onDocumentKeyUp (event) {
      switch (event.keyCode) {
        case 16: this.isShiftDown = false
          break
      }
    }
  },
  destroyed () {
    // Remove event listeners from orbit controls
    this.controls.dispose()

    // Remove event listeners from map
    this.map.removeEventListener('update', this.render, false)

    // Remove event listeners
    document.removeEventListener('mousemove', this.onDocumentMouseMove, false)
    document.removeEventListener('mousedown', this.onDocumentMouseDown, false)
    document.removeEventListener('mouseup', this.onDocumentMouseUp, false)
    document.removeEventListener('keydown', this.onDocumentKeyDown, false)
    document.removeEventListener('keyup', this.onDocumentKeyUp, false)
    window.removeEventListener('resize', this.onWindowResize, false)
  }
}
</script>

<style scoped>
#canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
