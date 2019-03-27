<template>
  <div id="app">
    <!--<button @click="testRefs" ref="button1">点击一下</button>-->
    <!--<input ref="input1" text="123"></input>-->
    <router-view/>
  </div>
</template>

<script>
  import login from "./components/login"

  export default {
    name: 'app',
    components: {login},
    data() {
      return {
        msg: '初始页面msg',
      }
    },
    methods: {
      /*
      测试vue操作dom
      */
      testRefs() {
        this.$refs.input1.placeholder = "????"
        this.$refs.button1.innerHTML = "我要改变世界改变自己"
      }
    },

    beforeCreate() {
      /*
      虽然vue不提倡操纵dom元素,
      但是由于body是在页面还未渲染之前就有的,
      此时vue内的el对象还没生产,所以无法通过el来操作dom,
      所以只能通过这种方式来给body设置图片
       */
      document.querySelector('body').setAttribute('style', 'background-image:url(/static/2b.jpg);background-repeat:no-repeat;width;100%;height: 100%;')
    },

    mounted() {
      console.log(this)
      this.$refs.input1.placeholder = "????"
      this.$refs.button1.innerHTML = "我要改变世界改变自己"
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
