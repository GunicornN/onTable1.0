<template>
  <div id="app">
    <OrderView/>
  </div>
</template>

<script>
import OrderView from '@/views/OrderView.vue'

export default {
  name: 'App',
  components: {
    OrderView
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
