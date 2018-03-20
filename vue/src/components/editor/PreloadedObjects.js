import * as THREE from 'three'
import 'three/examples/js/loaders/OBJLoader'
import 'three/examples/js/loaders/MTLLoader'

let MODEL_DATA = [
  {
    type: 'floor',
    display: 'Floor'
  }
]

let ENTITY_DATA = [
  {
    type: 'fighter',
    display: 'Fighter'
  },
  {
    type: 'ranger',
    display: 'Ranger'
  },
  {
    type: 'knight',
    display: 'Knight'
  },
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
  object.name = 'main'

  // Create bounding box
  // Todo: Find some way to make this not hard coded
  let geometry = new THREE.BoxGeometry(16, 16, 16)
  let material = new THREE.MeshPhongMaterial({
    transparent: true,
    opacity: 0
  })
  let boundingBox = new THREE.Mesh(geometry, material)
  boundingBox.name = 'bounding_box'
  boundingBox.position.y = 8
  boundingBox.userData = {
    isBoundingBox: true
  }

  let group = new THREE.Group()
  group.add(object)
  group.add(boundingBox)

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
  var entityBase = BASE_OBJECT.clone()
  entityBase.name = 'base'
  entityBase.scale.set(16, 16, 16)

  group.add(entityBase)

  return group
}

let ObjectList = {}

// Preload all models
MODEL_DATA.forEach((data) => {
  if (!data.type) throw TypeError('MODEL_DATA element must have a type attribute')

  // Load the model
  ObjectList[data.type] = loadModel(data.type)
})

// Preload all entities
ENTITY_DATA.forEach((data) => {
  if (!data.type) throw TypeError('ENTITY_DATA element must have a type attribute')

  // Load the entity
  ObjectList[data.type] = loadEntity(data.type)
})

export {
  ObjectList,
  MODEL_DATA,
  ENTITY_DATA,
  BASE_RING_OBJECT_NAME,
  BASE_CENTER_OBJECT_NAME
}
