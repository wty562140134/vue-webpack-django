// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'// 导入element-ui
import 'element-ui/lib/theme-chalk/index.css'//导入element-ui css
import App from './App'
import router from './router'
import Axios from 'axios'// 导入前端请求发送插件
import Qs from 'qs'// 导入表单内容组织成后台能够使用的数据的插件
import './plugins/element.js'// 导入element.js插件

Axios.defaults.withCredentials = true//这句不写有可能后台拒绝post请求
Vue.prototype.qs = Qs// 设置全局的表单插件
Vue.prototype.$ajax = Axios// 设置全局的请求发送插件
Vue.config.productionTip = false
Vue.use(ElementUI)// 设置全局使用element-ui

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})

module.exports = Vue
