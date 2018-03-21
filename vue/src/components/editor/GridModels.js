import * as THREE from 'three'
import 'three/examples/js/loaders/OBJLoader'
import 'three/examples/js/loaders/MTLLoader'
import { GridHelpers } from './GridHelpers'
import { ObjectList, BASE_RING_OBJECT_NAME } from './PreloadedObjects'

const DEFAULT_WIREFRAME_LINE_WIDTH = 1

export const GridModelType = Object.freeze({
  VOXEL: 'voxel',
  TILE_FLOOR: 'tile_floor',
  CHARACTER: 'character_type'
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

export class TileGridModel extends GridModel {
  constructor (position, color, type) {
    super(position)

    if (color === undefined) {
      throw new TypeError('Color must be defined')
    }

    if (type === undefined) {
      throw new TypeError('Type must be defined')
    }

    this.type = type
    this.color = color
  }

  createObject (scale = 1) {
    let mesh = ObjectList[this.type].clone()
    mesh.traverse((node) => {
      if (node.material) {
        node.material = node.material.clone()
        node.material.transparent = true
        node.material.color = new THREE.Color(this.color)

        if (node.userData && !node.userData.isBoundingBox) {
          node.material.opacity = 1.0
        }
      }
    })
    mesh.scale.set(scale / 16, scale / 16, scale / 16)
    mesh.position.y = -scale / 2

    let object = new THREE.Group()
    object.add(mesh)

    return object
  }
}

export class EntityGridModel extends GridModel {
  constructor (position, color, type) {
    super(position)

    if (color === undefined) {
      throw new TypeError('Color must be defined')
    }

    if (type === undefined) {
      throw new TypeError('Type must be defined')
    }

    this.type = type
    this.color = color
  }

  createObject (scale = 1) {
    let mesh = ObjectList[this.type].clone()
    mesh.traverse((node) => {
      if (node.material) {
        node.material = node.material.clone()
        node.material.transparent = true

        if (node.userData && !node.userData.isBoundingBox) {
          node.material.opacity = 1.0
        }
      }

      // Change the color of the ring
      if (node.name === BASE_RING_OBJECT_NAME) {
        node.material.color = new THREE.Color(this.color)
      }
    })
    mesh.scale.set(scale / 16, scale / 16, scale / 16)
    mesh.position.y = -scale / 2

    let group = new THREE.Group()
    group.add(mesh)

    return group
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
