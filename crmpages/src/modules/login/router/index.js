import Vue from 'vue'
import Router from 'vue-router'
import login from '../components/login'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/hello',
    //   name: 'HelloWorld',
    //   component: HelloWorld
    // },
    {
      path: '/',
      redirect: '/login'
    }, {
      path: '/login',
      name: 'login',
      component: login
    }, {
      path: '/admin',
      name: 'admin',
      component: () => import('../components/admin'),
    }, {
      path: '/route',
      name: 'route',
      component: () => import('../../../components/public_route')
    },
  ]
})
