import { GridModel, VoxelGridModel, GridModelType } from '@/components/editor/GridModels'

const TEST_POSITION = { x: 1, y: 2, z: 3 }
const TEST_COLOR = '#ffffff'

describe('GridModel', () => {
  it('should not be instantiated', () => {
    expect(() => {
      let model = new GridModel()
    }).toThrow()
  })
})

describe('VoxelGridModel', () => {
  it('should throw an error when no position value is passed', () => {
    expect(() => {
      let voxel = new VoxelGridModel()
    }).toThrow()
  })
  it('should throw an error when no color value is passed', () => {
    expect(() => {
      let voxel = new VoxelGridModel(TEST_POSITION)
    }).toThrow()
  })
  it('should be defined', () => {
    let voxel = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
    expect(voxel).toBeDefined()
  })
  it('should have voxel type', () => {
    let voxel = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
    expect(voxel).toHaveProperty('type', GridModelType.VOXEL)
  })

  describe('create object', () => {
    it('should create an object that is defined', () => {
      let voxel = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
      let object = voxel.createObject()
      expect(object).toBeDefined()
    })
    it('should create an scaled object that is defined', () => {
      let scale = 50
      let voxel = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
      let object = voxel.createObject(scale)
      expect(object).toBeDefined()
    })
  })

  describe('equals', () => {
    it('should throw error when no model is passed', () => {
      let a = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
      expect(() => {
        let eq = a.equals()
      }).toThrow()
    })
    it('should return true when voxel (a) is equal to another voxel (b)', () => {
      let a = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
      let b = new VoxelGridModel(TEST_POSITION, TEST_COLOR)
      expect(a.equals(b)).toBeTruthy()
      expect(b.equals(a)).toBeTruthy()
    })
  })
})