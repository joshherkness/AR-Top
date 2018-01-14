<template>
  <div ref='canvas' id='canvas'></div>
</template>

<script>
import * as THREE from 'three'
import { VoxelMapModel, Map } from './EditorHelpers'
var OrbitControls = require('three-orbit-controls')(THREE)

export default {
  name: 'Editor',
  data: function () {
    return {
      camera: null,
      cameraFov: 45,
      controls: null,
      renderer: null,
      isShiftDown: false,
      raycaster: null,
      mouse: null,
      map: null,
      selectedColor: new THREE.Color(0xffffff)
    }
  },
  mounted () {
    this.setup()
    this.onWindowResize()
    this.render()

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
      this.map = new Map(16, 3, 50, this.render)

      // Create the renderer
      this.renderer = new THREE.WebGLRenderer()
      this.renderer.setPixelRatio(window.devicePixelRatio)

      // Create the camera
      this.camera = new THREE.PerspectiveCamera(this.cameraFov, window.innerWidth / window.innerHeight, 1, 10000)
      console.log((new THREE.Vector3(1, 1, 1)).multiplyScalar(this.map.actualSize))
      this.camera.position.copy(new THREE.Vector3(1, 1, 1).multiplyScalar(this.map.actualSize))
      this.camera.lookAt(new THREE.Vector3())

      // Add orbit controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enablePan = false
      this.controls.maxPolarAngle = (Math.PI / 2) + 0.1
      this.controls.addEventListener('change', this.render)

      let container = this.$refs.canvas
      container.appendChild(this.renderer.domElement)

      this.raycaster = new THREE.Raycaster()
      this.mouse = new THREE.Vector2()
    },
    render () {
      this.renderer.render(this.map.scene, this.camera)
    },
    onWindowResize () {
      this.camera.aspect = window.innerWidth / window.innerHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(window.innerWidth, window.innerHeight)
      this.render()
    },
    /**
     * Gets called when the 'mousemove' event has occured on the document.
     */
    onDocumentMouseMove (event) {
      event.preventDefault()

      // Update the cursor position
      let intersect = this.getIntersecting()
      if (!intersect || !intersect.face) {
        return
      }

      let position = intersect.point.add(intersect.face.normal)
      this.map.setActualCursorPosition(position)
    },
    onDocumentMouseDown (event) {
      event.preventDefault()
    },
    onDocumentMouseUp (event) {
      let intersect = this.getIntersecting()
      if (!intersect) {
        return
      }

      let position = intersect.point.add(intersect.face.normal)
      let unitPosition = this.map.getUnitPosition(position.clone())
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
        case 190: this.isGridEnabled = !this.isGridEnabled
          break
      }
    },
    onDocumentKeyUp (event) {
      switch (event.keyCode) {
        case 16: this.isShiftDown = false
          break
      }
    },
    getIntersecting () {
      this.mouse.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1)
      this.raycaster.setFromCamera(this.mouse, this.camera)
      let modelObjects = this.map.models.map((model) => { return model.object })

      let grid = this.map.scene.getObjectByName('grid')
      let intersects = this.raycaster.intersectObjects(modelObjects.concat([grid]), true)
      return intersects[0] || null
    }
  },
  destroyed () {
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
