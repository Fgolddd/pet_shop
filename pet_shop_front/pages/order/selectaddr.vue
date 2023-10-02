<template>
	<view>
		<!-- 默认收货地址 -->
		<view class="addr_box" v-if='defaultAddr' @click='selectAddr(defaultAddr.id)'>
			<view class='addr'>
				<text>{{defaultAddr.province+defaultAddr.city+defaultAddr.county+defaultAddr.address}}</text>
			</view>
			<view class='name'>
				<uni-tag text="默认" type="success" inverted />
				<text>{{defaultAddr.name}}</text>
				<text>{{defaultAddr.phone}}</text>
			</view>
		</view>
		<!-- 其他收货地址 -->
		<view class="addr_box" v-for='addr in address' :key="addr.id" @click='selectAddr(addr.id)'>
			<view class='addr'>
				<text>{{addr.province+addr.city+addr.county+addr.address}}</text>
			</view>
			<view class='name'>
				<text>{{addr.name}}</text>
				<text>{{addr.phone}}</text>
			</view>
		</view>

	</view>
</template>

<script>
	import {
		mapGetters
	} from 'vuex'
	export default {
		computed: {
			...mapGetters(['defaultAddr', 'address'])
		},
		methods:{
			// 选择收货地址，返回订单提交页面
			selectAddr(id){
				uni.redirectTo({
					url:`/pages/order/submit?id=${id}`
				})
			}
		}
	}
</script>

<style scoped lang="scss">
	// 地址栏显示的样式
	.addr_box {
		height: 130upx;
		background: #fff;
		margin-bottom: 4upx;
		padding: 10upx 20upx;

		// 地址样式
		.addr {
			height: 80upx;
			line-height: 80upx;
			font-size: 30upx;
		}

		// 名字和电话样式
		.name {
			height: 50upx;
			line-height: 50upx;
			color: #949494;
		}

		// 按钮样式
		.edit-btn {
			height: 130upx;
			line-height: 120upx;
		}

		
	}
</style>
