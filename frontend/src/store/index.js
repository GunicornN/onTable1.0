import { createStore } from 'vuex'

export default createStore({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {}
  },
  mutations: {
    auth_request(state){
      state.status = 'loading'
      
    }
  },
  actions: {
  },
  modules: {
  }
})
