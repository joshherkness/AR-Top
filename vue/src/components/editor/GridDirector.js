import * as THREE from 'three'
import { GridScene } from './GridScene'
import { ModelFactory } from './ModelFactory'
import { Grid } from './Grid'

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
   * Remove all currently tracked models from the current grid
   * as well as their corresponding objects from the current scene.
   * 
   * 
   * @memberOf GridDirector
   */
  clear () {
    var dirty = false
    this.objectMap.forEach((key, value) => {
      this.grid.remove(key)
      this.scene.remove(value)
      dirty = true
    })

    if (dirty) {
      this._onUpdate()
    }
  }

  load (grid) {
    this.grid = grid
    this.objectMap.clear()
    this.scene = new GridScene(this.grid, this.scale)
    
    var isDirty = false
    this.grid.models.forEach((model) => {
      let object = model.createObject(this.scale)
      object.position.clone(this.convertUnitToActualPosition(model.position))
      this.objectMap.set(model, object)
      this.scene.add(object)
      isDirty = true
    })

    if (isDirty) {
      this._onUpdate()
    }
  }

  add (model) {
    if (!this.grid) return
    if (model.position && !this.grid.isWithinBounds(model.position)) {
      throw new Error('Cannot add to position, position outside map bounds.')
    }

    if (this.grid.add(model)) {
      let object = model.createObject(this.scale)
      object.position.clone(this.convertUnitToActualPosition(model.position))
      this.objectMap.set(model, object)
    
      if (this.scene) {
        this.scene.add(object)
      }

      this._onUpdate()
    }
  }

  remove (model) {
    if (!this.grid) return

    let removedModel = this.grid.remove(model)
    if (removedModel) {
      let objectId = this.objectMap.get(removedModel).id
      let object = this.scene.getObjectById(objectId)
      this.scene.remove(object)
      this.objectMap.delete(removedModel)
      this._onUpdate()
    }
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

  get objects () {
    return Array.from(manager.objectMap.values())
  }

  _onUpdate () {
    this.dispatchEvent({
      type: 'update',
      message: this.grid
    })
  }
}