<template>
  <button @click="testRefs" ref="button1">点击一下</button>
  <input ref="input1" text="123"></input>
</template>

<script>
  // 如果需要在App.vue中使用<ref_test/>ref_test,并在components中定义.
  // <router-view/>标签是通过路由匹配渲染则不需要导入组件
  export default {
    name: "ref_test",

    methods: {
      /**
       测试vue操作dom
       */
      testRefs() {
        this.$refs.input1.placeholder = "????"
        this.$refs.button1.innerHTML = "我要改变世界改变自己"
      }
    },

  }
</script>

<style scoped>

</style>
