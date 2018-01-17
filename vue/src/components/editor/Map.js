import * as THREE from 'three'

import { MapUtils } from './MapUtils'

const DEFAULT_MAP_SIZE = 40
const DEFAULT_MAP_HEIGHT = 1000
const DEFAULT_MAP_UNIT_SIZE = 50
const DEFAULT_CURSOR_OPACITY = 0.5

/**
 * This class represents a map.
 *
 * @class Map
 *
 */
export class Map extends THREE.EventDispatcher {
  /**
   * Constructor used to create a Map using a specified size.
   *
   * @param {THREE.Vector3} size
   *
   * @memberOf Map
   */
  constructor (size, height, unitSize) {
    super()

    // Register member variables
    this.size = size > 0 ? size : DEFAULT_MAP_SIZE
    this.height = height > 0 ? height : DEFAULT_MAP_HEIGHT
    this.unitSize = unitSize || DEFAULT_MAP_UNIT_SIZE

    // Calculated variables
    this.actualSize = this.size * this.unitSize
    this.actualHeight = this.height * this.unitSize

    this.models = []

    // Setup the scene
    this._setupScene()

    this.cursorPosition = new THREE.Vector3(-1, -1, -1)
  }

  /**
   * Appends new model to the map, returning true if the model is added, and
   * false otherwise. _Optionally forced_ will replace any models that occupy
   * the same position first.
   *
   * @param {AbstractMapModel} model
   * @param {boolean} forced
   * @returns {boolean} true if model is added
   *
   * @memberOf Map
   */
  add (model, forced = false) {
    // Ensure that the model is defined
    if (!model) return false

    // Ensure that the model is within the bounds of the map
    if (!MapUtils.isPositionWithinBounds(this, model.position)) {
      throw new Error('Cannot add to position, position outside map bounds.')
    }

    // Remove the occupying model if forced
    let occupyingModel = this.at(model.position)
    if (occupyingModel) {
      if (!forced) return
      this.remove(occupyingModel)
    }

    // Add the model
    this.models.push(model)

    // Add the model object to the scene
    model.object.position.copy(MapUtils.convertUnitToActualPosition(this, model.position))
    this.scene.add(model.object)

    this._needsRedraw()
  }

  /**
   * Removes model from the map, returning the removed model.
   *
   * @param {AbstractMapModel} model
   * @returns {AbstractMapModel}
   *
   * @memberOf Map
   */
  remove (model) {
    // Ensure that the model is defined
    if (!model) return false

    let index = this.models.findIndex((_model) => {
      return model.object.id === _model.object.id
    })

    // Remove the model
    let removedModels = this.models.splice(index, 1)
    let removedModel = removedModels[0]

    // Remove the model from the scene
    if (removedModel && this.scene) {
      let object = this.scene.getObjectById(removedModel.object.id)
      this.scene.remove(object)

      // Dispatch update event
      this.dispatchEvent({type: 'update', message: 'Scene has been updated'})
    }

    return removedModel
  }

  /**
   * Removes model from the map using position.
   *
   * @param {THREE.Vector3} position
   * @returns {AbstractMapModel}
   *
   * @memberOf Map
   */
  removeAt (position) {
    let model = this.at(position)
    return this.remove(model)
  }

  /**
   * Searches through the map models and returns the first with a matching
   * unit position. A value of _undefined_ is returned if no matching model
   * exists.
   *
   * @param {THREE.Vector3} position
   * @returns {AbstractMapModel}
   *
   * @memberOf Map
   */
  at (position) {
    return this.with('position', position)
  }

  /**
   * Searches through the map models and returns the first with a matching
   * key value. A value of _undefined_ is returned if no matching model exists.
   *
   * @param {string} key
   * @param {any} value
   * @returns
   *
   * @memberOf Map
   */
  with (key, value) {
    return this.models.find((model) => {
      return model[key] && model[key] === value
    })
  }

  /**
   * Update the cursor position based on actual position coordinates within
   * the THREE.Scene.
   * 
   * - Note that we simply convert it to its respective unit position, and
   *   update the position of the cursor only if needed.
   * 
   * @param {THREE.Vector3} actualPosition 
   * 
   * @memberOf Map
   */
  setCursorActualPosition (actualPosition) {
    // Convert to unit position
    let unitPosition = MapUtils.convertActualToUnitPosition(this, actualPosition)

    // Ensure that the cursor position needs to be updated
    if (this.cursorModel && this.cursorModel.position.equals(unitPosition)) return

    // Update the cursor position using converted unit position
    this.setCursorUnitPosition(unitPosition)
  }

