<template>
	<view>
		<!-- 顶部区域 -->
		<view class='top_bj'>
			<!-- 左侧：用户头像显示 -->
			<view class="user-pic">
				<!-- 登录则显示用户头像 -->
				<image v-if='isAuth' :src="userInfo.avatar"></image>
				<!-- 每天登录则显示头像图标 -->
				<uni-icons v-else type="person-filled" size="50"></uni-icons>
			</view>
			<!-- 右侧：用户信息 -->
			<view class="user_info" v-if='isAuth'>
				<view>{{userInfo.username}}</view>
				<view class='email'>手机:{{userInfo.phone}}</view>
			</view>
			<view @click="navTo('/pages/user/login')" v-else class="user_info">点击登录</view>
		</view>
		<!-- 弧形效果图 -->
		<view class='bj-image'>
			<image src="../../static/arc.png"></image>
		</view>

		<!-- 用户信息管理 -->
		<view class='menu_box'>
			<uni-list>
				<uni-list-item clickable @click="navTo('/pages/order/order')"  :show-extra-icon="true" showArrow :extra-icon="Icon1" title="订单管理" />
				<uni-list-item clickable @click="navTo('/pages/user/address')" :show-extra-icon="true" showArrow :extra-icon="Icon2" title="地址管理" />
				<uni-list-item clickable @click="navTo('/pages/product/collect')" :show-extra-icon="true" showArrow :extra-icon="Icon3" title="我的收藏" />
				<uni-list-item clickable @click="navTo('/pages/common/set')" :show-extra-icon="true" showArrow :extra-icon="Icon4" title="设置" />
			</uni-list>
		</view>


	</view>

</template>

<script>
	import {
		mapState
	} from 'vuex'

	export default {
		data() {
			return {
				// 页面显示的图标
				Icon1: {
					color: '#4cd964',
					size: '22',
					type: 'shop'
				},
				Icon2: {
					color: '#329142',
					size: '22',
					type: 'location-filled'
				},
				Icon3: {
					color: '#00aaff',
					size: '22',
					type: 'star-filled'
				},
				Icon4: {
					color: '#ff557f',
					size: '22',
					type: 'gear'
				}
			}
		},
		computed: {
			...mapState(['isAuth', 'userInfo']),
		},
		methods: {
			navTo(url) {
				if (this.isAuth) {
					uni.navigateTo({
						url: url
					})
				} else {
					console.log('url地址', url)
					uni.navigateTo({
						url: '/pages/user/login'
					})
				}

			}
		}
	}
</script>

<style scoped lang="scss">
	.top_bj {
		height: 360upx;
		background: #00aa7f;
		display: flex;
		align-items: center;

		.user-pic {
			width: 150upx;
			height: 150upx;
			border-radius: 50%;
			background: #d3d8d3;
			margin: 0 50upx;
			line-height: 150upx;
			text-align: center;

			image {
				width: 150upx;
				height: 150upx;
				border-radius: 50%;
			}


		}

		.user_info {
			flex: 1;
			color: #fff;
			font-size: 35upx;

			.email {
				font-size: 20upx;
				color: #d3d8d3;
			}
		}
	}

	.bj-image {
		margin-top: -30upx;

		image {
			width: 100%;
			height: 40upx;
		}
	}

	// 下方显示操作菜单的列表
	.menu_box {
		background: #fff;
		margin: 5upx 20upx;
	}
</style>
