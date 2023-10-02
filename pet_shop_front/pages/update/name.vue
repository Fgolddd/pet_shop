<template>
	<view class='up_box'>
		<uni-forms ref="baseForm" :modelValue="formData">
			<uni-forms-item>
				<uni-easyinput v-model="formData.last_name" placeholder="请输入昵称" />
			</uni-forms-item>
		</uni-forms>
		<button @click='saveName'>保存</button>


	</view>
</template>

<script>
	import {
		mapState,
		mapMutations
	} from 'vuex'
	export default {
		computed:{
			...mapState(['userInfo'])
		},
		onLoad() {
			this.formData.last_name = this.userInfo.last_name
		},
		data() {
			return {
				formData: {
					last_name: ''
				}
			}
		},
		methods: {
			...mapMutations(['saveUserInfo']),
			// 保存用户名
			async saveName() {
				const response  = await this.$api.user.updateName(this.userInfo.id,this.formData)
				if(response.statusCode===200){
					uni.showToast({
						title:'修改成功!'
					})
					// 更新vuex中的用户数据
					this.getUserInfo(this.userInfo.id)
				}
			},
			async getUserInfo(id) {
				const response = await this.$api.user.getUserInfo(id)
				if (response.statusCode === 200) {
					// 保存用户信息到vuex中
					this.saveUserInfo(response.data)
				}
			},
		}
	}
</script>

<style scoped lang="scss">
	.up_box {
		margin: 40upx 10upx 20upx 10upx;

		button {
			background: #55aa7f;
			color: #fff;
			height: 74upx;
			line-height: 74upx;
		}
	}
</style>
