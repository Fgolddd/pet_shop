<script>
	import {
		mapMutations,
	
	} from 'vuex'
	export default {
		methods: {
			...mapMutations(['saveLoginStatus', 'saveUserInfo','saveGoodsGroup','saveCollectList','saveCartList','saveAddrList']),
			
		},
		onLaunch: function() {
			console.warn('当前组件仅支持 uni_modules 目录结构 ，请升级 HBuilderX 到 3.1.0 版本以上！')
			console.log('App Launch')
		},
		onShow: function() {
			// 解决刷新页面,vuex中用户信息数据丢失的问题.
			// 读取ninapp 的Storage中存储的用户信息数据,保存到veux中
			const uinfo = uni.getStorageSync('userinfo') || {}
			const loginStatus = {
				token: uni.getStorageSync('token'),
				refresh: uni.getStorageSync('refresh')
			}
			const isAuth = uni.getStorageSync('isAuth')
			if(isAuth){
				// 保存登录状态
				this.saveLoginStatus(loginStatus)
				// 保存用户信息
				this.saveUserInfo(uinfo)
				// 保存购物车商品
				this.saveCartList(uni.getStorageSync('cart'))
				// 保存收藏商品
				this.saveCollectList(uni.getStorageSync('collect'))
				// 保存收货地址
				this.saveAddrList(uni.getStorageSync('addr'))
				
			}
			// 保存商品分类信息到vuex中
			this.saveGoodsGroup(uni.getStorageSync('goodsGroup'))
			
		},
		onHide: function() {
			console.log('App Hide')
		},
		
	}
</script>

<style lang="scss">
	/*每个页面公共css */
	@import '@/uni_modules/uni-scss/index.scss';
	/* #ifndef APP-NVUE */
	@import '@/static/customicons.css';

	// 设置整个项目的背景色
	page {
		background-color: #f5f5f5;
	}

	/* #endif */
	.example-info {
		font-size: 14px;
		color: #333;
		padding: 10px;
	}
</style>
