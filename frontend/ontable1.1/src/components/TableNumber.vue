<template>
    <div class="card">
        <div class="card-body">
            <div class="card-title">
                <label for="table_number">Votre numéro de table </label>
            </div>
            <div class="form-group">
                <input id="table_number" class="form-control" type="text" v-model="table_number">
            </div>
            
            <button class="btn btn-primary" v-on:click="addTableNumber">Suivant</button>
        </div>

    </div>
</template>


<script>
export default {
    name: "TableNumber",
    data() {
        return {
            table_number: 1
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
        addTableNumber(){
            this.$store.dispatch('updatePersonName',this.name)
            this.$store.dispatch('updateCurrentStep',this.step+1)
        }
    }
}
</script>