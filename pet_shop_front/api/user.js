// 用户模块接口封装
import http from './request.js'

export default {
	// 登录接口
	login(params) {
		return http.post('api/users/login/', params)
	},
	// 获取用户信息
	getUserInfo(id) {
		return http.get(`api/users/${id}/`, {}, true)
	},
	// 注册接口
	register(params) {
		return http.post('api/users/register/', params)
	},
	// 刷新tokne

	// 校验token

	// 修改用户名
	// updateName(id, params) {
	// 	return http.put(`/api/users/${id}/name/`, params, true)
	// },
	// // 修改邮箱
	// updateEmail(id, params) {
	// 	return http.put(`/api/users/${id}/email/`, params, true)
	// },
	// // 发送验证码的接口
	// sendsms(params) {
	// 	return http.post('/api/users/sendsms/', params)
	// },
	// // 修改密码的接口
	// updatePwd(id, params) {
	// 	return http.put(`/api/users/${id}/password/`, params, true)
	// },
	// // 绑定手机号
	// bindMobile(id, params) {
	// 	return http.put(`/api/users/${id}/mobile/bind`, params, true)
	// },

	// // 解绑手机号
	// unBindMobile(id, params) {
	// 	return http.put(`/api/users/${id}/mobile/unbind`, params, true)
	// },
	//获取用户收货地址列表
	getAddress() {
		return http.get('api/users/address/', {}, true)
	},
	// 获取省市县区域的数据
	// getArea(level) {
	// 	return http.get(`/api/users/area/?level=${level}`)
	// },
	// 修改用户收货地址
	updateAddress(id, params) {
		return http.put(`api/users/address/${id}/`, params, true)
	},
	// 添加收货地址
	createAddress(params) {
		return http.post(`api/users/address/`, params, true)
	},
	// 删除收货地址
	deleteAddress(id) {
		return http.delete(`api/users/address/${id}/`, {}, true)
	},
	// 设置默认收货地址
	setDefaultAddr(id) {
		return http.put(`api/users/address/${id}/default`, {}, true)
	}
}
