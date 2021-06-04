<template>
    <div>
        Valider 

        <div class="order-recap">
            <OrderRecap/>
        </div>

        <div class="total">
            Total de la commande : {{ total }}€
        </div>

        <button>Valider votre commande</button>
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
    }
}
</script>