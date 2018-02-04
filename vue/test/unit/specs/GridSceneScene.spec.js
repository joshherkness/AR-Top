import * as THREE from 'three'

import { GridScene } from '@/components/editor/GridScene'
import { Grid } from '@/components/editor/Grid'

const TEST_GRID = new Grid(1, 1, 1, '#ffffff')

describe('EditorSCene', () => {
  it('should be defined', () => {
    let scale = 50
    let scene = new GridScene(TEST_GRID, scale)
    expect(scene).toBeDefined()
  })
  it('should be type of three.scene', () => {
    let scale = 50
    let scene = new GridScene(TEST_GRID, scale)
    expect(scene).toBeInstanceOf(THREE.Scene)
  })
})