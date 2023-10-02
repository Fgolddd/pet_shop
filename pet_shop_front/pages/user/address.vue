<template>
	<view>
		<!-- 默认收货地址 -->
		<view class="addr_box" v-if='defaultAddr'>
			<uni-row class="demo-uni-row">
				<uni-col :span="21">
					<view class='addr'>

						<text>{{defaultAddr.province+defaultAddr.city+defaultAddr.county+defaultAddr.address}}</text>
					</view>
					<view class='name'>
						<uni-tag text="默认" type="success" inverted />
						<text>{{defaultAddr.name}}</text>
						<text>{{defaultAddr.phone}}</text>
					</view>
				</uni-col>
				<uni-col :span="3">
					<view class="edit-btn">
						<uni-icons @click='editAddr(defaultAddr.id)' type="compose" size="30"></uni-icons>
					</view>
				</uni-col>
			</uni-row>
		</view>
		<!-- 其他收货地址 -->
		<view class="addr_box" v-for='addr in address' :key="addr.id">
			<uni-row class="demo-uni-row">
				<uni-col :span="21">
					<view class='addr'>
						<text>{{addr.province+addr.city+addr.county+addr.address}}</text>
					</view>
					<view class='name'>
						<text>{{addr.name}}</text>
						<text>{{addr.phone}}</text>
					</view>
				</uni-col>
				<uni-col :span="3">
					<view class="edit-btn">
						<uni-icons @click='editAddr(addr.id)' type="compose" size="30"></uni-icons>
					</view>
				</uni-col>
			</uni-row>
		</view>

		<view class="add_btn">
			<button @click='toCreateAddr()' type="default" >添加地址</button>
		</view>
	</view>
</template>

<script>
	import {
		mapActions,
		mapState,
		mapGetters
	} from 'vuex'
	export default {
		computed: {
			...mapState(['addrList']),
			...mapGetters(['defaultAddr', 'address'])
		},
		methods: {
			...mapActions(['getAddrList']),
			// 编辑收货地址
			editAddr(id) {
				uni.navigateTo({
					url: `/pages/user/editaddr?id=${id}`
				})
			},
			toCreateAddr(){
				uni.navigateTo({
					url: "/pages/user/createaddr"
				})
			}
		},
		onLoad() {
			this.getAddrList()
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

	// 添加收货地址按钮的样式
	.add_btn {
		position: fixed;
		width: 100%;
		bottom: 10upx;
		button {
			color: #fff;
			background: #55aa7f;
			height: 74upx;
			line-height: 74upx;
			margin: 0 10upx;
		}
	}
</style>
