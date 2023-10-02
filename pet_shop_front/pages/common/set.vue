<template>
	<view>
		<!-- 用户基本信息 -->
		<uni-list>
			<!-- 用户头像 -->
			<!-- <uni-list-item showArrow :title="userInfo.username" :thumb="userInfo.avatar" thumb-size="lg" /> -->
			<uni-list-item :rightText="userInfo.username">
				<!-- 自定义 header -->
				<template v-slot:header>
					<uni-file-picker limit="1" :del-icon="false" disable-preview :imageStyles="imageStyles"
						file-mediatype="image">
						<image style="width: 100%;height: 100%;" :src="userInfo.avatar"></image>
					</uni-file-picker>
				</template>
			</uni-list-item>
			<uni-list-item clickable @click="navTo('/pages/update/name')" showArrow title="昵称" :rightText="userInfo.last_name" />
			<uni-list-item  clickable @click="navTo('/pages/update/mobile')" showArrow title="手机" :rightText="userInfo.mobile" />
			<uni-list-item clickable @click="navTo('/pages/update/email')" showArrow  title="邮箱" :rightText="userInfo.email" />
			<uni-list-item  clickable @click="navTo('/pages/update/password')" showArrow title="修改密码" />
		</uni-list>
		<!-- 版本号 -->
		<uni-list class='m-t-10'>
			<uni-list-item title="版本" rightText="1.0.0" />
		</uni-list>
		<!-- 退出登录 -->
		<view class='m-t-10 logout'>
			<button @click='logout' type="default">退出登录</button>
		</view>

	</view>





</template>

<script>
	import {
		mapMutations,
		mapState
	} from 'vuex'
	export default {
		methods: {
			...mapMutations(['logout']),
			navTo(url) {
				uni.navigateTo({
					url: url
				})
			}

		},
		data() {
			return {
				imageStyles: {
					width: 64,
					height: 64,
					border: {
						radius: '50%'
					}
				},
			}
		},
		computed: {
			...mapState(['userInfo'])
		}
	}
</script>

<style scoped lang="scss">
	.m-t-10 {
		margin-top: 10upx;
	}

	.logout {
		background-color: #fff;

		// button {
		// 	color: #55aa00;
		// 	background-color: #fff;
		// 	font-size: 28upx;
		// }
		button {
			background: #55aa7f;
			color: #fff;
			height: 74upx;
			line-height: 74upx;
		}
	}
</style>
