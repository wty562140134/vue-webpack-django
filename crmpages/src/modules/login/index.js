// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'// 导入element-ui
import 'element-ui/lib/theme-chalk/index.css'//导入element-ui css
import "bootstrap"// 导入bootstrap
import "bootstrap/dist/css/bootstrap.css"//导入bootstrap css
import App from './App'
import router from './router'
import Axios from 'axios'// 导入前端请求发送插件
import Qs from 'qs'// 导入表单内容组织成后台能够使用的数据的插件
import '../../plugins/element.js'// 导入element.js插件
import md5 from 'md5'// 导入md5

Axios.defaults.withCredentials = true//这句不写有可能后台拒绝post请求
Vue.prototype.qs = Qs// 设置全局的表单插件
///////////////////////////////////////////////////////////////////////////////////////////////
/*
设置全局的Axios跨域session为true,这个默认为false,不设置为true每次请求都会是一个新的session
*/
Axios.defaults.withCredentials = true
///////////////////////////////////////////////////////////////////////////////////////////////
Vue.prototype.$ajax = Axios// 设置全局的请求发送插件
Vue.prototype.md5 = md5// 设置全局的md5
Vue.config.productionTip = false
Vue.use(ElementUI)// 设置全局使用element-u

Vue.config.debug = true// 开启debug模式
Vue.prototype.debug = true//声明这个用于控制是否是开发环境

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>',
})

/**
 * 模块跳转拦截
 */
router.beforeEach((to, from, next) => {
  if (to.path === '/route') {
    //是否登录验证
    Axios.get('/api/admin/admin').then(respons => {
      //如果验证通过
      if (respons.data.result === 'ok') {
        alert(respons.data.result)
      } else {
        //验证不通过则返回登录模块
        next({name: 'login'})
      }
    })
  }
  next()
});
