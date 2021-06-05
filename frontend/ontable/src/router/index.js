import { createRouter, createWebHistory } from 'vue-router';
import OrderView from '../views/OrderView.vue'
import CompanyDetailsView from '../views/CompanyDetailsView.vue'

// création des routes
/*

    companies/<slug>
    companies/<company_code>

    /order/<company_slug>/ 
    /order/

    /order/cart/
    /order/<company_slug>/cart/

    /order/<company_slug>/table/

    /order/table/
    /order/<company_slug>/table/

*/
const routes = [
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

// creation du router 

const router = createRouter({
    history: createWebHistory,
    routes
})

export default router