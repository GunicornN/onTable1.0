<template>

    <div>

      <div id="input-container">
        <input v-model="query" v-on:change="getSearchResults" type="text" placeholder="Chercher un Restaurant, Bar, ...">

      </div>

      <div id="box-results">
        {{ searchResults }}
        <ul>
          <li v-for="company in searchResults" v-bind:key="company.slug">
            <div>
                {{company.name}}
                {{company.address1}}
                {{company.city}}
                {{company.zip_code}}
                {{company.country}}
            </div>
          </li>
        </ul>


      </div>
    </div>

</template>

<script>
import axios from 'axios'

let api_address  = "http://0.0.0.0/api/"

export default {
  name: 'SearchBar',
  data(){
    return {
        searchResults: [],
        query: "",
        api_address: process.env.APP_ROOT_API
    }
  },
  methods:{
    getSearchResults: function(){
      console.log(this.query)
      let endpoint = api_address+"companies/?search="+this.query
      console.log(endpoint)
      axios
      .get(endpoint)
      .then(response => (this.searchResults = response.data.results))    

    }
  }
}
</script>

<style scoped>
  .input-container {
    border-radius: 5px;
    background: #677482;
    padding: 10px;
  }

.input-container input {
	border: none;
	background: transparent;
	color: white;
	padding: 6px 15px;
	font-size: 18px;
}


</style>