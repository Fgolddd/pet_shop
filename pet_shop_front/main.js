// #ifndef VUE3
import Vue from 'vue'
import App from './App'
import store from './store'

// 导入封装的请求对象
import api from './api/index.js'

Vue.prototype.$store = store
// 将请求对象设置为全局属性
Vue.prototype.$api = api

Vue.config.productionTip = false



App.mpType = 'app'

const app = new Vue({
	store,
	...App
})
app.$mount()
// #endif

// #ifdef VUE3
import {
	createSSRApp
} from 'vue'
import App from './App.vue'
export function createApp() {
	const app = createSSRApp(App)
	return {
		app
	}
}
// #endif
