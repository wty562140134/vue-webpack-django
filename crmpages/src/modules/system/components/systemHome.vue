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
          /*
              不同模块之间的跳转需要使用window.location.href = '/login'
              进行跳转不然会出现页面图片无法正常加载的情况,
              编译后需要去修改相应模块的js,修改为访问模块的html如:window.location.href="/login.html"
               */
          window.location.href = '/login'
        })
      }
    },

    //这是一个简单的登录验证测试,正式的登录验证需要放到拦截器中
    beforeCreate() {
      this.$ajax.get('/api/admin/admin').then(respons => {
        if (respons.data.result != 'ok') {
          /*
          模块之间使用this.$router.push('/login')方式进行跳转会出现图片无法正常加载的问题,
          使用window.location.href = '/login'就可以正常访问,
          编译后需要去修改相应模块的js,例如:window.location.href="/login.html"
           */
          window.location.href = '/login'
          alert(respons.data.result)
        } else {
          this.$router.push('/')
        }
      })
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
