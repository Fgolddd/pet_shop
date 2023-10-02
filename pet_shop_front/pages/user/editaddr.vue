<template>

	<view v-if='EditForm'>
		<view class="row">
			<view class="title">联系人</view>
			<input class="my-input" v-model='EditForm.name' placeholder="请输入联系人" />
		</view>
		<view class="row">
			<view class="title">电话：</view>
			<input class="my-input" v-model='EditForm.phone' placeholder="请输入电话" />
		</view>
		<view class="row">
			<view class="title">省份</view>
			<!-- 选择器组件 -->
			<picker class='sele' @change='proChange' :value='proIndex' :range='provinces' range-key='name'>
				<view class="select_box"> {{EditForm.province}}</view>
			</picker>
		</view>
		<view class="row">
			<view class="title">城市</view>
			<picker class='sele' @change='cityChange' :value='cityIndex' :range='citys' range-key='name'>
				<view class="select_box"> {{EditForm.city}}</view>
			</picker>
		</view>
		<view class="row">
			<view class="title">区县</view>
			<picker class='sele' @change='countyChange' :value='countyIndex' :range='countys' range-key='name'>
				<view class="select_box"> {{EditForm.county}}</view>
			</picker>
		</view>
		<view class="row">
			<view class="title">详细地址</view>
			<input class="my-input" v-model='EditForm.address' placeholder="请选择地址" />
		</view>



		<view class="row">
			<view class="title">设为默认</view>
			<view style="text-align: right; flex: 1;">
				<switch @change='switchDefault' :checked='EditForm.is_default' color="#55aa7f" />


			</view>
		</view>
		<view class="submit_btn">
			<button @click='submitData' type="default">提交</button>
		</view>
	</view>

</template>

<script>
	import {
		mapState,
		mapActions
	} from 'vuex'

	export default {
		data() {
			return {
				// 选中省份的索引
				proIndex: 0,
				// 保存所有的省份
				provinces: [],
				cityIndex: 0,
				// 省份下的市
				citys: [],
				countyIndex: 0,
				// 市下面的区县
				countys: [],
				// 区县
				EditForm: {
					address: "",
					city: "",
					county: "",
					is_default: false,
					name: "",
					phone: "",
					province: "",
				},
				// 是否是添加地址的操作
				isAdd: true
			}
		},
		computed: {
			...mapState(['addrList', 'userInfo']),
		},
		methods: {
			...mapActions(['getAddrList']),
			// 提交编辑的表单数据
			async submitData() {
				// 发送请求修改地址数据
				await this.updateAddr()
				// 是否设置为默认收货地址
				await this.setDefault()
				this.getAddrList()
				// 跳转到上级页面
				setTimeout(()=>{
					uni.navigateBack()
				},1000)
			},
			// 修改是否默认的状态
			switchDefault(){
				this.EditForm.is_default = !this.EditForm.is_default
			},
			// 设置为默认地址
			async setDefault() {
				// 判断是否设置为默认地址
				if (this.EditForm.is_default) {
					const response = await this.$api.user.setDefaultAddr(this.EditForm.id)
					if (response.status === 200) {
						console.log('默认地址修改：', response.data)
					}
				}

			},
			async updateAddr() {
				// 修改地址的请求参数
				const params = {
					province: this.EditForm.province,
					city: this.EditForm.city,
					county: this.EditForm.county,
					address: this.EditForm.address,
					name: this.EditForm.name,
					phone: this.EditForm.phone,
					user: this.userInfo.id

				}
				// 发送请求修改地址
				const response = await this.$api.user.updateAddress(this.EditForm.id, params)
				if (response.status === 200) {
					// 修改成功
					uni.showToast({
						title: "修改成功!"
					})
				
				}
			},

			// 获取省份的方法
			async getProvinceData() {
				const response = await this.$api.user.getArea(0)
				if (response.status === 200) {
					this.provinces = response.data
				}
			},
			// 获取选中省份下的所有市
			async getCityData(level) {
				const response = await this.$api.user.getArea(level)
				if (response.status === 200) {
					this.citys = response.data
					this.EditForm.city = this.citys[0].name
					this.getCountyData(this.citys[0].pid)
				}
			},
			// 获取选择市下面的所有区县
			async getCountyData(level) {
				const response = await this.$api.user.getArea(level)
				if (response.status === 200) {
					this.countys = response.data
					this.EditForm.county = this.countys[0].name
				}
			},
			// 选中的省份发送变化
			proChange(item) {
				// 更改选中省份的索引
				this.proIndex = item.detail.value
				this.EditForm.province = this.provinces[this.proIndex].name
				const pid = this.provinces[this.proIndex].pid
				this.getCityData(pid)
			},
			// 选中的城市发生变化
			cityChange(item) {
				// 更改选中城市的索引
				this.cityIndex = item.detail.value
				this.EditForm.city = this.citys[this.cityIndex].name
				const pid = this.citys[this.cityIndex].pid
				this.getCountyData(pid)
			},
			//选中的区县发生变化
			countyChange(item) {
				this.countyIndex = item.detail.value
				this.EditForm.county = this.countys[this.countyIndex].name
			}

		},
		onLoad(params) {
			// 判断是否是编辑操作
			if (params.id) {
				this.isAdd = false
				this.EditForm = this.addrList.find(item => {
					return params.id == item.id
				})
			}
			// 获取所有省份的数据
			this.getProvinceData()
		}

	}
</script>

<style scoped lang="scss">
	.row {
		display: flex;
		height: 100upx;
		background: #fff;
		margin-bottom: 4upx;
		padding: 5upx 20upx;
		align-items: center;

		.title {
			font-size: 34upx;

		}

		.my-input {
			margin-left: 40upx;
		}

		.sele {
			flex: 1;
		}

		.select_box {
			font-size: 34upx;
			text-indent: 40upx;
		}
	}

	.submit_btn {
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
