<template>
  <div class="public_route"></div>
</template>

<script>
  /**
   * 这个组件主要是用于做模块间的路由跳转,通过这个公共组件可以在模块间跳转时若时间长可以通过这个组件的动画
   * 过渡.通过这个组件还能解决不同模块间跳转的兼容问题.
   * 图片加载是在模块组件中通过js加载,模块之间路由跳转使用this.$router.push('/login').
   * 使用这种方式进行路由跳转若图片不是通过js在组件中加载会出现图片无法正常加载的问题,
   * 使用window.location.href = '/login'就可以正常访问,
   * 编译后需要去修改相应模块的js,例如:window.location.href="/system.html"
   */
  export default {
    name: "public_route",

    data() {
      return {
        to_route: this.$route.params['to_router']
      }
    },

    /**
     * 在组件创建完毕后直接跳转到指定模块
     */
    created() {
      //判断是否是开发环境
      if (this.debug) {
        window.location.href = '/' + this.to_route
      } else {
        window.location.href = '/' + this.to_route + '.html'
      }
    }

  }
</script>

<style scoped>

</style>
