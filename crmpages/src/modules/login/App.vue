<template>
  <div id="app">
    <!--<button @click="testRefs" ref="button1">点击一下</button>-->
    <!--<input ref="input1" text="123"></input>-->
    <router-view/>
  </div>
</template>

<script>
  // import login from "./components/login"

  export default {
    name: 'app',
    // components: {login},
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

    // mounted() {
    //   console.log(this)
    //   this.$refs.input1.placeholder = "????"
    //   this.$refs.button1.innerHTML = "我要改变世界改变自己"
    // }

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
