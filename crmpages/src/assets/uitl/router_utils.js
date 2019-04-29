/**
 * 前端路由beforeEach拦截器
 * @param router vue路由对象
 * @param Axios 发送请求Axiox对象
 * @param to_url 需要拦截器拦截的前端跳转到路由
 * @param redirect_url 拦截验证失败重定向前端路由
 * @param api_url_obj 拦截器拦截时需要访问后端验证url对象,其中需要三个参数method_type,api_url,params
 * 例如:{method_type:'post', api_url:'/api/admin/login', params:{'name':'zs','age':18}}
 */
export default (router, Axios, to_url, redirect_url, api_url_obj) => {
  //router路由的befoteEcah拦截器
  router.beforeEach((to, from, next) => {
    if (to.path === to_url) {
      verification(Axios, redirect_url, api_url_obj, next)
    }
    next()
  })
}

/**
 * 向后端发送请求的函数
 * @param router前端路由对象
 * @param api_url_obj 拦截器拦截时需要访问后端验证url对象,其中需要三个参数method_type,api_url,params
 * 例如:{method_type:'post', api_url:'/api/admin/login', params:{'name':'zs','age':18}}
 * @param route_params 路由跳转的参数对象
 * 例如跳转至公共路由{name: 'route', params: {to_router: 'system'}或者{url:'/admin'}
 * 其中name为注册路由js index 中的name,params为公共路由组件向其他模块跳转的模块名
 * 如果是本模块跳转route_params.params可以为空
 */
export let send = (Axios, router, api_url_obj, route_params) => {
  send_api(Axios, api_url_obj).then(respons => {
    if (respons.data.result === 'ok') {
      if (!(route_params.params) || Object.keys(route_params.params).length === 0) {
        if (!(router.name) || Object.keys(route_params.name).length === 0) {
          // alert(respons.data.name)
          router.push(route_params.url)
          return respons
        }
        router.push({name: route_params.name})
        return respons
      } else {
        router.push({name: route_params.name, params: route_params.params})
      }
    }
  }).catch(error => {

  })
}


/**
 * 发送请求去后端验证函数
 * @param Axiox 发送请求的Axiox对象
 * @param redirect_url 拦截验证失败重定向前端路由
 * @param api_url_obj 拦截器拦截时需要访问后端验证url对象
 * @param next router路由对象的next()函数
 */
function verification(Axios, redirect_url, api_url_obj, next) {
  send_api(Axios, api_url_obj).then(respons => {
    alert("1" + redirect_url)
    if (respons.data.result === 'ok') {
      alert("2" + respons.data.result)
    } else {
      alert("3" + respons.data.result)
      alert("4" + redirect_url)
      next(redirect_url)
    }
  }).catch(error => {
    alert(error)
    next()
  })
}


/**
 * 发送数据至后端判断请求类型的函数
 * @param Axios 发送请求的Axios对象
 * @param api_url_obj 拦截器拦截时需要访问后端验证url对象
 * @returns get或者post等请求体对象
 */
function send_api(Axios, api_url_obj) {
  let method_type = api_url_obj.method_type.toLocaleLowerCase()
  switch (method_type) {
    case 'post' || '':
      return Axios.post(api_url_obj.api_url, api_url_obj.params)
    case 'get':
      return Axios.get(api_url_obj.api_url, api_url_obj.params)
  }
}

