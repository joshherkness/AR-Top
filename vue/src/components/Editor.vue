<template>
  <div ref='canvas' id='canvas'></div>
</template>

<script>
import * as THREE from 'three'
var OrbitControls = require('three-orbit-controls')(THREE)

export default {
  name: 'Editor',
  data () {
    return {
      camera: null,
      controls: null,
      scene: null,
      renderer: null,
      objects: []
    }
  },
  mounted () {
    this.init()
    this.onWindowResize()
    this.render()

    // Attach event listeners to the document
    window.addEventListener('resize', this.onWindowResize, false)
  },
  methods: {
    init () {
      // Create the renderer
      this.renderer = new THREE.WebGLRenderer()
      this.renderer.setPixelRatio(window.devicePixelRatio)

      // Create the camera
      this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 10000)
      this.camera.position.set(500, 800, 1300)
      this.camera.lookAt(new THREE.Vector3())

      // Add orbit controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enablePan = false
      this.controls.maxPolarAngle = (Math.PI / 2) + 0.1
      this.controls.addEventListener('change', this.render)

      // Create the scene
      this.scene = new THREE.Scene()
      this.scene.background = new THREE.Color(0xffffff)

      // Add lighting
      var ambientLight = new THREE.AmbientLight(0x606060)
      this.scene.add(ambientLight)

      var directionalLight = new THREE.DirectionalLight(0xffffff)
      directionalLight.position.set(1, 0.75, 0.5).normalize()
      this.scene.add(directionalLight)

      // Create the grid
      let gridHelper = new THREE.GridHelper(1000, 20, 0xafafaf, 0xafafaf)
      this.scene.add(gridHelper)

      // Create the plane
      var geometry = new THREE.PlaneBufferGeometry(1000, 1000)
      geometry.rotateX(-Math.PI / 2)
      let plane = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ visible: false }))
      this.scene.add(plane)
      this.objects.push(plane)

      // Create the base
      let base = new THREE.Mesh(new THREE.CubeGeometry(1000, 50, 1000), new THREE.MeshBasicMaterial({color: 0xf9f9f9}))
      base.position.y = -26
      this.scene.add(base)

      let container = this.$refs.canvas
      container.appendChild(this.renderer.domElement)
    },
    render () {
      this.renderer.render(this.scene, this.camera)
    },
    onWindowResize () {
      this.camera.aspect = window.innerWidth / window.innerHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(window.innerWidth, window.innerHeight)
    }
  },
  destroyed () {
    // Remove event listeners
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
