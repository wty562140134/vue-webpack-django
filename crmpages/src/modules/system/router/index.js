import Vue from 'vue'
import Router from 'vue-router'
import mainBox from '../components/main'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'sys_home',
      component: () => import ('../components/systemHome')
    },
    {
      path: '/system', components: {
        'default': () => import('../components/header'),
        'left': () => import('../components/left'),
        'main': mainBox
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import ('../../../components/public_route')
    },
    {
      path: '/route',
      name: 'route',
      component: () => import ('../../../components/public_route')
    },
  ]
})
