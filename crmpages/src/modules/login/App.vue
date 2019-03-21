<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  import admin from "./components/admin"
  import login from "./components/login"

  export default {
    name: 'App',
    components: {admin, login},
    data() {
      return {
        msg: '初始页面msg'
      }
    },
    methods: {
      send: function () {
        //这里/api在proxyTable中被pathRewrite:所定义的空字符串代替,就剩下/index
        // 所以实际被替换为:http://127.0.0.1:8000/index/
        //注意index/参数需要和后台urls中的路由参数一致,不然无法正常发送请求
        this.$ajax.post('/api/index/').then(result => { // 请求成功后的回调函数
          console.log(result.data.msg)
          this.msg = result.data.msg
        }).catch(error => { //请求失败后的回调函数
          console.log(error)
        })
      }
    }
  }
</script>

<style>

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

</style>
