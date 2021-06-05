<template>
    <div>
      <b-card
        border-variant="primary"
        header="Récapitulatif de votre commande"
        header-bg-variant="primary"
        header-text-variant="white"
        align="center"
      >
        <b-card-text> 
            <div v-for="(product_quantity,idx) in products_quantiy" :key="idx">
                {{ products[idx] }}
                {{ product_quantity }}
                <b-button variant="danger" v-on:click="removeProductFromCart(idx)">Enlever</b-button>
            </div>
        </b-card-text>
      </b-card>

    </div>
</template>


<script>
export default {
    name: "OrderRecap",
    computed: {
        // TO DO: products_quantiy ne se met pas à jour car il ne considere pas que le tableau a changé
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