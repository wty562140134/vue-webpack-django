<template>
  <div id="app">
    <!--<router-view/>-->
    <sys-home></sys-home>
  </div>
</template>

<script>
  import sysHome from "./components/systemHome";

  export default {
    name: "App",
    components: {sysHome},
    comments: false,
    data() {
      return {}
    },
  }
</script>

<style scoped>

</style>
