import * as THREE from 'three'
import { Grid } from '@/components/editor/Grid'
import { VoxelGridModel } from '../../../src/components/editor/GridModels';

const TEST_COMPLEX_GRID_DATA = {
  width: 1,
  height: 2,
  depth: 3,
  color: '#ffffff',
  id: '0',
  name: 'Exandria',
  models: [
    {
      type: 'voxel',
      position: {
        x: 0,
        y: 0,
        z: 0
      },
      color: '#434323'
    },
    {
      type: 'voxel',
      position: {
        x: 0,
        y: 0,
        z: 1
      },
      color: '#434323'
    }
  ]
}

describe('Grid', () => {
  it('should throw error when no height value is passed', () => {
    expect(() => { let grid = new Grid() }).toThrow()
  })
  it('should throw error when no width value is passed', () => {
    expect(() => { let grid = new Grid(1) }).toThrow()
  })
  it('should throw error when no depth value is passed', () => {
    expect(() => { let grid = new Grid(1, 2) }).toThrow()
  })
  it('should throw error when no color value is passed', () => {
    expect(() => { let grid = new Grid(1, 2, 3) }).toThrow()
  })
  it('should construct a basic grid', () => {
    let grid = new Grid(1, 2, 3, '#ffffff')
    expect(grid).toBeDefined()
    expect(grid).toBeInstanceOf(Grid)
    expect(grid).toHaveProperty('width', 1)
    expect(grid).toHaveProperty('height', 2)
    expect(grid).toHaveProperty('depth', 3)
    expect(grid).toHaveProperty('color', '#ffffff')
  })
  it('should retrieve id from optional constructor parameter', () => {
    let grid = new Grid(1, 2, 3, '#ffffff', {
      id: '0'
    })
    expect(grid).toBeDefined()
    expect(grid).toHaveProperty('id', '0')
  })
  it('should retrieve name from optional constructor parameter', () => {
    let grid = new Grid(1, 2, 3, '#ffffff', {
      name: 'Exandria'
    })
    expect(grid).toBeDefined()
    expect(grid).toHaveProperty('name', 'Exandria')
  })
  it('should retrieve models from optional constructor parameter', () => {
    let grid = new Grid(1, 2, 3, '#ffffff', {
      models: [
        {
          type: 'voxel',
          position: {
            x: 0,
            y: 0,
            z: 0
          },
          color: '#434323'
        }
      ]
    })
    expect(grid).toBeDefined()
    expect(grid).toHaveProperty('models')
    expect(grid.models).toHaveLength(1)
  })
  it('should throw error when models is not an array type', () => {
    expect(() => { 
      let grid = new Grid(1, 2, 3, '#ffffff', {
        models: 'not an array'
      })
    }).toThrow()
  })

  describe('is within bounds', () => {
    it('should return true for position within bounds', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = new THREE.Vector3(0, 0, 0)
      expect(grid.isWithinBounds(position)).toBeTruthy()
    })
    it('should return false for position outside bounds', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = new THREE.Vector3(1, 1, 1)
      expect(grid.isWithinBounds(position)).toBeFalsy()
    })
  })

  describe('at', () => {
    it('should return undefined when no model matches the position', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = new THREE.Vector3(0, 0, 0)
      let model = grid.at(position)
      expect(model).toBeUndefined()
    })
    it('should return model at position', () => {
      let grid = new Grid(1, 1, 1, '#ffffff', {
        models: [
          {
            type: 'voxel',
            position: {
              x: 0,
              y: 0,
              z: 0
            },
            color: '#434323'
          }
        ]
      })
      let position = new THREE.Vector3(0, 0, 0)
      let model = grid.at(position)
      expect(model).toBeDefined()
      expect(model).toHaveProperty('position', {x: 0, y: 0, z: 0})
    })
  })

  describe('add', () => {
    it('should return true and add model when position is within bounds and unoccupied', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 0, y: 0, z: 0 }
      let a = new VoxelGridModel(position, '#ffffff')
      expect(grid.add(a)).toBeTruthy()
    })
    it('should return false when model position is outside bounds', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 1, y: 1, z: 1 }
      let a = new VoxelGridModel(position, '#ffffff')
      expect(grid.add(a)).toBeFalsy()
    })
    it('should return false when model position is occupied', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 0, y: 0, z: 0 }
      let a = new VoxelGridModel(position, '#ffffff')
      expect(grid.add(a)).toBeTruthy()
      let b = new VoxelGridModel(position, '#ffffff')
      expect(grid.add(b)).toBeFalsy()
    })
  })

  describe('remove', () => {
    it('should remove and return existing model', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 0, y: 0, z: 0 }
      let existant = new VoxelGridModel(position, '#ffffff')
      grid.add(existant)
      expect(grid.remove(existant)).toBeDefined()
    })
    it('should return undefined for nonexistant model', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 0, y: 0, z: 0 }
      let nonexistant = new VoxelGridModel(position, '#ffffff')
      expect(grid.remove(nonexistant)).toBeUndefined()
    })
  })

  describe('remove at', () => {
    it('should remove and return first matching model when matching model exists', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 0, y: 0, z: 0 }
      let existant = new VoxelGridModel(position, '#ffffff')
      grid.add(existant)
      expect(grid.removeAt(existant.position)).toBeDefined()
    })
    it('should return undefined when no matching models exist', () => {
      let grid = new Grid(1, 1, 1, '#ffffff')
      let position = { x: 0, y: 0, z: 0 }
      let nonexistant = new VoxelGridModel(position, '#ffffff')
      expect(grid.remove(nonexistant.position)).toBeUndefined()
    })
  })

  describe('deserialize', () => {
    it('should deserialize a basic grid', () => {
      let grid = Grid.deserialize({
        width: 1,
        height: 2,
        depth: 3,
        color: '#444444'
      })
      expect(grid).toBeDefined()
      expect(grid).toBeInstanceOf(Grid)
    })
    it('should deserialize a complex grid', () => {
      let grid = Grid.deserialize(TEST_COMPLEX_GRID_DATA)
      expect(grid).toBeDefined()
      expect(grid).toBeInstanceOf(Grid)
      expect(grid).toHaveProperty('width', 1)
      expect(grid).toHaveProperty('height', 2)
      expect(grid).toHaveProperty('depth', 3)
      expect(grid).toHaveProperty('color', '#ffffff')
      expect(grid).toHaveProperty('id', '0')
      expect(grid).toHaveProperty('name', 'Exandria')
      expect(grid).toHaveProperty('models')
      expect(grid.models).toHaveLength(2)
    })
  })

  describe('serialize', () => {
    it('should serialize a basic grid using 2 spaces', () => {
      let spaces = 2
      let grid = new Grid(1, 2, 3, '#ffffff')
      expect(grid.serialize()).toEqual(JSON.stringify({
        width: 1,
        height: 2,
        depth: 3,
        color: '#ffffff',
        models: []
      }, null, spaces))
    })
    it('should serialize a complex grid using 2 spaces', () => {
      let spaces = 2
      // We assume deserialize will work here
      let grid = Grid.deserialize(TEST_COMPLEX_GRID_DATA)
      let serialized = grid.serialize()
      expect(serialized).toBeDefined()
      expect(JSON.parse(serialized)).toEqual(TEST_COMPLEX_GRID_DATA)
    })
  })
})