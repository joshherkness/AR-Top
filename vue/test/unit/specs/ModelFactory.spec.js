import { ModelFactory } from '@/components/editor/ModelFactory'

describe('ModelFactory', () => {
  it('should return null when no data is given', () => {
    let model = ModelFactory.createModel()
    expect(model).toBeNull()
  })
  it('should return null when data is empty', () => {
    let model = ModelFactory.createModel({})
    expect(model).toBeNull()
  })
  it('should return null when data has no type', () => {
    let model = ModelFactory.createModel({
      position: { x: 1, y: 1, z: 1 }
    })
    expect(model).toBeNull()
  })
  it('should return null when data has no position', () => {
    let model = ModelFactory.createModel({
      type: 'voxel'
    })
    expect(model).toBeNull()
  })
  it('should return null when data has invalid type', () => {
    let model = ModelFactory.createModel({
      type: 'invalid',
      position: { x: 1, y: 1, z: 1 }
    })
    expect(model).toBeNull()
  })
  it('should return null for voxel when color is not specified', () => {
    let model = ModelFactory.createModel({
      type: 'voxel',
      position: {
        x: 1,
        y: 1,
        z: 1
      }
    })
    expect(model).toBeNull()
  })
  it('should return an instance of voxel model when type is voxel', () => {
    let model = ModelFactory.createModel({
      type: 'voxel',
      color: '#ffffff',
      position: {
        x: 1,
        y: 1,
        z: 1
      }
    })
    expect(model).toBeDefined()
    expect(model).toHaveProperty('type', 'voxel')
    expect(model).toHaveProperty('color', '#ffffff')
    expect(model).toHaveProperty('position', {
      x: 1,
      y: 1,
      z: 1
    })
  })
})
