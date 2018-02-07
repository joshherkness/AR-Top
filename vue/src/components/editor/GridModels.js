import 'three'
import 'three/examples/js/loaders/OBJLoader'
import 'three/examples/js/loaders/MTLLoader'
import { GridHelpers } from './GridHelpers'
import { TileFloorObject } from './PreloadModels'

const DEFAULT_WIREFRAME_LINE_WIDTH = 1

export const GridModelType = Object.freeze({
  VOXEL: 'voxel',
  TILE_FLOOR: 'tile_floor'
})

export class GridModel {
  constructor (position) {
    // Ensure that this abstract class cannot be constructed
    if (this.constructor === GridModel) {
      throw new TypeError("Can not construct abstract class 'MapContent'.")
    }

    // Check that instance methods are implemented
    if (this.createObject === GridModel.prototype.createObject) {
      throw new TypeError("Please implement abstract method 'createObject'.")
    }

    if (position === undefined) {
      throw new TypeError('Position must be defined')
    }

    this.position = new THREE.Vector3(position.x, position.y, position.z)
    this.type = undefined
  }

  createObject (scale) {
    throw new TypeError("Do not call abstract method 'setup' from child.")
  }

  equals (model) {
    if (model === undefined) {
      throw new Error('Model must be defined')
    }

    return this.position.equals(model.position) && this.type === model.type
  }
}

/**
* Class used to represent a voxel type model that can be added to a Map. We
* can think of a voxel as a 3D pixel or cube. Because of this, a voxel should
* be rendered using only a 3D position vector and a single color.
*
* @export
* @class VoxelGridModel
* @extends {GridModel}
*/
export class VoxelGridModel extends GridModel {
  constructor (position, color) {
    super(position)

    if (color === undefined) {
      throw new TypeError('Color must be defined')
    }

    this.color = color
    this.type = GridModelType.VOXEL
  }

  createObject (scale = 1) {
    // Create geometry and material
    let geometry = new THREE.BoxGeometry(scale, scale, scale)
    let material = new THREE.MeshPhongMaterial({
      color: this.color,
      vertexColors: THREE.VertexColors,
      polygonOffset: true,
      polygonOffsetFactor: 2,
      polygonOffsetUnits: 1,
      overdraw: 0.5,
      transparent: true
    })

    // Create the object
    let object = new THREE.Mesh(geometry, material)

    // Add wireframe
    let wireframe = _createWireframeObjectForGeometry(geometry, GridHelpers.darken(this.color))
    if (wireframe) {
      object.add(wireframe)
    }

    return object
  }

  equals (model) {
    return super.equals(model) && this.color === model.color
  }
}
import tile_floor_object from '@/assets/models/tile_floor.obj'
import tile_floor_material from '@/assets/models/tile_floor.mtl'

export class TileFloorGridModel extends GridModel {
  constructor (position) {
    super(position)

    this.type = GridModelType.TILE_FLOOR
  }

  createObject (scale = 1) {
    let mesh = TileFloorObject.clone()
    mesh.traverse((node) => {
      if (node.material) {
        node.material = node.material.clone()
      }
    })
    mesh.scale.set(scale/16, scale/16, scale/16)
    mesh.position.y = -scale/2
    mesh.children[0].material.transparent = true
    mesh.children[0].material.opacity = 1.0

    let object = new THREE.Group()
    object.add(mesh)

    return object
  }
}

/**
 * This function creates a wireframe object for a given geometry.
 *
 * @param {THREE.Geometry} geometry
 * @param {THREE.Color} color
 * @param {number} lineWidth
 * @returns {THREE.Object3D} representation of wireframe
 */
function _createWireframeObjectForGeometry (geometry, color, linewidth) {
  color = color || new THREE.Color(0x000000)
  linewidth = linewidth || DEFAULT_WIREFRAME_LINE_WIDTH

  let edgeGeometry = new THREE.EdgesGeometry(geometry)
  let lineMaterial = new THREE.LineBasicMaterial({ color: color, linewidth: linewidth })

  return new THREE.LineSegments(edgeGeometry, lineMaterial)
}