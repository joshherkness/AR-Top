import * as THREE from 'three'
import { GridHelpers } from './GridHelpers'

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

    var ambientLight = new THREE.AmbientLight(0xf4f4f4)
    scene.add(ambientLight)
  }

  let _setupGridLines = function (scene) {
    // Ensure teh scene exists
    if (!scene) return

    // Create the grid
    var lineColor = GridHelpers.darken(color)
    var lines = new THREE.GridHelper(scene.actualWidth, grid.width, lineColor, lineColor)
    lines.name = 'grid-lines'
    scene.add(lines)

    // Create the grid plane used for user interraction
    var gridPlaneGeometry = new THREE.PlaneBufferGeometry(scene.actualWidth, scene.actualDepth)
    gridPlaneGeometry.rotateX(-Math.PI / 2)
    var material = new THREE.MeshBasicMaterial({ visible: false })
    var gridPlane = new THREE.Mesh(gridPlaneGeometry, material)
    gridPlane.name = 'grid-plane'
    scene.add(gridPlane)
  }

  let _setupGridBase = function (scene) {
    // Ensure teh scene exists
    if (!scene) return

    let baseColor = new THREE.Color(color)
    let baseMaterial = new THREE.MeshPhongMaterial({color: baseColor})
    let baseGeometry = new THREE.CubeGeometry(scene.actualWidth, scale, scene.actualDepth)
    let base = new THREE.Mesh(baseGeometry, baseMaterial)

    // Place the base just below the grid
    base.position.y = -(scale / 2) - 1

    // Add to the scene
    scene.add(base)
  }

  _setupLighting(scene)
  _setupGridLines(scene)
  _setupGridBase(scene)

  return scene
}
