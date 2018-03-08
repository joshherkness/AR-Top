import { SECRET } from './secrets'
import axios from 'axios'
import store from '@/store/store'
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
  authenticate: `${API_ROOT}/auth`,
  register: `${API_ROOT}/register`,
  map: `${API_ROOT}/map`,
  maps: `${API_ROOT}/maps`,
  session: `${API_ROOT}/sessions`,
  authenticated: `${API_ROOT}/authenticated`
}

export class API {
  // eslint-disable-next-line
  static async authenticate({ email, password }) {
    try {
      let response = await axios.post(
        ENDPOINTS.authenticate,
        {},
        generateConfig({
          email: email,
          password: password
        })
      )
      return response.data
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async register({ email, password }) {
    try {
      let response = await axios.post(
        ENDPOINTS.register,
        {},
        generateConfig({
          email: email,
          password: password
        })
      )
      // Why doesn't this endpoint return the email also?
      return response.data.auth_token
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async getCurrentUser() {
    try {
      let authToken = store.state.user.token
      let response = await axios.get(
        ENDPOINTS.authenticated,
        generateConfig({
          auth_token: authToken
        })
      )
      return response.data.user
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async getMaps() {
    try {
      let authToken = store.state.user.token
      let url = `${ENDPOINTS.maps}/${authToken}`
      let response = await axios.get(
        url,
        generateConfig({
          auth_token: authToken
        })
      )
      return response.data
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async getMap(id) {
    try {
      let url = `${ENDPOINTS.map}/${id}`
      let response = await axios.get(
        url,
        generateConfig({
          email: store.state.user.email
        })
      )
      return response.data
    } catch (err) {
      // eslint-disable-next-line
      let authToken
    }
  }

  // eslint-disable-next-line
  static async deleteMap(id) {
    try {
      let url = `${ENDPOINTS.map}/${id}`
      let response = await axios.delete(
        url,
        generateConfig({
          email: store.state.user.email
        })
      )
      return response.data.success
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async updateMap(id, data) {
    try {
      let url = `${ENDPOINTS.map}/${id}`
      let response = await axios.post(
        url,
        data,
        generateConfig({
          email: store.state.user.email
        })
      )
      return response.data.map
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async getSession(id) {
    try {
      let url = `${ENDPOINTS.session}/${id}`
      let response = await axios.get(
        url,
        generateConfig({
          auth_token: store.state.user.token
        })
      )
      return response.data
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async getCurrentSession() {
    if (!store.state.user.token || store.state.user.token === '') {
      return null
    }

    try {
      let response = await axios.get(
        ENDPOINTS.session,
        generateConfig({
          auth_token: store.state.user.token
        })
      )
      return response.data.session
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async deleteSession(id) {
    try {
      let url = `${ENDPOINTS.session}/${id}`
      let response = await axios.delete(
        url,
        generateConfig({
          auth_token: store.state.user.token
        })
      )
      return response.data
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async createSession(map_id) {
    try {
      let url = `${ENDPOINTS.session}`
      let data = { map_id: map_id }
      let response = await axios.post(
        url,
        data,
        generateConfig({
          auth_token: store.state.user.token
        })
      )
      return response.data.session
    } catch (err) {
      throw err
    }
  }

  // eslint-disable-next-line
  static async updateSession(id, { map_id }) {
    try {
      let url = `${ENDPOINTS.session}/${id}`
      let data = { map_id: map_id }
      let response = await axios.post(
        url,
        data,
        generateConfig({
          auth_token: store.state.user.token
        })
      )
      return response.data.session
    } catch (err) {
      throw err
    }
  }
}
