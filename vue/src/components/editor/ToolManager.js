import * as THREE from 'three'

import { ModelFactory } from '@/components/editor/ModelFactory'

class Tool {
  constructor () {
    this.type = null
    this.keyCode = null
    this.icon = null
    this.options = null

    // Mouse data
    this.mouse = null
    this.mouseDown = null
  }

  onMouseDown () {
    // Save the mouse down position
    this.mouseDown = {
      x: (event.offsetX / window.innerWidth) * 2 - 1,
      y: -(event.offsetY / window.innerHeight) * 2 + 1
    }
  }

  onMouseUp () {
    // Reset the mouse down position
    this.mouseDown = null
  }

  onMouseMove () {
    // Save the mouse position
    this.mouse = {
      x: (event.offsetX / window.innerWidth) * 2 - 1,
      y: -(event.offsetY / window.innerHeight) * 2 + 1
    }
  }

  isDisabled () { return false }
  isRotateDisabled () { return false }
}

class PlaceTool extends Tool {
  constructor () {
    super()

    this.type = 'place'
    this.keyCode = 49
    this.icon = 'mdi-cube-outline'

    this.options = {
      type: 'fighter',
      color: {
        hex: '#ffffff'
      }
    }
  }

  onMouseUp (event, director, raycaster) {
    // Cache the disabled state
    let disabled = this.isDisabled()

    super.onMouseUp()

    if (disabled) {
      director.clearSelection()
      return
    }

    // Create and place model
    let data = director.getFirstIntersectData(raycaster)

    // Ensure that intersect data exists, otherwise we don't care
    if (!data || !data.object) return

    // Determine the unit position we need to interact with
    let interactPosition = new THREE.Vector3()
    if (!data.face) return
    interactPosition.copy(data.point.add(data.face.normal))
    let unitPosition = director.convertActualToUnitPosition(interactPosition)

    // Create the model
    let model = ModelFactory.createModel({
      type: this.options.type,
      color: this.options.color.hex,
      position: unitPosition
    })

    // Add the model
    director.add(model)
  }

  onMouseMove (event, director, raycaster) {
    super.onMouseMove()

    if (this.isDisabled()) {
      director.clearSelection()
      return
    }

    // Update selection
    let data = director.getFirstIntersectData(raycaster)

    if (!data || !data.object) return

    // Determine the unit position we need to interact with
    let interactPosition = new THREE.Vector3()
    if (!data.face) return
    interactPosition.copy(data.point.add(data.face.normal))
    let unitPosition = director.convertActualToUnitPosition(interactPosition)

    // Create the model
    let model = ModelFactory.createModel({
      type: this.options.type,
      color: this.options.color.hex,
      position: unitPosition
    })

    // Set selection using this model
    director.setSelection(unitPosition, { model: model })
  }

  isDisabled () {
    let disableThreshold = 0.01
    if (this.mouseDown &&
      (Math.abs(this.mouse.x - this.mouseDown.x) > disableThreshold ||
      Math.abs(this.mouse.y - this.mouseDown.y) > disableThreshold)) {
      return true
    }
    return false
  }
}

class DeleteTool extends Tool {
  constructor () {
    super()

    this.type = 'delete'
    this.keyCode = 50
    this.icon = 'mdi-eraser'
  }

  onMouseUp (event, director, raycaster) {
    super.onMouseUp()

    // Get intersect data
    let data = director.getFirstIntersectData(raycaster)

    // Ensure that intersect data exists, otherwise we don't care
    if (!data || !data.object) return

    // Determine the unit position we need to interact with
    let interactPosition = new THREE.Vector3()
    interactPosition.setFromMatrixPosition(data.object.matrixWorld)
    let unitPosition = director.convertActualToUnitPosition(interactPosition)

    // Remove the model at this position
    let model = director.grid.at(unitPosition)
    director.remove(model)
  }

