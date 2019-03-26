<template>
  <!--<div class="login">-->
  <!--</div>-->
  <div class="login">
    <p style="font-size: 35px;">登录</p>
    <el-form label-width="55px" class="demo-ruleForm">

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
        this.login_data.password = this.md5(this.login_data.password)
        var login_data = this.qs.stringify(this.login_data)
        //这里/api在proxyTable中被pathRewrite:所定义的空字符串代替,就剩下/index
        // 所以实际被替换为:http://127.0.0.1:8000/index/
        //注意index/参数需要和后台urls中的路由参数一致,不然无法正常发送请求
        this.$ajax.post('/api/admin/login', login_data, {
          // withCredentials: true
        }).then(
          respons => {
            alert(respons.data.result)
            console.log(respons)
            //this.$router.push({name: 'HelloWorld'})//重定向到router路由文件中定义别名为HelloWorld的公用组件
            if (respons.data.result === 'ok') {
              /*
              不同模块之间的跳转需要使用window.location.href = '/system'
              进行跳转不然会出现页面图片无法正常加载的情况,
              编译后需要去修改相应模块的js,修改为访问模块的html如:window.location.href="/system.html"
               */
              window.location.href = '/system'
            } else {
              alert(respons.data.result)
              this.$router.push({name: 'login'})
            }
            // this.$router.push( '/system/index.html#/')
          }).catch(error => {
          console.log(error)
        })
      },
    },
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
