<template>
	<view class='status_box'>
		<!-- 支付状态图标 -->
		<view v-if='status==1'>
			<image src="../../static/pay/success.png">
			</image>
			<view class='desc'>支付成功</view>
		</view>
		<view v-else>
			<image src="../../static/pay/error.png"></image>
			<view class='desc'>支付失败</view>
		</view>

		<!-- 按钮 -->
		<button class='btn1' @click='toOrder'>查看订单</button>

		<button class='btn2' @click='toIndex'>返回首页</button>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				status: 1
			}
		},
		onLoad(item) {
			if (item.status) {
				this.status = item.status
			}
		},
		methods: {
			toOrder() {
				uni.navigateTo({
					url: "/pages/order/order"
				})
			},
			toIndex() {
				uni.switchTab({
					url: '/pages/index/index'
				})
			}
		}
	}
</script>

<style scoped lang="scss">
	.status_box {
		padding: 40upx 60upx;
		text-align: center;

		image {
			width: 200upx;
			height: 200upx;
			margin-top: 100upx;
		}

		button {
			height: 74upx;
			line-height: 74upx;
			margin-top: 40upx;

		}

		.btn1 {
			background: #55aa7f;
			color: #fff;
		}

		.desc {
			color: #939393;
		}


	}
</style>
