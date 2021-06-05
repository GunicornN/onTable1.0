<template>
  <div id="app">
    <nav>
      <router-link :to="{name: 'Order',params:{ company_slug: 'le-coq-69006'}}">Order</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
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
