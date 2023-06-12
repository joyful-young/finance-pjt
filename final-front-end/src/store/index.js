import Vue from 'vue'
import Vuex from 'vuex'

import articles from './modules/articles'
import comments from './modules/comments'
import finlife from './modules/finlife'
import accounts from './modules/accounts'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // BACKEND_URL: 'http://127.0.0.1:8000/',
    BACKEND_URL: 'http://70.12.102.97:8000/',      // ssafy
    // BACKEND_URL: 'http://172.30.43.87:8000/',
    // BACKEND_URL: 'http://172.30.42.155:8000/',
    // BACKEND_URL: 'http://175.196.236.214:8000/',

    // redirectPath: null,
  },
  getters: {
    // 여기 이거 필요할까???????????
    token() {
      return localStorage.getItem('key') ? localStorage.getItem('key') : false
    }
  },
  mutations: {
    // SET_REDIRECT_PATH(state, path) {
    //   console.log('mutations', path)
    //   state.redirectPath = path
    // }
  },
  actions: {
    // setRedirectPath(context, path) {
    //   context.commit('SET_REDIRECT_PATH', path)
    // }
  },
  modules: {
    articles,
    comments,
    finlife,
    accounts,
  }
})
