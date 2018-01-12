<template>
  <div>
    <h1>Editor</h1>
    <div ref='canvas'></div>
  </div>
</template>

<script>
import * as THREE from 'three'

export default {
  name: 'Editor',
  data () {
    return {
      camera: null,
      scene: null,
      renderer: null,
      objects: []
    }
  },
  mounted () {
    this.init()
    this.render()

    // Attach event listeners to the document
    document.addEventListener('mousemove', this.onDocumentMouseMove, false)
    document.addEventListener('mousedown', this.onDocumentMouseDown, false)
  },
  methods: {
    init () {
      // Create the renderer
      this.renderer = new THREE.WebGLRenderer({ antialias: true })
      this.renderer.setPixelRatio(window.devicePixelRatio)

      // Create the camera
      this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 10000)
      this.camera.position.set(500, 800, 1300)
      this.camera.lookAt(new THREE.Vector3())

      // Create the scene
      this.scene = new THREE.Scene()
      this.scene.background = new THREE.Color(0xf0f0f0)

      // Add lighting
      var ambientLight = new THREE.AmbientLight(0x606060)
      this.scene.add(ambientLight)

      var directionalLight = new THREE.DirectionalLight(0xffffff)
      directionalLight.position.set(1, 0.75, 0.5).normalize()
      this.scene.add(directionalLight)

      // Create the grid
      let gridHelper = new THREE.GridHelper(1000, 20)
      this.scene.add(gridHelper)

      // Create the plane
      var geometry = new THREE.PlaneBufferGeometry(1000, 1000)
      geometry.rotateX(-Math.PI / 2)
      let plane = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ visible: false }))
      this.scene.add(plane)
      this.objects.push(plane)

      let container = this.$refs.canvas
      container.appendChild(this.renderer.domElement)
    },
    render () {
      this.renderer.render(this.scene, this.camera)
    },
    onDocumentMouseMove (event) {
      // Called when mouse moved
    },
    onDocumentMouseDown (event) {
      // Called when mouse down
    }
  },
  destroyed () {

  }
}
</script>

<style scoped>

</style>
