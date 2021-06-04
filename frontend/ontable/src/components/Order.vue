<template>
    <div class="row">
        <div class="col-sm-12">
            <div class="card">
                <div v-if="step == 0">
                    <CustomerName/>
                </div>
                <div v-else-if="step == 1">
                    <TableNumber/>
                </div>
                <div v-else-if="step ==2">
                    <ProductList :company_slug="company_slug"/>
                    <OrderRecap/>
                    <button v-on:click="next">Suivant</button>
                </div>

                <div v-else-if="step == 3" id="order-recap">
                    <PaymentMethod/>
                </div>

                <div v-else-if="step == 4" id="order-recap">
                    <OrderRecap/>
                </div>
                <div v-else-if="step == 5" id="order-recap">
                    <Validation/>
                </div>
            </div>
        </div>

    </div>
</template>


<script>

import OrderRecap from './OrderRecap.vue'
import ProductList from './ProductList.vue'
import CustomerName from './CustomerName.vue'
import TableNumber from './TableNumber.vue'
import PaymentMethod from './PaymentMethod.vue'
import Validation from './Validation.vue'

export default {
    name: "Order",
    props: {
        company_slug : String
    },
    components: {
        OrderRecap,
        ProductList,
        CustomerName,
        TableNumber,
        PaymentMethod,
        Validation
    },
    computed: {
        step(){
            // accès direct, c'est pas la bonne façon de le faire
            // return this.$store.state.order

            // Getters, pour simplifier l'accès aux données
            return this.$store.getters.getCurrentStep
        },
    },
    beforeMount(){
        // REMOVE THIS AFTER, adapter le code en conséquence
        this.company_slug = 'le-coq-69006'
    },
    methods: {
        next(){
            this.$store.dispatch('updateCurrentStep',this.step+1)
            console.log(this.step)
        }        
    }
}
</script>