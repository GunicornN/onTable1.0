import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

/*
Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)


new Vue({
  store,
  router: router,
  render: h => h(App)
}).$mount('#app')
*/




const app = createApp(App).use(store)
app.use(router)
app.use(BootstrapVue)
app.use(IconsPlugin)
app.use(store)
app.mount('#app')