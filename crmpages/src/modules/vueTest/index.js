// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// import Vue from 'vue'
// import Vue from 'vue/dist/vue.esm.js'
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

/*
var ren = {
  template: '<h1>测试render渲染组件</h1>'
}*/

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>',
  /*
  render: (createElement) => {
    return createElement(ren)
  }*/
})

import ml, {title, content as content1} from './es6-export-test'

console.log(ml)
console.log(title + '----' + content1)

class TestClass {
  static info = {name: 'lw', age: 30}
}

console.log(TestClass.info)
