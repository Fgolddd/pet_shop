<template>
	<view class='up_box'>
		<uni-forms ref="baseForm" :modelValue="formData">
			<uni-forms-item>
				<uni-easyinput v-if='isbind' prefixIcon="phone"  v-model="formData.mobile" placeholder="请输入手机号码" />
				<uni-easyinput v-else disabled prefixIcon="phone"  v-model="formData.mobile" placeholder="请输入手机号码" />
			</uni-forms-item>
			<uni-forms-item >
				<uni-row class="demo-uni-row" :gutter='40' >
					<uni-col :span="12">
						<uni-easyinput prefixIcon="chat-filled" placeholder="请输入验证码"  v-model="formData.code" />
					</uni-col>
					<uni-col :span="12">
						<button v-if='disable' size="mini" @click='sendMsg'>获取短信验证码</button>
						<button v-else class='dis' size="mini" @click='sendMsg'>{{count}}(s)可再次获取</button>
					</uni-col>
				</uni-row>

			</uni-forms-item>
		</uni-forms>
		<button v-if='isbind' @click='bindMobile'>绑定</button>
		<button v-else @click='unbindMobile'>解绑</button>
	</view>
</template>

<script>
	import {
		mapState,
		mapMutations
	} from 'vuex'
	export default {
		data() {
			return {
				formData: {
					code: "",
					mobile: "",
					codeID: "",
				},
				// 发送验证码
				disable: true,
				count: 60,
				isbind:true,
			}
		},
		methods: {
			...mapMutations(['saveUserInfo']),
			async sendMsg() {
				// 禁用发送验证码的按钮
				this.disable = false
				this.count = 60
				// 调用发送验证码的接口
				const response = await this.$api.user.sendsms({
					mobile: this.formData.mobile
				})
				if (response.statusCode === 200) {
					// 保存验证码的id
					this.formData.codeID = response.data.codeID
				}
				// 使用定时器控制验证码发送的时间
				setInterval(() => {
					if (this.count===0){
						// 启用发送验证码的接口
						this.disable = true
						clearInterval()
					}else{
						this.count--
					}	
				}, 1000)

			},
			// 绑定手机号
			async bindMobile(){
				const uid = this.userInfo.id
				const response = await this.$api.user.bindMobile(uid,this.formData)
				if(response.statusCode===200){
					uni.showToast({
						title:response.data.message
					})
					// 从新获取用户信息
					this.getUserInfo(uid)
					// 返回设置页面
					uni.navigateBack()
				}
			},
			// 解绑手机号
			async unbindMobile(){
				const uid = this.userInfo.id
				const response = await this.$api.user.unBindMobile(uid,this.formData)
				if(response.statusCode===200){
					uni.showToast({
						title:response.data.message
					})
					// 从新获取用户信息
					this.getUserInfo(uid)
					uni.navigateBack()
				}
			},
			async getUserInfo(id) {
				const response = await this.$api.user.getUserInfo(id)
				if (response.statusCode === 200) {
					// 保存用户信息到vuex中
					this.saveUserInfo(response.data)
				}
			},
		},
		computed: {
			...mapState(['userInfo'])
		},
		onLoad() {
			if(this.userInfo.mobile){
				this.isbind = false
				this.formData.mobile = this.userInfo.mobile
			}
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

		.dis {
			background: #f4f4f4;
			color: #888888;
		}
	}
</style>
