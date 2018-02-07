import 'three'
import 'three/examples/js/loaders/OBJLoader'
import 'three/examples/js/loaders/MTLLoader'

import TileFloorOBJData from '@/assets/models/tile_floor.obj'
import TileFloorMTLData from '@/assets/models/tile_floor.mtl'


// Load the tile floor object
var mtlLoader = new THREE.MTLLoader()
let tile_floor_materials = mtlLoader.parse(TileFloorMTLData)
tile_floor_materials.preload()

var objLoader = new THREE.OBJLoader()
objLoader.setMaterials(tile_floor_materials)
let tile_floor_object = objLoader.parse(TileFloorOBJData)

export {
    tile_floor_object as TileFloorObject,
}