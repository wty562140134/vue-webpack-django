<template>
  <!--<div class="login">-->
  <!--</div>-->
  <div class="login">
    <p style="font-size: 35px;">登录</p>
    <el-form label-width="50px" class="demo-ruleForm">

      <el-form-item label="用户名">
        <el-input autocomplete="on" v-model="login_data.user_name"></el-input>
      </el-form-item>

      <el-form-item label="密码">
        <el-input type="password" v-model="login_data.password" autocomplete="on"></el-input>
      </el-form-item>

      <div class="box clearfix">
        <span class="lf"
              style="cursor: pointer;color: #f19149;font-size: 0.75rem;margin-left: 5px;">忘记密码？</span>
        <div class="rt">
          <el-checkbox style="color:#a0a0a0;">一周内自动登录</el-checkbox>
        </div>
      </div>

      <el-form-item>
        <el-button type="primary" style="width:100%;" @click="login">登录</el-button>
        <!--  <el-button @click="resetForm('ruleForm')">重置</el-button> -->
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        login_data: {
          user_name: '',
          password: '',
        },
      }
    },
    methods: {
      login() {
        console.log(this.login_data)
        this.login_data.password = this.md5(this.login_data.password)
        var login_data = this.qs.stringify(this.login_data)
        this.$ajax.post('/api/admin/login', login_data).then(
          respons => {
            alert(respons.data.result)
            this.$router.push({name: 'HelloWorld'})//重定向到router路由文件中定义别名为HelloWorld的公用组件
          }).catch(error => {
          console.log(error)
        })
      },
    }
  }
</script>

<style scoped>

  .lf {
    float: left;
  }

  .box {
    min-width: 350px;
    margin-left: 50px;
    width: 30%;
  }

  .rf {
    float: right;
  }

  .clearfix:after {
    content: ".";
    display: block;
    height: 0;
    visibility: hidden;
    clear: both;
  }

  .clearfix {
    *zoom: 1;
  }

  .login {
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
