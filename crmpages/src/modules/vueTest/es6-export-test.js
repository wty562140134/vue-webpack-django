//es6向外暴露成员export 和export default
//export default这种方式一个JS文件只能暴露导出一次
export default {
  name: 'zs',
  age: 19
}

//export这种导出可以暴露多个成员导出,但是只能在外部用定义名称在花括号中接收,如果想换名称需要使用as来起别名
export var title = '123'
export var content = '234'

