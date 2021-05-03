
import axios from 'axios';

class Company {
    constructor(slug){
        axios.get(`http://jsonplaceholder.typicode.com/posts`)
        .then(response => {
          // JSON responses are automatically parsed.
          this.name = response.name
          this.address1 = response.address1
          this.address2 = response.address2
          this.city = response.city
          this.country = response.country
          this.zip_code = response.zip_code
          this.company_code = response.company_code
          this.types = response.types
          this.slug = slug 
        })
        .catch(e => {
          this.errors.push(e)
        })
    }

    cards(){
        axios.get(`http://jsonplaceholder.typicode.com/posts`)
        .then(response => {
          // JSON responses are automatically parsed.
            
        })
        .catch(e => {
          this.errors.push(e)
        })       
    }
}
