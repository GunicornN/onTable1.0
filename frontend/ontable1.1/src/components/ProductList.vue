<template>
    <div class="card">
        <div class="card-body">
            <div class="card-title">
                <label>Choose your dishes</label>
            </div>

            <b-list-group>
                <b-list-group-item v-for="product in company_products" :key="product.id">
                    <Product :product="product" />  
                </b-list-group-item>
            </b-list-group>
        </div>

    </div>
</template>

<script>

import Product from './Product.vue'
import axios from 'axios'
import config from '../config'

export default {
    name: "ProductList",
    props: {
        company_slug : {
            type: String,
            required: true
        }
    },
    components: {
        Product
    },
    data(){
        return {
            company_products: {}
        }
    },
    created() {
        const api_address = `${config.API_BASE_URL}/api/companies/${this.company_slug}/products/`
        axios.get(api_address)
        .then(response => {
            this.company_products = response.data
        })
        .catch(e => {
            console.log(e)
        })
    },
}
</script>