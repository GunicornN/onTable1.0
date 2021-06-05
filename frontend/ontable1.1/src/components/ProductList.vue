<template>
    <div class="card">
        <div class="card-body">
            <div class="card-title">
                <label >Choisissez vos plats  </label>
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
import axios from 'axios';

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
        // Fetches posts when the component is created.
        //console.log(this.products)
        var api_address = 'http://127.0.0.1:8000/api/companies/'+this.company_slug+'/products/' 
        axios.get(api_address)
        .then(response => {
        // JSON responses are automatically parsed.
        this.company_products = response.data
        })
        .catch(e => {
        console.log(e)
        })
    },
}
</script>