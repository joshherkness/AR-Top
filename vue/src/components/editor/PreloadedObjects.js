import * as THREE from 'three'
import 'three/examples/js/loaders/OBJLoader'
import 'three/examples/js/loaders/MTLLoader'

let MODEL_DATA = [
  {
<<<<<<< HEAD
    type: 'voxel',
    display: 'Voxel'
  },
  {
    type: 'wall',
    display: 'Wall'
  },
  {
=======
>>>>>>> origin/Import-entity-models-to-Unity
    type: 'floor',
    display: 'Floor'
  }
]

let ENTITY_DATA = [
  {
    type: 'fighter',
    display: 'Fighter'
<<<<<<< HEAD
  },
  {
    type: 'ranger',
    display: 'Ranger'
  },
  {
    type: 'knight',
    display: 'Knight'
  },
=======
  }, 
  {
    type: 'ranger',
    display: 'Ranger'
  }, 
  {
    type: 'knight',
    display: 'Knight'
  }, 
>>>>>>> origin/Import-entity-models-to-Unity
  {
    type: 'goblin',
    display: 'Goblin'
  }
]

// Load the base object and note some other useful base related constants
var BASE_OBJECT = loadObject('base')
var BASE_RING_OBJECT_NAME = 'base.ring'
var BASE_CENTER_OBJECT_NAME = 'base.center'

function loadObject (name) {
  let objData = require(`@/assets/models/${name}.obj`)
  let mtlData = require(`@/assets/models/${name}.mtl`)

  // Load materials
  var mtlLoader = new THREE.MTLLoader()
  let materials = mtlLoader.parse(mtlData)
  materials.preload()

  // Create object
  var objLoader = new THREE.OBJLoader()
  objLoader.setMaterials(materials)
  return objLoader.parse(objData)
}

function loadModel (name) {
  // Load the object
  let object = loadObject(name)
<<<<<<< HEAD
  object.name = 'main'
=======
  object.name = "main"
>>>>>>> origin/Import-entity-models-to-Unity

  // Create bounding box
  // Todo: Find some way to make this not hard coded
  let geometry = new THREE.BoxGeometry(16, 16, 16)
  let material = new THREE.MeshPhongMaterial({
    transparent: true,
    opacity: 0
  })
<<<<<<< HEAD
  let boundingBox = new THREE.Mesh(geometry, material)
  boundingBox.name = 'bounding_box'
  boundingBox.position.y = 8
  boundingBox.userData = {
=======
  let bounding_box = new THREE.Mesh(geometry, material)
  bounding_box.name = "bounding_box"
  bounding_box.position.y = 8
  bounding_box.userData = {
>>>>>>> origin/Import-entity-models-to-Unity
    isBoundingBox: true
  }

  let group = new THREE.Group()
  group.add(object)
<<<<<<< HEAD
  group.add(boundingBox)
=======
  group.add(bounding_box)
>>>>>>> origin/Import-entity-models-to-Unity

  return group
}

function loadEntity (name) {
  // Load the object
  let group = loadModel(name)

  // Shift the main object above the base
  group.traverse((node) => {
    if (node.name === 'main') {
      node.position.y = 1
    }
  })

  // Create the base
<<<<<<< HEAD
  var entityBase = BASE_OBJECT.clone()
  entityBase.name = 'base'
  entityBase.scale.set(16, 16, 16)

  group.add(entityBase)
=======
  var entity_base = BASE_OBJECT.clone()
  entity_base.name = "base"
  entity_base.scale.set(16, 16, 16)

  group.add(entity_base)
>>>>>>> origin/Import-entity-models-to-Unity

  return group
}

let ObjectList = {}

// Preload all models
MODEL_DATA.forEach((data) => {
<<<<<<< HEAD
  if (!data.type) throw TypeError('MODEL_DATA element must have a type attribute')
=======
  if (!data.type) throw TypeError("MODEL_DATA element must have a type attribute")
>>>>>>> origin/Import-entity-models-to-Unity

  // Load the model
  ObjectList[data.type] = loadModel(data.type)
})

// Preload all entities
ENTITY_DATA.forEach((data) => {
<<<<<<< HEAD
  if (!data.type) throw TypeError('ENTITY_DATA element must have a type attribute')
=======
  if (!data.type) throw TypeError("ENTITY_DATA element must have a type attribute")
>>>>>>> origin/Import-entity-models-to-Unity

  // Load the entity
  ObjectList[data.type] = loadEntity(data.type)
})

export {
<<<<<<< HEAD
  ObjectList,
=======
  ObjectList as ObjectList,
>>>>>>> origin/Import-entity-models-to-Unity
  MODEL_DATA,
  ENTITY_DATA,
  BASE_RING_OBJECT_NAME,
  BASE_CENTER_OBJECT_NAME
<<<<<<< HEAD
}
=======
}
>>>>>>> origin/Import-entity-models-to-Unity
