import * as THREE from 'three'

import { ModelFactory } from './ModelFactory'

export class Grid {
  constructor (width, height, depth, color, { id, name, models = [] } = {}) {
    // Check for required parameters
    if (width === undefined) {
      throw new Error('Width must be defined')
    }

    if (height === undefined) {
      throw new Error('Height must be defined')
    }

    if (depth === undefined) {
      throw new Error('Depth must be defined')
    }

    if (color === undefined) {
      throw new Error('Color must be defined')
    }

    this.width = width
    this.height = height
    this.depth = depth
    this.color = color
    this.id = id
    this.name = name
    this.models = []

    if (models) {
      // Models property must be an array
      if (!(models instanceof Array)) {
        throw new TypeError('Optional property of models must be of type Array')
      }

      models.forEach((data) => {
        this.add(ModelFactory.createModel(data))
      })
    }
  }

  /**
   * Add the specified grid model into the grid only if the position is unoccupied
   * and within bounds, returning true. Otherwise a value of false is returned.
   *
   * @param {GridModel} model
   * @returns
   *
   * @memberOf Grid
   */
  add (model) {
    const isWithinBounds = this.isWithinBounds(model.position)
    const isPositionUnoccupied = !this.at(model.position)

    // Add only if within bounds and position is unoccupied
    if ((isWithinBounds && isPositionUnoccupied)) {
      this.models.push(model)
      return true
    }
    return false
  }

  /**
   * Returns the first model which has a matchin position value. Otherwise,
   * a value of undefined will be returned.
   *
   * @param { {number, number, number} } { x, y, z } position
   * @returns
   *
   * @memberOf Grid
   */
  at ({ x, y, z }) {
    return this.models.find((model) => {
      let position = new THREE.Vector3(x, y, z)
      return model.position.equals(position)
    })
  }

  /**
   * Removes the first model matching that specified, returning the removed
   * model. Otherwis, a value of undefined will be returned.
   *
   * @param {GridModel} model
   * @returns
   *
   * @memberOf Grid
   */
  remove (model) {
    if (!model) {
      return new TypeError('Property model is undefined')
    }

    let index = this.models.findIndex((_model) => {
      return model.equals(_model)
    })

    return this.models.splice(index, 1)[0] || undefined
  }

  /**
   * Removes the first model which has a matching position value, returning
   * the removed model. Otherwise, a value of undefined will be returned.
   *
   * @param { {number, number, number} } { x, y, z} position
   * @returns
   *
   * @memberOf Grid
   */
  removeAt ({ x, y, z }) {
    let model = this.at({ x, y, z })
    return this.remove(model)
  }

  /**
   * Returns true if the specified three dimensional position is within
   * the bounds of the map.
   *
   * @param { {number, number, number} } { x, y, z } position
   * @returns
   *
   * @memberOf Grid
   */
  isWithinBounds ({ x, y, z }) {
    return ((x >= 0 && x < this.width) &&
    (y >= 0 && y < this.height) &&
    (z >= 0 && z < this.depth))
  }

  /**
   * Serialize this grid into a JSON string.
   *
   * @param {number} [space=2]
   * @returns
   *
   * @memberOf Grid
   */
  serialize (space = 2) {
    return JSON.stringify(this, null, space)
  }

  /**
   * Deserialize a Grid object based on a data.
   *
   * @static
   * @param {any} data
   * @returns
   *
   * @memberOf Grid
   */
  static deserialize (data) {
    let {width, height, depth, color, ...optional} = data
    return new Grid(width, height, depth, color, optional)
  }
}
