import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Editor from '@/components/Editor'
import Registration from '@/components/Registration'
import Authentication from '@/components/Authentication'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
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
