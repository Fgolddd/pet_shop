// 购物车模块接口封装
import http from './request.js'

export default {

	// 添加商品到购物车
	addGoods(params) {
		return http.post('api/cart/products/', params, true)
	},
	// 获取购物车中的商品列表
	getCartGoods(params) {
		return http.get('api/cart/products/', params, true)
	},
	// 修改购物车中商品的状态
	checkedCartGoods(id) {
		return http.put(`api/cart/products/${id}/checked/`, {}, true)
	},
	// 修改购物车中商品的数量
	updateGoodsNumber(id, params) {
		return http.put(`api/cart/products/${id}/number/`, params, true)
	},
	// 删除购物车中的商品
	deleteCartGoods(id) {
		return http.delete(`api/cart/products/${id}/`, true)
	}

}
