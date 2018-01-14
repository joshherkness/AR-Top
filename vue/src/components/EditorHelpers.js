import * as THREE from 'three'

const DEFAULT_WIREFRAME_LINE_WIDTH = 2
const DEFAULT_MAP_SIZE = 40
const DEFAULT_MAP_HEIGHT = 1000
const DEFAULT_MAP_UNIT_SIZE = 50
const DEFAULT_CURSOR_COLOR = 0xFFD966
const DEFAULT_CURSOR_OPACITY = 0.5

/**
 * This enumerator represents the type of content that are available
 * within a map.
 */
export const MapModelType = Object.freeze({
  VOXEL: Symbol('voxel')
})

/**
 * This class represents a map.
 *
 * @class Map
 *
 */
export class Map {
  /**
   * Constructor used to create a Map using a specified size.
   *
   * @param {THREE.Vector3} size
   *
   * @memberOf Map
   */
  constructor (size, height, unitSize, updateListener) {
    // Register member variables
    this.size = size > 0 ? size : DEFAULT_MAP_SIZE
    this.height = height > 0 ? height : DEFAULT_MAP_HEIGHT
    this.unitSize = unitSize || DEFAULT_MAP_UNIT_SIZE
    this.updateListener = updateListener || null

    // Calculated variables
    this.actualSize = this.size * this.unitSize
    this.actualHeight = this.height * this.unitSize

    this.models = []

    // Setup the scene
    this._setupScene()

    this.cursorPosition = new THREE.Vector3(-1, -1, -1)
  }

  /**
   * This function adds a specified model to the map. If another model is
   * occupying the same position of that specified, an error should be thrown.
   *
   * @param {AbstractMapModel} model
   *
   * @memberOf Map
   */
  add (model) {
    // Ensure that the model is defined
    if (!model) return

    // Ensure that a model is not already occupying that position
    if (this.at(model.position)) {
      throw new Error('A model with this position already exists.')
    }

    // Ensure that the model is within the bounds of the map
    if (!this.isWithinBounds(model.position)) {
      throw new Error('The models position is outside the bounds of the map.')
    }

    // Add the model
    this.models.push(model)

    // Add the model object to the scene
    model.object.position.copy(this.getActualPosition(model.position))
    this.scene.add(model.object)

    if (this.updateListener) {
      this.updateListener()
    }
  }

  /**
   * This function removes the first model whos object matches that specified.
   *
   * - Note that this function is not responsible for removing the model object
   * from the scene in which it is placed.
   *
   * @param {THREE.Object3D} object
   *
   * @returns {AbstractMapModel} the removed model, otherwise undefined
   *
   * @memberOf Map
   */
  removeModelByObject (object) {
    let index = this.models.findIndex((model) => {
      if (!model.object) {
        throw new Error('Object should be defined for model.')
      }
      return model.object.id === object.id
    })

    if (index === -1) {
      return undefined
    }

    // Remove the model
    let removedModel = this.models.splice(index, 1)

    if (this.updateListener) {
      this.updateListener()
    }

    return removedModel
  }

  /**
   * This function returns the first model that matches the specified
   * vector position within the map. Otherwise, a value of _undefined_ will
   * be returned.
   *
   * @param {THREE.Vector3} position
   * @returns {AbstractMapModel} the first model at the specified location.
   *
   * @memberOf Map
   */
  at (position) {
    return this.models.find((model) => {
      return position.equals(model.position)
    })
  }

  /**
   * This function returns a boolean of whether the specified position is
   * within the bounds of the map.
   *
   * @returns {boolean} whether the position is within bounds
   *
   * @memberOf Map
   */
  isWithinBounds (position) {
    return ((position.x >= 0 && position.x < this.size) &&
      (position.y >= 0 && position.y < this.height) &&
      (position.z >= 0 && position.z < this.size))
  }

  getUnitPosition (actualPosition) {
    let offset = new THREE.Vector3(this.actualSize / 2, 0, this.actualSize / 2)
    return actualPosition
      .add(offset)
      .divideScalar(this.unitSize)
      .floor()
      .multiplyScalar(this.unitSize)
      .divideScalar(this.unitSize)
  }

