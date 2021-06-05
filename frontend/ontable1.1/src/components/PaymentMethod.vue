<template>
    <div>
        <b-card-group deck>
            <b-card header="Carte Bancaire" class="text-center">

                <b-card-body>
                    <div class="choice-payment-method-cb">
                        <img src="../assets/payment_methods/cb.png" alt="cb">
                        <input type="radio" v-model="payment_method" value="CB">
                    </div>
                </b-card-body>
            </b-card>

            <b-card header="Espèces" class="text-center">

                <b-card-body>
                    <div class="choice-payment-method-cash">
                        <img src="../assets/payment_methods/cash.png" alt="cash">
                        <input type="radio" v-model="payment_method" value="cash">
                    </div>
                </b-card-body>
            </b-card>

            <b-card header="Chèque" class="text-center">

                <b-card-body>
                    <div class="choice-payment-method-bank-check">
                        <img src="../assets/payment_methods/bank_check.png" alt="bank_check">
                        <input type="radio" v-model="payment_method" value="bank_check">
                    </div>
                </b-card-body>
            </b-card>
            
        </b-card-group>
        <b-row class="mt-2">
            <b-col lg="12"><b-button size="lg" v-on:click="addPaymentMethod">Suivant</b-button></b-col>
        </b-row>

    </div>
</template>

<script>
export default {
    name: "PaymentMethod",
    data() {
        return {
            payment_method: ""
        }
    },
    computed: {
        payment_method_stored() {
            return this.$store.getters.getPaymentMethod
        },
        step(){
            // accès direct, c'est pas la bonne façon de le faire
            // return this.$store.state.order

            // Getters, pour simplifier l'accès aux données
            return this.$store.getters.getCurrentStep
        }
    },
    methods: {
        addPaymentMethod(){
            //console.log(this.payment_method)
            this.$store.dispatch('updatePaymentMethod',this.payment_method)
            this.$store.dispatch('updateCurrentStep',this.step+1)
        }
    }
}
</script>