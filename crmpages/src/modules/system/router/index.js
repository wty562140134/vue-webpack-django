import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import header from '../components/header'
import leftBox from '../components/left'
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
        'default': header,
        'left': leftBox,
        'main': mainBox
      }
    }
  ]
})
