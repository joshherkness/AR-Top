import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Editor from '@/components/Editor'
import Registration from '@/components/Registration'
import Authentication from '@/components/Authentication'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/editor',
      name: 'Hello',
      component: Editor
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
