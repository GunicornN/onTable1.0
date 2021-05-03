<template>
  <div class="company">
    <h1>Entreprise</h1>
    
    <div>
        {{ company.name }}
        {{ company.address1 }}
        {{ company.address2 }}
        {{ company.city }}
        {{ company.country }}
        {{ company.zip_code }}
    </div>

    <div class="cards">


    </div>
  </div>
</template>


<script>

import axios from 'axios'

export default {
    name: 'company-details',
    props:{
        slug: {
            type: String,
            required: true
        }
    },
    data(){
            return {
                company: null,
                api_address: process.env.APP_ROOT_API,
                error: ""
            }
    },
    methods: {
        get_company_details: function(){
            let endpoint = this.api_address+"companies/"+this.slug+"/"
            axios
            .get(endpoint)
            .then(response => (this.company = response))    
        },
        get_company_cards: function(){
            //let endpoint = api_address+"company/"
            
        }
    },
    mounted(){
        axios
        .get(this.api_address)
        .then(response => (this.info = response))      
    }

}
</script>



