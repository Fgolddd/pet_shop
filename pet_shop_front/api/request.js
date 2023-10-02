const http = {
	// baseurl地址
	baseUrl: "http://127.0.0.1:8000/",
	// baseUrl: "http://192.168.110.185:8000/",
	// 请求方法
	request(config) {
		// config：请求配置对象，具体的值参照uniapp文档
		// 调用请求拦截器
		config = beforeRequest(config)
		config.url = this.baseUrl + config.url
		// 创建一个Promise对象,在里面发送请求
		return new Promise((resolve, reject) => {
			uni.request(config)
				.then(res => {
					let [error, resp] = res
					// 调用响应拦截器
					const response = beforeResponse(resp)
					resolve(response)
				})
				.catch(err => {
					// 调用异常处理的方法
					errorHandle(err)
					reject(err)
				})
		})
	},
	get(url, data, auth) {
		/*
		url：接口地址
		data: 查询参数
		auth：请求是否需要携带tokne进行认证(true or false)
		*/
		return this.request({
			url: url,
			data: data,
			auth: auth,
			method: "GET"
		})
	},
	post(url, data, auth) {
		/*
		url：接口地址
		data: 请求体参数
		auth：请求是否需要携带tokne进行认证(true or false)
		*/
		return this.request({
			url: url,
			data: data,
			auth: auth,
			method: 'POST'
		})
	},
	delete(url, auth) {
		/*
		url：接口地址
		auth：请求是否需要携带tokne进行认证(true or false)
		*/
		return this.request({
			url: url,
			auth: auth,
			method: 'DELETE'
		})
	},
	put(url, data, auth) {
		/*
		url：接口地址
		data: 请求体参数
		auth：请求是否需要携带tokne进行认证(true or false)
		*/
		return this.request({
			url: url,
			data: data,
			auth: auth,
			method: 'PUT'
		})
	}
}
// 请求拦截器
const beforeRequest = (config) => {
	// 请求之前的做的操作
	console.log('请求拦截器：', config)
	config.header = {}
	// 判断该接口请求是否需要携带token
	if(config.auth){
		if(uni.getStorageSync('token')){
			// 在请求头中添加token
			config.header['Authorization'] = 'Bearer '+ uni.getStorageSync('token')
		}else{
			// 没有登录，无访问权限，重定向到登录页面
			uni.navigateTo({
				url:'/pages/user/login'
			})
		}
	}
	return config
}

//响应拦截器
const beforeResponse = (response) => {
	console.log('响应拦截器：', response)
	// 判断请求返回的响应状态码是否为操作成功的。
	if(response.statusCode!==200 && response.statusCode!==201&& response.statusCode!==204){
		// 给出对应的提示
		if (response.data.error){
			// 显示错误提示内容
			uni.showToast({
				title: response.data.error.toString(),
				duration: 1000,
				icon:"none",
			
			});
		}
	}
	
	return response
}

//异常处理器
const errorHandle = (err) => {
	console.log('网络异常，请求失败!', err)
}


export default http
