import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home/Home'
import Library from '@/components/home/Library'
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
          path: 'editor/:id',
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
          component: Library,
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
