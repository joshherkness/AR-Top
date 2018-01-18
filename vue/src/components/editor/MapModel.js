import * as THREE from 'three'

const DEFAULT_WIREFRAME_LINE_WIDTH = 2

/**
 * This enumerator represents the type of content that are available
 * within a map.
 */
export const MapModelType = Object.freeze({
  VOXEL: Symbol('voxel')
})

/**
 * Abstract class used to represent any model that can be placed onto a Map.
 *
 * - Note that this should never be directly constructed, as it is abstract.
 *
 * @class AbstractMapModel
 */
class AbstractMapModel {
  constructor (position, type) {
    // Ensure that this abstract class cannot be constructed
    if (this.constructor === AbstractMapModel) {
      throw new TypeError("Can not construct abstract class 'MapContent'.")
    }

    // Check that instance methods are implemented
    if (this._setup === AbstractMapModel.prototype._setup) {
      throw new TypeError("Please implement abstract method 'setup'.")
    }

    // Register member variables
    this.position = position
    this.type = type
    this.object = null
  }

  /**
   * This function should be implementd by subclasses in order to do any
   * setup after construction.
   *
   * - Note that this function **must** be implemented.
   *
   * @private
   *
   * @memberOf AbstractMapModel
   */
  _setup () {
    throw new TypeError("Do not call abstract method 'setup' from child.")
  }
}

/**
 * Class used to represent a voxel type model that can be added to a Map. We
 * can think of a voxel as a 3D pixel or cube. Because of this, a voxel should
 * be rendered using only a 3D position vector and a single color.
 *
 * @export
 * @class VoxelMapModel
 * @extends {AbstractMapModel}
 */
export class VoxelMapModel extends AbstractMapModel {
  /**
   * Creates an instance of VoxelMapModel.
   *
   * @param {number} position
   * @param {number} scale
   * @param {THREE.Color} color
   *
   * @memberOf VoxelMapModel
   */
  constructor (position, scale, color) {
    super(position, MapModelType.VOXEL)

    // Register member variables
    this.scale = scale || 1
    this.color = color || new THREE.Color(0xffffff)

    this._setup()
  }

  /**
   * This function is used to create a THREE.Object3D representing
   * a voxel for this model
   *
   * @private
   *
   * @memberOf VoxelMapModel
   */
  _setup () {
    // Create geometry and material
    let geometry = new THREE.BoxGeometry(this.scale, this.scale, this.scale)
    let material = new THREE.MeshLambertMaterial({
      color: this.color,
      vertexColors: THREE.VertexColors,
      polygonOffset: true,
      polygonOffsetFactor: 4,
      polygonOffsetUnits: 1,
      overdraw: 0.5
    })

    // Create the object
    this.object = new THREE.Mesh(geometry, material)

    // Add wireframe
    let wireframe = _createWireframeObjectForGeometry(geometry)
    if (wireframe) {
      this.object.add(wireframe)
    }
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
