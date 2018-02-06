import { SECRET } from './secrets'
import axios from 'axios'
import store from '@/store/store';
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

const API_ROOT = 'http://localhost:5000/api'
const ENDPOINTS = {
  authenticate: `${ API_ROOT }/auth`,
  register: `${ API_ROOT }/register`,
  map: `${ API_ROOT }/map`,
  maps: `${ API_ROOT }/maps`
}

export class API {
  static async authenticate({email, password}) {
    try {
      let response = await axios.post(ENDPOINTS.authenticate, {}, generateConfig({
        email: email,
        password: password
      }))
      return response.data
    } catch (err) {
      throw err
    }
  }

  static async register({email, password}) {
    try {
      let response = await axios.post(ENDPOINTS.register, {}, generateConfig({
        email: email,
        password: password
      }))
      // Why doesn't this endpoint return the email also?
      return response.data.auth_token
    } catch (err) {
      throw err
    }
  }

  static async getMaps () {
    try {
      let auth_token = store.state.user.token 
      let url = `${ ENDPOINTS.maps }/${ auth_token }`
      let response = await axios.get(url, generateConfig({
        auth_token: auth_token
      }))
      return response.data
    } catch (err) {
      throw err
    }
  }

  static async getMap (id) {
    try {
      let url = `${ ENDPOINTS.map }/${ id }`
      let response = await axios.get(url, generateConfig({
        email: store.state.user.email
      }))
      return response.data
    } catch (err) {
      let auth_token 
    }
  }

  static async deleteMap (id) {
    try {
      let url = `${ ENDPOINTS.map }/${ id }`
      let response = await axios.delete(url, generateConfig({
        email: store.state.user.email
      }))
      return response.data.success
    } catch (err) {
      throw err
    }
  }

  static async updateMap (id, data) {
    try {
      let url = `${ ENDPOINTS.map }/${ id }`
      let response = await axios.post(url, data, generateConfig({
        email: store.state.user.email
      }))
      return response.data.map
    } catch (err) {
      throw err
    }
  }
}