  getActualPosition (unitPosition) {
    let offset = new THREE.Vector3(this.actualSize / 2, 0, this.actualSize / 2)
    return unitPosition
      .multiplyScalar(this.unitSize)
      .addScalar(this.unitSize / 2)
      .sub(offset)
  }

  setActualCursorPosition (actualPosition) {
    // Convert actual to unit position
    let unitPosition = this.getUnitPosition(actualPosition)
    let roundedActualPosition = this.getActualPosition(unitPosition.clone())
    let isWithinBounds = this.isWithinBounds(unitPosition)

    this.cursorPosition = isWithinBounds ? roundedActualPosition : new THREE.Vector3(-1, -1, -1)

    // Retrieve and update the cursor
    let cursor = this.scene.getObjectByName('cursor')
    if (!cursor) {
      return
    }
    cursor.visible = isWithinBounds
    cursor.position.copy(roundedActualPosition)

    if (this.updateListener) {
      this.updateListener()
    }
  }

  _setupScene () {
    this.scene = new THREE.Scene()
    this.scene.background = new THREE.Color(0xbbbbbb)
    this._setupLighting()
    this._setupGrid()
    this._setupGridBase()
    this._setupCursor()
  }

  _setupLighting () {
    let lighting = new THREE.Group()
    lighting.name = 'lighting'

    var ambientLight = new THREE.AmbientLight(0x404040)
    this.scene.add(ambientLight)

    var directionalLight = new THREE.DirectionalLight(0xffffff)
    directionalLight.position.x = 1
    directionalLight.position.y = 1
    directionalLight.position.z = 0.75
    directionalLight.position.normalize()
    this.scene.add(directionalLight)

    directionalLight = new THREE.DirectionalLight(0x808080)
    directionalLight.position.x = -1
    directionalLight.position.y = 1
    directionalLight.position.z = -0.75
    directionalLight.position.normalize()
    this.scene.add(directionalLight)
  }

  _setupGrid () {
    var grid = new THREE.Group()
    grid.name = 'grid'

    // Create the grid
    var lineColor = new THREE.Color(0x434b54)
    var lines = new THREE.GridHelper(this.actualSize, this.size, lineColor, lineColor)
    grid.add(lines)

    // Create the grid plane used for user interraction
    var gridPlaneGeometry = new THREE.PlaneBufferGeometry(this.actualSize, this.actualSize)
    gridPlaneGeometry.rotateX(-Math.PI / 2)
    var gridPlane = new THREE.Mesh(gridPlaneGeometry, new THREE.MeshBasicMaterial({ visible: false }))
    grid.add(gridPlane)

    // Add to the scene
    this.scene.add(grid)
  }

  _setupGridBase () {
    let baseColor = new THREE.Color(0x545d67)
    let baseMaterial = new THREE.MeshLambertMaterial({color: baseColor})
    let baseGeometry = new THREE.CubeGeometry(this.actualSize, this.unitSize, this.actualSize)
    let base = new THREE.Mesh(baseGeometry, baseMaterial)

    // Place the base just below the grid
    base.position.y = -(this.unitSize / 2) - 1

    // Add to the scene
    this.scene.add(base)
  }

  _setupCursor () {
    let cursorModel = new VoxelMapModel(new THREE.Vector3(), this.unitSize, DEFAULT_CURSOR_COLOR)
    cursorModel.object.name = 'cursor'
    cursorModel.object.visible = false
    cursorModel.object.material.opacity = DEFAULT_CURSOR_OPACITY
    cursorModel.object.material.transparent = true

    // Add cursor to scene
    this.scene.add(cursorModel.object)
  }
}

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
    if (this.setup === AbstractMapModel.prototype.setup) {
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
   * @memberOf AbstractMapModel
   */
  setup () {
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
   * @param {number} x
   * @param {number} y
   * @param {number} z
   * @param {THREE.Color} color
   *
   * @memberOf VoxelMapModel
   */
  constructor (position, scale, color) {
    super(position, MapModelType.VOXEL)

    // Register member variables
    this.scale = scale || 1
    this.color = color || new THREE.Color(0xffffff)

    this.setup()
  }

  /**
   * This function is used to create a THREE.Object3D representing
   * a voxel for this model
   *
   * @memberOf VoxelMapModel
   */
  setup () {
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
