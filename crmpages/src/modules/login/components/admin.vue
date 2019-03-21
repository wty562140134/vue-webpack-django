<template>
  <div class="admin">
    <p>{{ msg }}</p>
    <input type="button" value="发送测试" @click="send"></input>
  </div>
</template>

<script>
  export default {
    name: "admin",
    data() {
      return {
        msg: '初始页面admin msg!!!!!!!!!!!!!!!!'
      }
    },
    methods: {
      send() {
        this.$ajax.post('/api/admin/test').then(result => {
          console.log(result.data.result)
          this.msg = result.data.result
          // this.$router.push({name: 'HelloWorld'})// 测试重定向
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>

<style scoped>

</style>
