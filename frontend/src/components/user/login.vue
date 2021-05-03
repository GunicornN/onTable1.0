<template>
    <div>
        <form class="login" @submit.prevent="login">
            <label for="">Email</label>
            <input required v-model="email" type="email" placeholder="Adresse mail">
            <label for="">Mot de passe </label>
            <input required v-model="username" type="password" placeholder="Adresse mail">

            <button type="submit">Connexion</button>
        </form>
    </div>
</template>



<script>
export default {
    name: "Login",
    data(){
        return {
            loginInfo: {
            username: "",
            email: "",
        },
        error: ''    
        }
    },
    methods: {
        login: function(){
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


<style lang="stylus" scoped>

</style>