<template>
  <div id="app">
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
    methods: {},
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
