<template>
    <div>
      <b-card
        border-variant="primary"
        header="Order Summary"
        header-bg-variant="primary"
        header-text-variant="white"
        align="center"
      >
        <b-card-text> 
            <div v-for="(product_quantity,idx) in products_quantiy" :key="idx">
                {{ products[idx] }}
                {{ product_quantity }}
                <b-button variant="danger" v-on:click="removeProductFromCart(idx)">Remove</b-button>
            </div>
        </b-card-text>
      </b-card>

    </div>
</template>


<script>
export default {
    name: "OrderRecap",
    computed: {
        // TODO: products_quantity does not update because Vue does not detect array mutations
        products(){
            return this.$store.getters.getOrder['products']
        },
        products_quantiy(){
            return this.$store.getters.getOrder['products_quantiy']
        }
    },
    methods: {
        removeProductFromCart(index_product){
            this.$store.dispatch('removeProductFromOrder',index_product)
        }
    }
}
</script>