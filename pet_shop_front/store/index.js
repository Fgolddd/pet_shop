import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index.js'
Vue.use(Vuex);

const store = new Vuex.Store({
	// 全局数据
	state: {
		token: "",
		userInfo: {},
		// 用户是否登录
		isAuth: false,
		// 商品分类
		goodsGroup: [],
		activaGroupId: null,
		// 保存购物车商品
		cartGoodsList: [],
		// 保存收藏商品的数据
		collectList:[],
		// 用户所有的地址列表
		addrList:[]
	},
	// 全局的计算属性
	getters: {
		// 购物车中商品的数量
		cartNumber(state){
			return state.cartGoodsList.length
		},
		defaultAddr(state){
			return  state.addrList.find(item=>{
				return item.is_default
			})
		},
		address(state){
			return  state.addrList.filter(item=>{
				return !item.is_default
			})
		}
	},
	// 修改数据的方法
	mutations: {
		// 保存登录后的用户信息
		saveLoginStatus(state, info) {
			state.isAuth = true
			state.token = info.token
			// 存储到uniapp提供的持久化数据存储仓库中
			uni.setStorage({
				key: "isAuth",
				data: true
			})
			uni.setStorageSync("token", info.token)
			uni.setStorage({
				key: "refresh",
				data: info.refresh
			})
		},
		saveUserInfo(state, user) {
			// 保存用户信息
			state.userInfo = user
			uni.setStorage({
				key: "userinfo",
				data: user
			})
		},
		// 保存商品分类信息的方法
		saveGoodsGroup(state, info) {
			state.goodsGroup = info
			uni.setStorage({
				key: "goodsGroup",
				data: info
			})
		},
		saveActivaGroupId(state, info) {
			state.activaGroupI = info
		},
		// 保存购物车中数据的方法
		saveCartList(state, value) {
			state.cartGoodsList = value
			uni.setStorage({
				key:"cart",
				data:value
			})
		},
		// 保存收藏商品数据的方法
		saveCollectList(state,value){
			state.collectList = value
			uni.setStorage({
				key:"collect",
				data:value
			})
		},
		//  保存用户的收货地址列表
		saveAddrList(state,value){
			state.addrList = value
			uni.setStorage({
				key:"addr",
				data:value
			})
			// uni.getStorage({
			// 	key:'addr',
			// 	success(res) {
			// 		console.log(res.data);
			// 	}
			// })
			
		},
		// 退出登录
		logout(state) {
			state.isAuth = false
			state.userInfo = {}
			uni.clearStorage()
			// 跳转到商城首页
			uni.switchTab({
				url: "/pages/index/index"
			})
		}
	},
	// 全局操作的方法
	actions: {
		// 获取购物车中所有的商品
		async getCartGoodsList(context) {
			// 发送请求
			const response = await api.cart.getCartGoods()
			if (response.statusCode === 200) {
				// 将购物车中的商品数据保存到vuex的state中
				context.commit('saveCartList',response.data)
			}
		},
		// 添加商品到购物车的方法
		async addGoodsCart(context,goodsId){
			// 发送请求
			const response =await api.cart.addGoods({
				product:goodsId
			})
			// 判断接口请求是否成功
			if(response.statusCode===201){
				uni.showToast({
					title:'已为您加入购物车'
				})
				// 更新购物车中的数据
				context.dispatch('getCartGoodsList')
			}
		},
		// 获取已收藏的商品列表
		async getCollectList(context){
			const response = await api.goods.getCollectList()
			if(response.statusCode===200){
				context.commit('saveCollectList',response.data)
			}
		},
		// 取消收藏的方法
		async delCollect(context,g){
			const response = await api.goods.delCollectGoods(g.id)
			if(response.statusCode===204){
				context.dispatch('getCollectList')
				uni.showToast({
					title:"已取消收藏"
				})
			}
		},
		// 获取所有的收货地址列表
		async getAddrList(context){
			// 获取用户所有的收货地址
			const response = await api.user.getAddress()
			if(response.statusCode===200){
				// 保存收货地址
				context.commit('saveAddrList',response.data)
			}
		},
		// 加载用户数据的方法
		loadData(context){
			// 加载用户收货地址
			context.dispatch('getAddrList')
			// 加载用户购物车商品
			context.dispatch('getCartGoodsList')
			// 加载用户收藏列表
			context.dispatch('getCollectList')
		}
		
		
	}
})
export default store;
