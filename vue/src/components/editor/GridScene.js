import * as THREE from 'three'

export function GridScene (grid, scale) {
  let scene = new THREE.Scene()
  scene.actualWidth = grid.width * scale
  scene.actualHeight = grid.height * scale
  scene.actualDepth = grid.depth * scale
  let color = grid.color

  let _setupLighting = function (scene) {
    // Ensure teh scene exists
    if (!scene) return

    let lighting = new THREE.Group()
    lighting.name = 'lighting'

    var ambientLight = new THREE.AmbientLight(0x404040)
    scene.add(ambientLight)

    var directionalLight = new THREE.DirectionalLight(0xffffff)
    directionalLight.position.x = 1
    directionalLight.position.y = 1
    directionalLight.position.z = 0.75
    directionalLight.position.normalize()
    scene.add(directionalLight)

    directionalLight = new THREE.DirectionalLight(0x808080)
    directionalLight.position.x = -1
    directionalLight.position.y = 1
    directionalLight.position.z = -0.75
    directionalLight.position.normalize()
    scene.add(directionalLight)
  }

  let _setupGridLines = function (scene) {
    // Ensure teh scene exists
    if (!scene) return

    // Create the grid
    var lineColor = new THREE.Color(0x434b54)
    var lines = new THREE.GridHelper(scene.actualWidth, grid.width, lineColor, lineColor)
    lines.name = 'grid-lines'
    scene.add(lines)

    // Create the grid plane used for user interraction
    var gridPlaneGeometry = new THREE.PlaneBufferGeometry(scene.actualWidth, scene.actualDepth)
    gridPlaneGeometry.rotateX(-Math.PI / 2)
    var gridPlane = new THREE.Mesh(gridPlaneGeometry, new THREE.MeshBasicMaterial({ visible: false }))
    gridPlane.name = 'grid-plane'
    scene.add(gridPlane)
  }

  let _setupGridBase = function (scene) {
    // Ensure teh scene exists
    if (!scene) return

    let baseColor = new THREE.Color(color)
    let baseMaterial = new THREE.MeshLambertMaterial({color: baseColor})
    let baseGeometry = new THREE.CubeGeometry(scene.actualWidth, scale, scene.actualDepth)
    let base = new THREE.Mesh(baseGeometry, baseMaterial)

    // Place the base just below the grid
    base.position.y = -(scale / 2) - 1

    // Add to the scene
    scene.add(base)
  }

  scene.background = new THREE.Color(0xffffff)
  _setupLighting(scene)
  _setupGridLines(scene)
  _setupGridBase(scene)

  return scene
}
