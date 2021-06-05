<template>
    <div>

        <div class="row">
            <div class="col-6">
                <div class="text-left">
                    {{ product.name }}
                </div>
            </div>
            <div class="col-3">
                <b-form-input
                type="number"
                id="inline-form-input-quantity"
                class="mb-2 mr-sm-2 mb-sm-0"
                v-model="quantity"
                ></b-form-input>
            </div>
            <div class="col-3">
                <b-button variant="primary" v-on:click="ajouterAuPanier">Ajouter</b-button>
            </div>
        </div>        

    </div>
</template>

<script>


export default {
    name: "Product",
    props: {
        product: {
            type: Object,
            required: true
        }
    },
    computed: {
        // TO DO: products_quantiy ne se met pas à jour
        index_product_quantiy_stored(){
            return this.$store.getters.getProductIndex(this.product.slug)
        }
    },
    data(){
        return {
            quantity: 0
        }
    },
    methods: {
        ajouterAuPanier(){
            //console.log(this.product.slug)
            //console.log(this.quantity)
            var quantity = this.quantity
            var product_slug = this.product.slug
            if (this.quantity > 0){
                this.$store.dispatch('updateProductToOrder',{product_slug,quantity}) // TODO : switch en update
            }
            console.log(this.$store.getters.getOrder['products'])
            
        }
    }
}
</script>