  /**
   * Update the cursor position based on the unit position coordinates within
   * the map.
   * 
   * - Note that an out of bounds position will not be used to update the
   *   cursor position.
   * 
   * @param {THREE.Vector3} unitPosition 
   * 
   * @memberOf Map
   */
  setCursorUnitPosition (unitPosition) {
    // Check bounds of new position
    let isWithinBounds = MapUtils.isPositionWithinBounds(this, unitPosition)

    this.cursorPosition = isWithinBounds ? unitPosition : new THREE.Vector3(-1, -1, -1)

    if (this.cursorModel && this.cursorModel.position) {
      this.cursorModel.position.copy(unitPosition)
    }

    // Retrieve and update the cursor
    let cursor = this.scene.getObjectByName('cursor')
    if (!cursor) return

    cursor.visible = isWithinBounds
    cursor.position.copy(MapUtils.convertUnitToActualPosition(this, unitPosition))

    this._needsRedraw()
  }

  /**
   * Update the model used for the cursor.
   * 
   * - Note that the position of the specified model will be ignored, and
   *   replaced with the current cursor model position.
   * 
   * @param {AbstractMapModel} model 
   * 
   * @memberOf Map
   */
  setCursorModel (model) {
    if (!model.object) return

    // Remove the current cursor from the scene
    let currentCursorObject = this.scene.getObjectByName('cursor')
    this.scene.remove(currentCursorObject)

    this.cursorModel = model

    // Add cursor to scene
    model.object.name = 'cursor'
    model.object.visible = true
    model.object.material.opacity = DEFAULT_CURSOR_OPACITY
    model.object.material.transparent = true
    model.object.position.copy(MapUtils.convertUnitToActualPosition(this, this.cursorModel.position))

    this.scene.add(model.object)

    this._needsRedraw()
  }

  /**
   * Search model objects within the map, and return the first one that the
   * specified raycaster intersects with. Otherwise, a value of _undefined_
   * will be returned.
   * 
   * - Note that the 'grid-plane' object should be included in the search,
   *   so that the user can interact with the grid.
   * 
   * @param {THREE.Raycaster} raycaster 
   * @returns {THREE.Object3D}
   * 
   * @memberOf Map
   */
  getFirstIntersectObject(raycaster) {

    if (!raycaster) {
      throw new Error('Raycaster must be defined')
    }

    let objects = this.models.map((model) => model.object)

    // Add the grid, so we can still interact with it
    let grid = this.scene.getObjectByName('grid-plane')
    if (grid) {
      objects.push(grid)
    }

    let intersectObjects = raycaster.intersectObjects(objects, true)

    if (intersectObjects.length === 0) {
      return undefined
    }

    return intersectObjects[0]
  }

  /**
   * This function should be used internally to dsipatch events targeted
   * toward redraw of the map.
   * 
   * @memberOf Map
   */
  _needsRedraw() {
    this.dispatchEvent({
      type: 'redraw', 
      message: 'Map has been updated, and a redraw is required.'
    })
  }

  /**
   * This function should be used internally to setup the scene.
   * 
   * @private
   * 
   * @memberOf Map
   */
  _setupScene () {
    this.scene = new THREE.Scene()
    this.scene.background = new THREE.Color(0xbbbbbb)
    this._setupLighting()
    this._setupGrid()
    this._setupGridBase()
  }

  /**
   * This function should be used internally to setup lighting within
   * the scene.
   * 
   * @private
   * 
   * @memberOf Map
   */
  _setupLighting () {
    // Ensure teh scene exists
    if (!this.scene) return

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

  /**
   * This function should be used internally to setup the grid within
   * the scene. This includes the creation of the grid lines by using
   * THREE.GridHelper class, as well as the creation of the grid plane
   * overlapping the lines in order to allow user interaction.
   * 
   * @private
   * 
   * @memberOf Map
   */
  _setupGrid () {
    // Ensure teh scene exists
    if (!this.scene) return

    // Create the grid
    var lineColor = new THREE.Color(0x434b54)
    var lines = new THREE.GridHelper(this.actualSize, this.size, lineColor, lineColor)
    lines.name = 'grid-lines'
    this.scene.add(lines)

    // Create the grid plane used for user interraction
    var gridPlaneGeometry = new THREE.PlaneBufferGeometry(this.actualSize, this.actualSize)
    gridPlaneGeometry.rotateX(-Math.PI / 2)
    var gridPlane = new THREE.Mesh(gridPlaneGeometry, new THREE.MeshBasicMaterial({ visible: false }))
    gridPlane.name = 'grid-plane'
    this.scene.add(gridPlane)
  }

  /**
   * This function should be used internally to setup the grid base within
   * the scene.
   * 
   * - Note that this is purely for asthetics, and serves no functional 
   *   purpose.
   * 
   * @private
   * 
   * @memberOf Map
   */
  _setupGridBase () {
    // Ensure teh scene exists
    if (!this.scene) return

    let baseColor = new THREE.Color(0x545d67)
    let baseMaterial = new THREE.MeshLambertMaterial({color: baseColor})
    let baseGeometry = new THREE.CubeGeometry(this.actualSize, this.unitSize, this.actualSize)
    let base = new THREE.Mesh(baseGeometry, baseMaterial)

    // Place the base just below the grid
    base.position.y = -(this.unitSize / 2) - 1

    // Add to the scene
    this.scene.add(base)
  }
}
