<template>
    <div>
        <div class="order-recap">
            <OrderRecap/>
        </div>

        <div class="total">
            Order total: {{ total }}€
        </div>

        <b-row class="mt-2">
            <b-col lg="12"><b-button size="lg" v-on:click="addPaymentMethod">Validate your order</b-button></b-col>
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
            // Use getters for simplified data access
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