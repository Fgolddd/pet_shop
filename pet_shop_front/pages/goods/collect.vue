<template>
	<view>
	<view class='goods-item' v-for='g in collectList' :key='g.id'>
		<uni-row class="demo-uni-row" >
			<!-- 商品图 -->
			<uni-col :span="12">
				<image class='goods-pic' :src="g.goods.cover"  @click='toGoodsDetail(g.goods.id)'></image>
			</uni-col>
			<!-- 商品的价格和描述 -->
			<uni-col :span="8">
				<view class="info" @click='toGoodsDetail(g.goods.id)' >
					<view class="g-title">{{g.goods.title}}</view>
					<view class="g-desc">{{g.goods.desc}}</view>
					<view class="g-price">￥{{g.goods.price}}/份</view>
				</view>
			</uni-col>
			<!-- 取消收藏 -->
			<uni-col :span="4">
				<view class="cart-icon" @click='delCollect(g)' >
					<uni-icons type="trash-filled" size="24" color="#ff557f"></uni-icons>
				</view>
			</uni-col>
		</uni-row>
	
	</view>
	</view>
</template>

<script>
	import {mapActions,mapState} from 'vuex'
	export default {
		computed:{
			...mapState(['collectList'])
		},
		methods:{
			...mapActions(['getCollectList','delCollect']),
			// 跳转到商品详情页
			toGoodsDetail(goodsId){
				const url = `/pages/goods/detail?id=${goodsId}`
				uni.navigateTo({
					url:url
				})
			},
		},
		onLoad() {
			this.getCollectList()
		}
	}
</script>

<style scoped lang="scss">
	// 单个商品
	.goods-item {
		margin: 15upx;
		background: #fff;
		height: 300upx;
		border-radius: 10upx;
	
		// 商品图
		.goods-pic {
			width: 300upx;
			height: 300upx;
		}
		// 商品文字信息
		.info{
			// 商品的标题
			.g-title{
				font-size: 30upx;
				height: 100upx;
				line-height: 100upx;
			}
			// 商品的描述
			.g-desc{
				font-size: 20upx;
				height: 100upx;
				line-height: 25upx;
				color: #8b8b8b;
			}
			// 商品的价格
			.g-price{
				font-weight: bold;
				color: #ff557f;
				font-size: 30upx;
				height: 100upx;
				line-height: 100upx;
			}
		}
		// 购物车图标样式
		.cart-icon{
			width: 50px;
			text-align: center;
			line-height: 300upx;
			image{
				width: 30px;
				height: 30px;
				background: #ececec;
				border-radius: 50%;
			}
		}
	}
</style>
