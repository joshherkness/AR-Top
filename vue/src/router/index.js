import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Library from '@/components/Library'
import Editor from '@/components/editor/Editor'
import Registration from '@/components/Registration'
import Authentication from '@/components/Authentication'
import store from './../store/store.js'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: true,
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
    // Determine if the user is authenticated
    // TODO: Verify the token here
    let isAuthenticated = !Object.is(store.getters.token, '')
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next() // make sure to always call next()!
  }
})

export default router
