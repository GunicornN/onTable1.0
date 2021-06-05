<template>
    <div>

        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">: Commande en ligne</b-navbar-brand>

        </b-navbar>
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
                        <b-button variant="success" v-on:click="next">Suivant</b-button>
                    </div>

                    <div v-else-if="step == 3" id="order-recap">
                        <PaymentMethod/>
                    </div>
                    <div v-else-if="step == 4" id="order-recap">
                        <Validation/>
                    </div>
                </div>
            </div>

        </div>

    </div>

</template>


<script>

import OrderRecap from '@/components/OrderRecap.vue'
import ProductList from '@/components/ProductList.vue'
import CustomerName from '@/components/CustomerName.vue'
import TableNumber from '@/components/TableNumber.vue'
import PaymentMethod from '@/components/PaymentMethod.vue'
import Validation from '@/components/Validation.vue'

export default {
    name: "OrderView",
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
    methods: {
        next(){
            this.$store.dispatch('updateCurrentStep',this.step+1)
            console.log(this.step)
        }        
    }
}
</script>