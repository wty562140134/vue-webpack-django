<template>
  <div>
    <img src="../../../assets/logo.png">
    <h1>{{msg}}</h1>
    <el-form label-width="55px" class="demo-ruleForm">
      <el-form-item>
        <el-button type="primary" style="width:10%;" @click="quit">退出</el-button>
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
          使用window.location.href = '/login'就可以正常访问
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

</style>
