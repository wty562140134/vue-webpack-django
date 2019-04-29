<template>
  <div id="app">
    <!--<router-view/>-->
    <!--<div class="container">-->
    <!--<router-view name="left"/>-->
    <!--<router-view name="main"/>-->
    <!--</div>-->

    <el-container>
      <el-header style="padding:0px;">
        <router-view/>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <router-view name="left"/>
        </el-aside>
        <el-main style="padding: 1px;align:right">
          <router-view name="main"/>
        </el-main>
      </el-container>
    </el-container>

  </div>
  <!--<sys-home></sys-home>-->
</template>

<script>
  import sysHome from "./components/systemHome";

  export default {
    name: "App",
    components: {sysHome},
    comments: false,//这个为true是吧代码中注释去除默认为false
    data() {
      return {}
    },
  }
</script>

<style scoped>

  /*.container {*/
  /*width: 100%;*/
  /*display: flex;*/
  /*height: 680px;*/
  /*padding: 0;*/
  /*margin: 0;*/
  /*}*/

</style>
