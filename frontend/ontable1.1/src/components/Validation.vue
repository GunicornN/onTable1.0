<template>
    <div>
        <div class="order-recap">
            <OrderRecap/>
        </div>

        <div class="total">
            Total de la commande : {{ total }}€
        </div>

        <b-row class="mt-2">
            <b-col lg="12"><b-button size="lg" v-on:click="addPaymentMethod">Valider votre commande</b-button></b-col>
        </b-row>
    </div>
</template>

<script>

import OrderRecap from './OrderRecap.vue'

export default {
    name: "Validation",
    components: {
        OrderRecap
    },
    data(){
        return {
            total: 0
        }
    },
    computed: {
        step(){
            // accès direct, c'est pas la bonne façon de le faire
            // return this.$store.state.order

            // Getters, pour simplifier l'accès aux données
            return this.$store.getters.getCurrentStep
        }
    },
    methods: {
        validateOrder(){
            this.$store.dispatch('updateCurrentStep',this.step+1)
        }
    }
}

</script>