  onMouseMove (event, director, raycaster) {
    super.onMouseMove()

    let data = director.getFirstIntersectData(raycaster)

    // Ensure that intersect data exists, otherwise we don't care
    if (!data || !data.object) return

    // Determine the unit position we need to interact with
    let interactPosition = new THREE.Vector3()

    if (data.object.name === 'grid-plane') {
      director.clearSelection()
      return
    }
    interactPosition.setFromMatrixPosition(data.object.matrixWorld)

    let unitPosition = director.convertActualToUnitPosition(interactPosition)
    director.setSelection(unitPosition)
  }
}

class MoveTool extends Tool {
  constructor () {
    super()

    this.type = 'move'
    this.keyCode = 51
    this.icon = 'mdi-cursor-move'

    this.preventRotate = true

    this.data = {
      model: null
    }
  }

  onMouseDown (event, director, raycaster) {
    super.onMouseDown()

    // Get intersect data
    let data = director.getFirstIntersectData(raycaster)

    // Ensure that intersect data exists, otherwise we don't care
    if (!data || !data.object) return

    // Determine the unit position we need to interact with
    let interactPosition = new THREE.Vector3()

    if (data.object.name === 'grid-plane') {
      director.clearSelection()
      return
    }
    interactPosition.setFromMatrixPosition(data.object.matrixWorld)

    let unitPosition = director.convertActualToUnitPosition(interactPosition)

    // Copy and remove the model at this position
    let model = director.grid.at(unitPosition)
    this.data.model = model
    director.remove(model)
    director.setSelection(this.data.model.position, { model: this.data.model })

    event.stopPropagation()
  }

  onMouseUp (event, director, raycaster) {
    super.onMouseUp()

    // Add the model
    director.add(this.data.model)
    this.data.model = null
  }

  onMouseMove (event, director, raycaster) {
    super.onMouseMove()

    if (!this.data.model) {
      director.clearSelection()
      return
    }

    // Update selection
    let data = director.getFirstIntersectData(raycaster)

    if (!data || !data.object) return

    // Determine the unit position we need to interact with
    let interactPosition = new THREE.Vector3()
    if (!data.face) return
    interactPosition.copy(data.point.add(data.face.normal))
    let unitPosition = director.convertActualToUnitPosition(interactPosition)

    // Update the position
    this.data.model.position = unitPosition

    // Set selection using this model
    director.setSelection(unitPosition, { model: this.data.model })
  }

  isRotateDisabled () {
    return this.data.model
  }
}

export let ToolManager = (() => {
  // Instance of tool manager used for singleton
  let instance = null

  class ToolManager {
    constructor () {
      this.tools = [
        new PlaceTool(),
        new DeleteTool(),
        new MoveTool()
      ]

      this.tool = this.tools[0] || null

      this.mouse = null
      this.mouseDown = null
    }

    selectTool (type) {
      // Switch tools if possible
      this.tools.forEach((tool) => {
        if (type === tool.type) {
          this.tool = tool
        }
      })
    }

    onKeyPress (event) {
      // Switch tools if possible
      this.tools.forEach((tool) => {
        if (event.keyCode === tool.keyCode) {
          this.selectTool(tool.type)
        }
      })
    }

    onMouseDown (event, director, raycaster) {
      // Call tool mouse down
      if (this.tool) {
        this.tool.onMouseDown(event, director, raycaster)

        // Check if er have to manager our controls
        if (this.controls && this.tool.isRotateDisabled()) {
          this.controls.enableRotate = false
        } else {
          this.controls.enableRotate = true
        }
      }
    }

    onMouseUp (event, director, raycaster) {
      // Call tool mouse up
      if (this.tool) {
        this.tool.onMouseUp(event, director, raycaster)
      }

      if (this.controls) {
        this.controls.enableRotate = true
      }
    }

    onMouseMove (event, director, raycaster) {
      // Call tool mouse move
      if (this.tool) {
        this.tool.onMouseMove(event, director, raycaster)
      }
    }
  }

  return {
    getInstance: () => {
      if (instance == null) {
        instance = new ToolManager()
        instance.constructor = null
      }
      return instance
    }
  }
})()
