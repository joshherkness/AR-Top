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
  object.name = "main"

  // Create bounding box
  // Todo: Find some way to make this not hard coded
  let geometry = new THREE.BoxGeometry(16, 16, 16)
  let material = new THREE.MeshPhongMaterial({
    transparent: true,
    opacity: 0
  })
  let bounding_box = new THREE.Mesh(geometry, material)
  bounding_box.name = "bounding_box"
  bounding_box.position.y = 8
  bounding_box.userData = {
    isBoundingBox: true
  }

  let group = new THREE.Group()
  group.add(object)
  group.add(bounding_box)

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
  let entity_base = new THREE.Group()
  entity_base.name = "entity_base"

  var cylinder_geometry = new THREE.CylinderGeometry( 7.5, 8, 1, 32 );
  var cylinder_material = new THREE.MeshBasicMaterial( {color: 0x50E3C2} );
  var cylinder = new THREE.Mesh( cylinder_geometry, cylinder_material );
  cylinder.name = "entity_base.ring"
  cylinder.position.y = 0.5

  var cylinder_geometry_b = new THREE.CylinderGeometry( 7, 7, 1, 32 );
  var cylinder_material_b = new THREE.MeshBasicMaterial( {color: 0x222222} );
  var cylinder_b = new THREE.Mesh( cylinder_geometry_b, cylinder_material_b );
  cylinder_b.name = "entity_base.center"
  cylinder_b.position.y = 0.55

  entity_base.add(cylinder)
  entity_base.add(cylinder_b)

  group.add(entity_base)

  return group
}

let ObjectList = {}

// Preload all models
MODEL_DATA.forEach((data) => {
  if (!data.type) throw TypeError("MODEL_DATA element must have a type attribute")

  // Load the model
  ObjectList[data.type] = loadModel(data.type)
})

// Preload all entities
ENTITY_DATA.forEach((data) => {
  if (!data.type) throw TypeError("ENTITY_DATA element must have a type attribute")

  // Load the entity
  ObjectList[data.type] = loadEntity(data.type)
})

export {
  ObjectList as ObjectList,
  MODEL_DATA,
  ENTITY_DATA
}