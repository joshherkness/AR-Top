import * as THREE from 'three'

import { GridDirector } from '@/components/editor/GridDirector'
import { Grid } from '@/components/editor/Grid'
import { VoxelGridModel } from '@/components/editor/GridModels'

const TEST_BASIC_GRID_DATA = {
  width: 16,
  height: 3,
  depth: 16,
  color: '#ffffff'
}

describe('GridDirector', () => {
  it('should be defined', () => {
    let director = new GridDirector()
    expect(director).toBeDefined()
  })

  it('should be able to load a grid', () => {
    let director = new GridDirector()
    let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
    director.load(grid)
    expect(director.scene).toBeDefined()
    expect(director.grid).toEqual(grid)
  })

  it('should be able to add a model', () => {
    let director = new GridDirector()
    let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
    director.load(grid)
    let model = new VoxelGridModel({x: 0, y: 0, z: 0}, '#ffffff')
    director.add(model)
    expect(director.objectMap.size).toEqual(1)
  })

  it('should be able to remove a model', () => {
    let director = new GridDirector()
    let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
    director.load(grid)
    let model = new VoxelGridModel({x: 0, y: 0, z: 0}, '#ffffff')
    director.add(model)
    director.remove(model)
    expect(director.objectMap.size).toEqual(0)
  })

  it('should be able to convert actual position to unit position', () => {
    let director = new GridDirector({scale: 50})
    let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
    director.load(grid)
    let actualPosition = new THREE.Vector3(-375, 25, -375)
    let unitPosition = new THREE.Vector3(0, 0, 0)
    expect(director.convertActualToUnitPosition(actualPosition)).toEqual(unitPosition)
  })

  it('should be able to convert unit position to actual position', () => {
    let director = new GridDirector({scale: 50})
    let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
    director.load(grid)
    let unitPosition = new THREE.Vector3(0, 0, 0)
    let actualPosition = new THREE.Vector3(-375, 25, -375)
    expect(director.convertUnitToActualPosition(unitPosition)).toEqual(actualPosition)
  })

  describe('selection', () => {
    it('should init selection', () => {
      let director = new GridDirector()
      let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
      director.load(grid)
      expect(director.scene).toBeDefined()
      director.initSelection()
      expect(director.scene.getObjectByName('selection')).toBeDefined()
      expect(director.scene.getObjectByName('model-selection')).toBeDefined()
    })
    it('should clear selection', () => {
      let director = new GridDirector()
      let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
      director.load(grid)
      director.initSelection()
      director.scene.getObjectByName('selection').add(new THREE.Object3D())
      director.scene.getObjectByName('model-selection').add(new THREE.Object3D())
      expect(director.scene.getObjectByName('selection').children).toHaveLength(1)
      expect(director.scene.getObjectByName('model-selection').children).toHaveLength(1)
      director.clearSelection()
      expect(director.scene.getObjectByName('selection').children).toHaveLength(0)
      expect(director.scene.getObjectByName('model-selection').children).toHaveLength(0)
    })
    it('should set selection on unoccupied position', () => {
      let director = new GridDirector()
      let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
      director.load(grid)
      let model = new VoxelGridModel( '#ffffff', { x: 0, y: 0, z: 0 })
      director.setSelection(model.position, {model: model})
      expect(director.scene.getObjectByName('selection').children).toHaveLength(1)
    })
    it('should set model selection on occupied position', () => {
      let director = new GridDirector()
      let grid = Grid.deserialize(TEST_BASIC_GRID_DATA)
      director.load(grid)
      let model = new VoxelGridModel( '#ffffff', { x: 0, y: 0, z: 0 })
      director.add(model)
      director.setSelection(model.position)
      expect(director.scene.getObjectByName('model-selection').children).toHaveLength(1)
      expect(director.objectMap.get(model).material.opacity).toBe(0.5)
    })
  })
})