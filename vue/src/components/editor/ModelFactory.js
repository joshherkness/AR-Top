<<<<<<< HEAD
import { EntityGridModel, TileGridModel } from './GridModels'
import { ENTITY_DATA, MODEL_DATA } from './PreloadedObjects'
=======
import { GridModelType, VoxelGridModel , TileGridModel, EntityGridModel} from './GridModels'
import { ENTITY_DATA } from './PreloadedObjects'
>>>>>>> origin/Import-entity-models-to-Unity

/**
 * Factory used to create instances of map models based on
 * a data object representing the model. The type field is
 * used to classify each model.
 *
 * @export
 * @class ModelFactory
 */
export class ModelFactory {
  /**
   * Returns an instance of a map model created from the given
   * data object.
   *
   * @static
   * @param {any} data
   * @returns
   *
   * @memberOf ModelFactory
   */
  static createModel (data) {
    // All models must have these properties
    if (!data || !data.type || !data.position) return null

    // Create the type based instance of our model
<<<<<<< HEAD
    if (ENTITY_DATA.map(data => data.type).includes(data.type)) {
      return new EntityGridModel(data.position, data.color, data.type)
    } else if (MODEL_DATA.map(data => data.type).includes(data.type)) {
      return new TileGridModel(data.position, data.color, data.type)
=======
    if (data.type === GridModelType.VOXEL && data.color) {
      return new VoxelGridModel(data.position, data.color)
    } else if (ENTITY_DATA.map(data => data.type).includes(data.type)) {
      return new EntityGridModel(data.position, data.color, data.type)
>>>>>>> origin/Import-entity-models-to-Unity
    }

    return null
  }
}
