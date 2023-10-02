// 订单模块接口封装
import http from './request.js'
export default{
	// 获取用户的订单数据
	getOrderList(){
		return http.get('api/orders/order/',{},true)
	},
	// 取消订单
	colseOrder(id){
		return http.put(`api/orders/order/${id}/`,{},true)
	},
	// 创建订单
	createOrder(params){
		return http.post('api/orders/submit/',params,true)
	},
	payOrder(id){
		return http.put(`api/orders/order/pay/${id}/`,{},true)
	},
	confirmOrder(id){
		return http.put(`api/orders/order/confirm/${id}/`,{},true)
	},
	// 获取单个订单数据
	getOrderInfo(id){
		return http.get(`api/orders/order/${id}/`,{},true)
	},
	// 获取支付宝支付的url地址
	getAlipayUrl(params){
		return http.post('api/orders/payment/',params,true)
	}
	
}