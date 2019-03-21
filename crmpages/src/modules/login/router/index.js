import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
// import login from '../../../components/login'
// import admin from '../components/admin'
import login from '../components/login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
    // {
    //   path: '/',
    //   name: 'login',
    //   component: login,
    // },
    // {
    //   path: '/admin',
    //   name: 'admin',
    //   component: admin,
    // },
  ]
})
