
import { EventDispatcher } from 'three'
import { MapUtils } from './MapUtils'

const DEFAULT_HIGHLIGHT_OPACITY = 0.5

export class SelectionManager extends EventDispatcher {
  /**
   * Construct selection manager.
   *
   * - Note that a map must be provided.
   *
   * @param {any} map
   *
   * @memberOf SelectionManager
   */
  constructor (map) {
    super()

    // Ensure that the map is defined
    if (map === undefined) {
      throw new TypeError('Argument of type map must be defined')
    }

    this.map = map
    this.selectedModel = null
    this.highlightedModel = null
  }

  /**
  * Clears the current selection within the map.
  *
  * @memberOf SelectionManager
  */
  clear () {
    // Make sure there is a map we can reference
    if (!this.map) {
      return
    }

    if (this.selectedModel) {
      // Reset transparency
      this.selectedModel.object.material.opacity = 1.0
      this.selectedModel.object.material.transparent = false
      this.selectedModel = null
    }

    if (this.highlightedModel) {
      // Remove from the scene
      let highlightedObject = this.map.scene.getObjectByName(this.highlightedModel.object.name)
      this.map.scene.remove(highlightedObject)
      this.highlightedModel = null
    }

    this._onChanged()
  }

  /**
  * Selects the specified position within the current map. If the position
  * is empty, the specified model will be used, otherwise we set the opacity
  * of the model rendered in that position.
  *
  * @param {any} unitPosition
  * @param {any} model
  *
  * @memberOf SelectionManager
  */
  selectAt (unitPosition, model) {
    // Make sure there is a map we can reference
    if (!this.map) {
      return
    }

    // Don't change selection if the position of the selection remains the same
    if (this.isSelected(unitPosition)) {
      return
    }

    this.clear()

    // If the unit position is outside map bounds, don't update
    if (!MapUtils.isPositionWithinBounds(this.map, unitPosition)) {
      return
    }

    // Determine if a model exists at this location within the map
    let occupyingModel = this.map.at(unitPosition)
    if (occupyingModel) {
      this.selectedModel = occupyingModel
      this.selectedModel.object.material.opacity = DEFAULT_HIGHLIGHT_OPACITY
      this.selectedModel.object.material.transparent = true
    } else if (model) {
      // We use this model, updating onyl its position
      this.highlightedModel = model
      this.highlightedModel.position.copy(unitPosition)
      this.highlightedModel.object.position.copy(MapUtils.convertUnitToActualPosition(this.map, unitPosition))
      this.highlightedModel.object.material.opacity = DEFAULT_HIGHLIGHT_OPACITY
      this.highlightedModel.object.material.transparent = true
      this.highlightedModel.object.name = 'highlight'
      this.map.scene.add(this.highlightedModel.object)
    } else {
      // No model is specified
      return
    }

    this._onChanged()
  }

  /**
  * Returns true if the specified unit position is selected.
  *
  * @param {any} unitPosition
  *
  * @memberOf SelectionManager
  */
  isSelected (unitPosition) {
    if (this.selectedModel) {
      return this.selectedModel.position.equals(unitPosition)
    } else if (this.highlightedModel) {
      return this.highlightedModel.position.equals(unitPosition)
    } else {
      return false
    }
  }

  /**
  * This function should be used internally to dsipatch events targeted
  * toward selection changed.
  *
  * @memberOf Map
  */
  _onChanged () {
    this.dispatchEvent({
      type: 'change',
      message: 'Selection has been changed'
    })
  }
}
