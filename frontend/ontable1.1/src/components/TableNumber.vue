<template>
    <div class="card">
        <div class="card-body">
            <div class="card-title">
                <label for="table_number">Your table number</label>
            </div>
            <div class="form-group">
                <input id="table_number" class="form-control" type="text" v-model="table_number">
            </div>
            
            <button class="btn btn-primary" v-on:click="addTableNumber">Next</button>
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
            // Use getters for simplified data access
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