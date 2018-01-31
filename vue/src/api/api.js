import { SECRET } from './secrets'
var r = require('jsrsasign')

/**
 * This function returns an object that serves as a
 * configuration for a axios request, which includes
 * a JSON Web Token.
 *
 * @param {Object} data
 *
 * @returns {Object}
 *
 */
export const generateConfig = data => {
  try {
    const JWT_HEADER = { alg: 'HS512', typ: 'JWT' }
    const JWT_PAYLOAD = {}
    JWT_PAYLOAD.iat = r.jws.IntDate.get('now')
    JWT_PAYLOAD.exp = r.jws.IntDate.get('now + 1day')
    JWT_PAYLOAD.data = data
    const header = JSON.stringify(JWT_HEADER)
    const payload = JSON.stringify(JWT_PAYLOAD)
    const jwt = r.jws.JWS.sign('HS512', header, payload, {
      b64: SECRET
    })

    const config = {
      headers: {
        Authorization: 'Bearer ' + jwt
      }
    }
    return config
  } catch (err) {
    console.error(err)
  }
}
