<template>
  <div class="syshome">
    <img src="../../../assets/logo.png">
    <h1>{{msg}}</h1>
    <el-form label-width="55px" class="demo-ruleForm">
      <el-form-item>
        <el-button type="primary" style="width:100%" @click="quit">退出</el-button>
        <!--  <el-button @click="resetForm('ruleForm')">重置</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "system-home",

    data() {
      return {
        msg: '这是登录成功后跳转的后台模块',
        exit: '退出'
      }
    },

    methods: {
      quit() {
        this.$ajax.get('/api/admin/exit').then(respons => {
          // window.location.href = '/login'
          this.$router.push({name: 'route', params: {to_router: 'login'}})
        })
      }
    },

    /**
     * 是否是登录状态拦截
     */
    beforeRouteEnter(to, from, next) {
      if (to.path === '/') {
        //登录验证
        next(vm => {
          // 通过 `vm` 访问组件实例
          vm.$ajax.get('/api/admin/admin').then(respons => {
            //如果验证通过
            if (respons.data.result === 'ok') {
              // window.location.href = '/login'
              //通过公共路由路由到指定模块
              // router.push({name: 'route', params: {to_router: 'system'}})
            } else {
              //验证不通过则返回登录模块
              alert(respons.data.result)
              next({name: 'route', params: {to_router: 'login'}})
            }
          })
        })
      }
      next()
    },

  }
</script>

<style scoped>

  .syshome {
    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

</style>
