<template>
    <div>
        <form class="login" @submit.prevent="register">
            <label for="first_name"> Prénom </label>
            <input required v-model="first_name" type="text" placeholder="Prénom">

            <label for="last_name"> Nom </label>
            <input required v-model="last_name" type="text" placeholder="Nom">

            <label for="name"> Entreprise </label>
            <input required v-model="name" type="text" placeholder="Entreprise">

            <label for="address1"> Adresse de l'entreprise </label>
            <input required v-model="address1" type="text" placeholder="420 Rue du Général">

            <label for="address2"> Complément d'adresse </label>
            <input required v-model="address2" type="text">

            <label for="city"> Ville</label>
            <input required v-model="city" type="text" placeholder="Lyon">

            <label for="zip_code"> Code postal</label>
            <input required v-model="zip_code" type="number" placeholder="69000">

            <label for="password1">Mot de passe</label>
            <input required v-model="password1" type="password" placeholder="">

            <label for="password2">Confirmation du mot de passe</label>
            <input required v-model="password1" type="password" placeholder="">

        </form>
    </div>
</template>


<script>
export default {
    name:"Register",
    data(){
        return {
            userForm: {
                first_name: "",
                last_name: "",
                password1: "",
                password2: ""
            },
            companyForm: {
                name: "",
                address1: "",
                address2: "",
                city: "",
                zip_code: Number
            },
            error: ""
        }
    },
    methods: {
        register: function(){ // Faire cette fonction
            let email = this.email
            let password = this.password
            this.$store.dispatch('login',{email,password})
            .then( ()=> this.$router.push('/'))
            .catch( () => this.displayError())
        },
        displayError(){
            this.error = "Le mot de passe et/ou l'adresse mail sont incorrects."
        }

    }
}
</script>