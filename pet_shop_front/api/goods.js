// 商品模块接口封装
import http from './request.js'

export default{
	// 获取商城首页的数据
	getIndexData(){
		return http.get('api/products/index/')
	},
	// 获取单个商品的详情
	getGoodsDetail(productId){
		return http.get(`api/products/list/${productId}/`)
	},
	// 根据商品分类获取商品数据
	getGoodsList(params){
		return http.get('api/products/list/',params)
	},
	// 获取收藏的商品列表
	getCollectList(){
		return http.get('api/products/collect/',{},true)
	},
	// 收藏商品 
	collectGoods(params){
		return http.post('api/products/collect/',params,true)
	},
	// 取消收藏
	delCollectGoods(id){
		return http.delete(`api/products/collect/${id}/`,{},true)
	}
}