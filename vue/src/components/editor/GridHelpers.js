import * as THREE from 'three'

export class GridHelpers {
  static darken (hex, value) {
    value = value || 0.8
    let color = new THREE.Color(hex)
    return color.multiplyScalar(value)
  }
}
