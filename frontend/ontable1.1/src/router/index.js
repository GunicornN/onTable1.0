import { createRouter, createWebHistory } from 'vue-router'
import OrderView from '../views/OrderView.vue'
import CompanyDetailsView from '../views/CompanyDetailsView.vue'
import Home from '../views/Home.vue'
//component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
const routes = [
  {
      name: 'Home',
      path: '/',
      component : Home
  },
  {
      name: 'Order',
      path: '/orders/:company_slug',
      component: OrderView
  },
  {
      name: 'CompanyDetailsView',
      path: '/companies/',
      component : CompanyDetailsView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
