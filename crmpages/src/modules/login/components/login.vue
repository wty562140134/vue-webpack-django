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
            //this.$router.push({name: 'HelloWorld'})//重定向到router路由文件中定义别名为HelloWorld的公用组件
            if (respons.data.result === 'ok') {
              /*
              图片加载是在模块组件中通过js加载,模块之间路由跳转使用this.$router.push('/login').
              使用这种方式进行路由跳转若图片不是通过js在组件中加载会出现图片无法正常加载的问题,
              使用window.location.href = '/login'就可以正常访问,
              编译后需要去修改相应模块的js,例如:window.location.href="/system.html"
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

    /**
     * 把静态资源加载放在相应的组件中并通过js进行加载可以很好的解决模块跳转导致图片无法加载的问题
     */
    beforeCreate() {
      /*
      虽然vue不提倡操纵dom元素,
      但是由于body是在页面还未渲染之前就有的,
      此时vue内的el对象还没生产,所以无法通过el来操作dom,
      所以只能通过这种方式来给body设置图片
       */
      document.querySelector('body').setAttribute('style', 'background-image:url(/static/2b.jpg);background-repeat:no-repeat;width;100%;height: 100%;')
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
