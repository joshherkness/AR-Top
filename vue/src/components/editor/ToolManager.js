import * as THREE from 'three'

import { ModelFactory } from '@/components/editor/ModelFactory'

class Tool {
  constructor () {
    this.type = null
    this.keyCode = null
    this.icon = null
    this.options = null
  }

  onMouseDown () {}
  onMouseUp () {}
  onMouseMove () {}
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
}

class DeleteTool extends Tool {
  constructor () {
    super()

    this.type = 'delete'
    this.keyCode = 50
    this.icon = 'mdi-eraser'
  }

  onMouseUp (event, director, raycaster) {
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

export let ToolManager = (() => {
  // Instance of tool manager used for singleton
  let instance = null

  class ToolManager {
    constructor () {
      this.tools = [
        new PlaceTool(),
        new DeleteTool()
      ]

      this.tool = this.tools[0] || null
      this.disabled = false

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
          this.tool = tool
        }
      })
    }

    onMouseDown (event, director, raycaster) {
      // Save the mouse down position
      this.mouseDown = {
        x: (event.offsetX / window.innerWidth) * 2 - 1,
        y: -(event.offsetY / window.innerHeight) * 2 + 1
      }

      if (this.disabled) {
        return
      }

      // Call tool mouse down
      if (this.tool) {
        this.tool.onMouseDown(event, director, raycaster)
      }
    }

    onMouseUp (event, director, raycaster) {
      // Reset the mouse down position
      this.mouseDown = null

      if (this.disabled) {
        this.disabled = false
        return
      }

      // Call tool mouse up
      if (this.tool) {
        this.tool.onMouseUp(event, director, raycaster)
      }
    }

    onMouseMove (event, director, raycaster) {
      // Save the mouse position
      this.mouse = {
        x: (event.offsetX / window.innerWidth) * 2 - 1,
        y: -(event.offsetY / window.innerHeight) * 2 + 1
      }

      // Determine whether the disable the tool.
      // I.e. disable the tool when the mouse moves a certain threshold from
      // the mouse down location
      let disableThreshold = 0.01
      if (this.mouseDown &&
        (Math.abs(this.mouse.x - this.mouseDown.x) > disableThreshold ||
        Math.abs(this.mouse.y - this.mouseDown.y) > disableThreshold)) {
        this.disabled = true
      }

      if (this.disabled) {
        director.clearSelection()
        return
      }

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
