<template>
	<view class='detail-box' v-if='goods.detail'>
		<!-- 商品图 -->
		<view class='goods-pic'>
			<image :src="goods.cover" style="width: 100%" mode="widthFix"></image>
		</view>
		<!-- 商品的基本信息 -->
		<view class=info>
			<view class="name">{{goods.title}}</view>
			<view class="desc">{{goods.desc}}</view>
			<view class='price'>￥{{goods.price}}/per</view>
			<!-- 销量和库存 -->
			<uni-row class="demo-uni-row">
				<uni-col :span="12">
					<view class="desc">销量:{{goods.sales}}</view>
				</uni-col>
			</uni-row>
		</view>
		<!-- 其他信息 -->
		<uni-list border-full>
			<uni-list-item>
				<template v-slot:header>
					<text class="name1">{{'商家:' +'     '+ '暂时没有'}}</text>
				</template>
			</uni-list-item>
			
			<uni-list-item>
				<template v-slot:header>
					<text class="name1">{{'服务:' +'     品质保证不满意包退'}}</text>
				</template>
			</uni-list-item>
		</uni-list>

		<!-- 商品评价信息 -->
		<view style="margin: 10upx 0;">
			<uni-list border-full>
				<uni-list-item showArrow title="商品评价" rightText="查看" />
			</uni-list>
		</view>
		<!-- 商品详情 -->
		<view class="detail-info">
			<view style="text-align: center; font-size: 32upx; line-height: 80upx;">图文详情</view>
			<rich-text :nodes="goods.detail.details"></rich-text>
		</view>

		<!-- 商品导航 -->
		<view class="goods-carts">
			<uni-goods-nav :options="options" :fill="true" :button-group="buttonGroup" @click="onClick"
				@buttonClick="buttonClick" />
		</view>
	</view>
</template>

<script>
	import {
		mapActions,
		mapGetters,
		mapState
	} from 'vuex'

	export default {
		computed: {
			...mapState(['userInfo', 'collectList']),
			...mapGetters(['cartNumber', ]),
			// 商品导航栏配置
			options() {
				// 判断商品是否已收藏
				const res = this.collectList.find(item => {
					return item.goods.id === this.goods.id
				})
				// 判断是否已收藏
				if (res) {
					return [{
						icon: 'star-filled',
						text: '已收藏',
					}, {
						icon: 'cart',
						text: '购物车',
						info: this.cartNumber
					}]
				} else {
					return [{
						icon: 'star',
						text: '收藏'
					}, {
						icon: 'cart',
						text: '购物车',
						info: this.cartNumber
					}]
				}

			}
		},
		data() {
			return {
				// 商品数据
				goods: {},

				buttonGroup: [{
					text: '加入购物车',
					backgroundColor: 'linear-gradient(90deg, #55aa7f, #00bd8b)',
					color: '#fff'
				}, ],
			}
		},
		methods: {
			...mapActions(['addGoodsCart','delCollect','getCollectList']),
			// 点击收藏或者购物车时调用
			onClick(e) {
				if (e.content.text === '购物车') {
					// 跳转到购物车页面
					uni.switchTab({
						url: "/pages/cart/cart"
					})
				} else if (e.content.text === '收藏') {
					// 收藏商品
					this.clloectGoods()
				}else {
					// 取消收藏该商品
					// 查找该商品的收藏记录
					const res =  this.collectList.find(item=>{
						return item.goods.id===this.goods.id
					})
					// 删除该收藏记录
					this.delCollect(res)
				}

			},
			// 收藏商品
			async clloectGoods() {
				// 收藏商品
				const response = await this.$api.goods.collectGoods({
					user: this.userInfo.id,
					goods: this.goods.id
				})
				console.log('收藏商品!')
				if (response.statusCode === 201) {
					uni.showToast({
						title: '收藏成功'
					})
					// 更新收藏列表的数据
					this.getCollectList()
				}

			},
			buttonClick(e) {
				// 点击加入购物车时调用
				console.log(e)
				this.addGoodsCart(this.goods.id)

			}
		},
		async onLoad(option) {
			// 发送请求到后台,加载商品的数据
			const response = await this.$api.goods.getGoodsDetail(option.id)
			if (response.statusCode === 200) {
				this.goods = response.data
			}
		}
	}
</script>

<style scoped lang="scss">
	.info {
		padding: 40upx;
		background: #fff;

		.name {
			font: normal 30upx/80upx '微软雅黑';
		}

		.desc {
			color: #818181;
		}

		.price {
			color: #ff557f;
			font-size: 40upx;
			line-height: 80upx;
		}
	}

	.name1 {
		font-size: 28upx;
	}

	.detail-info {
		background: #fff;
	}

	// 商品导航
	.goods-carts {
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: column;
		position: fixed;
		left: 0;
		right: 0;
		/* #ifdef H5 */
		left: var(--window-left);
		right: var(--window-right);
		/* #endif */
		bottom: 0;
	}
</style>
