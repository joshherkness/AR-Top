import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Library from '@/components/Library'
import Editor from '@/components/editor/Editor'
import Registration from '@/components/Registration'
import Authentication from '@/components/Authentication'
import { API } from '@/api/api'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: false,
        requiresNavbar: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Authentication,
      meta: {
        requiresAuth: false,
        requiresNavbar: false
      }
    },
    {
      path: '/register',
      name: 'register',
      component: Registration,
      meta: {
        requiresAuth: false,
        requiresNavbar: false
      }
    },
    {
      path: '/library',
      name: 'library',
      component: Library,
      meta: {
        requiresAuth: true,
        requiresNavbar: true
      }
    },
    {
      path: '/editor/:id',
      name: 'editor',
      component: Editor,
      meta: {
        requiresAuth: true,
        requiresNavbar: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Fetch the current user using auth token
    API.getCurrentUser().then((user) => {
      // We successfully retrieved the current user, therefore we can route the
      // user
      next()
    }).catch((err) => {
      // Route the user to login page if error status is 401 (unauthorized)
      if (err.response.status === 401) {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
      } else {
        throw err
      }
    })
  } else {
    next() // make sure to always call next()!
  }
})

export default router
