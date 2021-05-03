<template>
  <body>
    Test
      <Head/>
      
      <BodyHomePage/>
      <Footer/>
  </body>
</template>

<script>

import BodyHomePage from '@/components/Home/Body.vue'
import Head from '@/components/main/Head.vue'
import Footer from '@/components/main/Footer.vue'

export default {
  name: 'Home',
  components: {
    Head,
    Footer,
    BodyHomePage
  }
}
</script>
