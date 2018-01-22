import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home/Home'
import Maps from '@/components/home/Maps'
import Editor from '@/components/editor/Editor'
import Registration from '@/components/user/Registration'
import Authentication from '@/components/user/Authentication'
import store from './../store/store.js'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      children: [
        {
          path: 'editor',
          name: 'Editor',
          component: Editor,
          meta: { requiresAuth: true },
          beforeEnter: (to, from, next) => {
            if (Object.is(store.getters.token, '')) {
              next('/auth')
            } else {
              next()
            }
          }
        },
        {
          path: 'maps',
          name: 'Maps',
          component: Maps,
          beforeEnter: (to, from, next) => {
            if (Object.is(store.getters.token, '')) {
              next('/auth')
            } else {
              next()
            }
          }
        }
      ]
    },
    {
      path: '/register',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/auth',
      name: 'Authentication',
      component: Authentication
    }
  ]
})
