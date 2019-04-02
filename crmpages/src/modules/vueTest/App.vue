<template>
  <div id="app">
    <ref_test/>
    <router-view/>
  </div>
</template>

<script>
  import ref_test from "./components/reftest";

  export default {
    name: "App",
    components: {ref_test}
  }
</script>

<style scoped>

</style>
