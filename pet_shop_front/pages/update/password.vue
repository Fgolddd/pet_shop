<template>
	<view class='up_box'>
		<uni-forms ref="baseForm" :modelValue="formData">
			<uni-forms-item>
				<uni-easyinput prefixIcon="locked" type="password" v-model="formData.password" placeholder="请输入新密码" />
			</uni-forms-item>
			<uni-forms-item>
				<uni-easyinput prefixIcon="locked-filled" type="password" v-model="formData.password_confirmation"
					placeholder="再次输入新密码" />
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
		<button @click='savePwd'>保存</button>


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
					password: "",
					password_confirmation: "",
					codeID: "",
					mobile:""
				},
				// 发送验证码
				disable: true,
				count: 60,
			}
		},
		methods: {
			async sendMsg() {
				// 禁用发送验证码的按钮
				this.disable = false
				this.count = 60
				// 调用发送验证码的接口
				const response = await this.$api.user.sendsms({
					mobile: this.userInfo.mobile
				})
				if (response.statusCode === 200) {
					// 保存验证码的id
					this.formData.codeID = response.data.codeID
					this.formData.mobile = this.userInfo.mobile
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
			// 保存修改的密码
			async savePwd(){
				// 准备修改密码的参数
				const uid = this.userInfo.id
				// 发送请求
				const response = await this.$api.user.updatePwd(uid,this.formData)
				if(response.statusCode===200){
					uni.showToast({
						title:"修改成功"
					})
				}
			}
		},
		computed: {
			...mapState(['userInfo'])
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
