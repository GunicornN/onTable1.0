import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    order: {}, // TODO
    table_number: 0, // TODO
    payment_method : "", // TODO
    person_name : "", // TODO
    company_slug : "", // TODO
    products : [],
    products_quantiy : [],
    formulas : [],
    current_step: 0,
  },
  mutations: {
    addNewProduct(state,{product_slug,quantity}){
      //console.log(typeof(quantity))
      //console.log("test :",Number.isInteger(quantity))
      quantity = parseInt(quantity)

      // modifier le quantité si le produit est déjà présent 
      var index_product = state.products.indexOf(product_slug)
      console.log("index_product :",index_product)
      if( index_product >= 0){
        state.products_quantiy[index_product] = parseInt(quantity)
      }
      else {
        if (Number.isInteger(quantity)){ // on vérifie que la quantité est un nbr
          state.products.push(product_slug) // on ajoute au tableau de produits
          state.products_quantiy.push(quantity) // on ajoute la quantité au tab products_quantiy
        }
      }
    },
    removeProduct(state,index_product){
      if (Number.isInteger(index_product)){ // on vérifie que la quantité est un nbr
        state.products.splice(index_product,1) // on enleve 1 élement à l'index du produit
        state.products_quantiy.splice(index_product,1) // on enleve 1 élement à l'index des quantités
      }
    },
    setPaymentMethod(state,payment_method){
      // TODO - : verifier si la valeur est correcte
      state.payment_method = payment_method
    },
    setPersonName(state,person_name){
      state.person_name = person_name
    },
    setCompanySlug(state,company_slug){
      state.company_slug = company_slug
    },
    setCurrentStep(state,step){
      state.current_step = step
    }

  },
  actions : {
    // les mutations permettent de changer la valeur du state
    updateProductToOrder({commit},{product_slug,quantity}){
      //console.log("ajout de :",quantity," ",product_slug)
      commit('addNewProduct',{product_slug,quantity})
    },
    removeProductFromOrder({commit},index_product){
      commit('removeProduct',index_product)

    },
    updatePaymentMethod({commit},payment_method){
      commit('setPaymentMethod',payment_method)
    },
    updatePersonName({commit},person_name){
      commit('setPersonName',person_name)
    },
    updateCompanySlug({commit},company_slug){
      commit('setCompanySlug',company_slug)
    },
    updateCurrentStep({commit},step){
      commit('setCurrentStep',step)
    },
    // Other methods 
    sendOrder(){
      //var new_products = [{}]
    }
  },
  getters: {
    getOrder(state){
      return state;
    },
    getCurrentStep(state){
      return state.current_step
    },
    getPaymentMethod(state){
      return state.payment_method
    },
    getProducts(state){
      // TODO : RECUPERER TOUS LES products ainsi que quantités 
      const json = []
      for(var i=0;i<state.products.length;i++){
        var details = {
          "product": state.products[i],
          "quantity": state.products_quantiy[i]
        }
        json.push(details)
      }
      //console.log(json)
      // on parse l'objet avant de le retourner
      return json
    },
    getProductIndex(state,product_slug){
      for(var i=0;i<state.products.length;i++){
        if (product_slug == state.products[i]){
          return i
        }
      }
    }
  },

})


// Créer l'extension pour la partie Recherche,...