import * as THREE from 'three'
import { GridScene } from './GridScene'

/**
 * Acts as a mediator between a grid and a scene, keeping the two in sync.
 *
 * @export
 * @class GridDirector
 * @extends {THREE.EventDispatcher}
 */
export class GridDirector extends THREE.EventDispatcher {
  constructor ({scale = 50} = {}) {
    super()

    this.grid = null
    this.scene = null
    this.scale = scale
    this.objectMap = new Map()
  }

  /**
   * Remove all tracked models and objects from the grid and scene
   * respectively.
   *
   *
   * @memberOf GridDirector
   */
  clear () {
    if (this.objectMap.size <= 0) {
      // There is nothing to clear, exit early
      return
    }

    this.objectMap.forEach((key, value) => {
      // Remove the model from the grid
      this.grid.remove(key)
      // Remove the object from the scene
      this.scene.remove(value)
    })
  }

/**
 * Asynchronously load a grid, creating a usable scene and loading any existing
 * models into that scene.
 *
 * @param {any} grid
 *
 * @memberOf GridDirector
 */
  async load (grid) {
    try {
      this.initSelection()

      this.grid = grid
      this.objectMap.clear()
      this.scene = new GridScene(this.grid, this.scale)

      this.grid.models.forEach((model) => {
        let object = model.createObject(this.scale)
        object.position.copy(this.convertUnitToActualPosition(model.position))
        this.objectMap.set(model, object)
        this.scene.add(object)
      })
    } catch (error) {
      throw error
    }
  }

  /**
   * Adds one or more models into both the grid and scene.
   *
   * @param {any} model
   *
   * @memberOf GridDirector
   */
  add (...models) {
    if (!this.grid) return

    models.forEach((model) => {
      if (model.position && !this.grid.isWithinBounds(model.position)) {
        throw new Error('Cannot add to position, position outside map bounds.')
      }

      if (this.grid.add(model)) {
        let object = model.createObject(this.scale)
        object.position.copy(this.convertUnitToActualPosition(model.position))
        console.log(object.position)
        this.objectMap.set(model, object)

        if (this.scene) {
          this.scene.add(object)
        }
      }
    })

    this._onUpdate()
  }

  remove (...models) {
    if (!this.grid) return

    models.forEach((model) => {
      let removedModel = this.grid.remove(model)
      if (removedModel) {
        let objectId = this.objectMap.get(removedModel).id
        let object = this.scene.getObjectById(objectId)

        // We don't necessarily know the parent of the object, so we remove
        // it from any parent in the scene.
        // TODO: this could be costly on larger scenes.
        this.scene.traverse((child) => {
          child.remove(object)
        })

        this.objectMap.delete(removedModel)
      }
    })

    this._onUpdate()
  }

  setSelection (unitPosition, { model } = {}) {
    if (!this.scene) return

    // First, we want to clear any current selection
    this.clearSelection()

    let occupyingModel = this.grid.at(unitPosition)
    if (occupyingModel) {
      // Add the model to the model selection group
      let object = this.objectMap.get(occupyingModel)
      if (!object) {
        throw new Error('An object should exist.')
      }

      object.material.transparent = true
      object.material.opacity = 0.5

      this.scene.remove(object)

      let group = this.scene.getObjectByName('model-selection')
      group.add(object)
    } else {
      // Create a selection using the provided model
      if (!model) {
        throw new Error('Property model must be defined')
      }

      let object = model.createObject(this.scale)
      object.position.copy(this.convertUnitToActualPosition(unitPosition))
      object.material.transparent = true
      object.material.opacity = 0.5
      let group = this.scene.getObjectByName('selection')
      group.add(object)
    }

    this._onUpdate()
  }

  initSelection () {
    if (!this.scene) return

    let a = this.scene.getObjectByName('selection')
    this.scene.remove(a)
    let b = this.scene.getObjectByName('model-selection')
    this.scene.remove(b)

    let group = new THREE.Group()
    group.name = 'selection'
    this.scene.add(group)

    let modelGroup = new THREE.Group()
    modelGroup.name = 'model-selection'
    this.scene.add(modelGroup)
  }

  clearSelection () {
    if (!this.scene) {
      return
    }

    // Clean up any current selections
    let group = this.scene.getObjectByName('selection')
    if (group) {
      this.scene.remove(group)
    }

    let modelGroup = this.scene.getObjectByName('model-selection')
    if (modelGroup) {
      modelGroup.children.forEach((child) => {
        if (child.material) {
          child.material.transparent = true
          child.material.opacity = 1.0
        }
        this.scene.add(child)
        modelGroup.remove(child)
      })
    }

    // Hard reset the selection, now that we cleaned up
    this.initSelection()

    this._onUpdate()
  }

  convertActualToUnitPosition (actualPosition) {
    // Ensure the the grid is defined
    if (!this.grid) throw new Error('Grid must be defined.')

    let offset = new THREE.Vector3(this.scene.actualWidth / 2, 0, this.scene.actualDepth / 2)
    return actualPosition
      .clone()
      .add(offset)
      .divideScalar(this.scale)
      .floor()
      .multiplyScalar(this.scale)
      .divideScalar(this.scale)
  }

  convertUnitToActualPosition (unitPosition) {
    // Ensure that the grid is defined
    if (!this.grid) throw new Error('Grid must be defined.')

    let offset = new THREE.Vector3(this.scene.actualWidth / 2, 0, this.scene.actualDepth / 2)

    return unitPosition
      .clone()
      .multiplyScalar(this.scale)
      .addScalar(this.scale / 2)
      .sub(offset)
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
  getFirstIntersectData (raycaster) {
    if (!raycaster) throw new Error('Raycaster must be defined')

    let objects = this.objects

    // Add the grid, so we can still interact with it
    let grid = this.scene.getObjectByName('grid-plane')
    if (grid) {
      objects.push(grid)
    }

    let intersectData = raycaster.intersectObjects(objects, true)

    if (intersectData.length === 0) {
      return undefined
    }

    // Return the first intersect that contains a face value, otherwise something
    // like a wireframe can be returned
    return intersectData.find((intersect) => {
      return intersect.face
    })
  }

  /**
   * Returns a complete list of the scene objects that are mapped by our models.
   *
   * @readonly
   *
   * @memberOf GridDirector
   */
  get objects () {
    return Array.from(this.objectMap.values())
  }

  /**
   * Function should only be called internally to notify any event
   * listeners that there has been an update.
   *
   * @memberOf GridDirector
   */
  _onUpdate () {
    this.dispatchEvent({
      type: 'update',
      message: this.grid
    })
  }
}
