<template>
    <div class="card">
        <div class="card-body">
            <div class="card-title">
                <label for="name">Comment vous vous appellez ?  </label>
            </div>
            <div class="form-group">
                <input id="name" class="form-control" type="text" v-model="name">
            </div>
            
            <button class="btn btn-primary" v-on:click="addCustomerName">Suivant</button>
        </div>

    </div>
</template>

<script>
export default {
    name: "CustomerName",
    data() {
        return {
            name: ""
        }
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
        addCustomerName(){
            this.$store.dispatch('updatePersonName',this.name)
            this.$store.dispatch('updateCurrentStep',this.step+1)
            //console.log(this.step)
        }
    }
}
</script>