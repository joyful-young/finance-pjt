import axios from 'axios'
import router from '@/router/index'
// import store from '@/store/index'
import api from '@/api'

export default {
  // namespaced: true,
  state: {
    token: localStorage.getItem('key') ? localStorage.getItem('key') : null,
    currentUser: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
  },
  getters: {
    currentUser(state) {
      return state.currentUser
    },
    // currentUsername(state, getters) {
    //   return getters.currentUser.username
    // },
    isLoggedIn(state) {
      return state.token ? true : false
    },
    authHeader(state) {
      return { Authorization: `Token ${state.token}` }
    }
  },
  mutations: {
    SAVE_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('key', token)
    },
    LOGOUT(state) {
      state.token = null
      state.currentUser = null
      localStorage.removeItem('key')
      localStorage.removeItem('user')
      console.log('로그아웃 성공')
      router.push({ name: 'login' })
    },
    SET_CURRENT_USER(state, user) {
      state.currentUser = user    // 객체로 저장
      const stringifiedUser = JSON.stringify(user)
      localStorage.setItem('user', stringifiedUser)
      console.log('유저 저장', user)
    },
  },
  actions: {
    async login({ commit, dispatch }, form) {
      try {
        const response = await axios({
          method: 'POST',
          url: api.accounts.login(),
          data: {
            ...form
          }
        })
        console.log('login', response)

        await commit('SAVE_TOKEN', response.data.key)
        await dispatch('getCurrentUser')

        return response
      } catch (error) {
        console.log(error)
        return error
      }
    },
    // login({ commit, dispatch }, form) {
    //   const username = form.username
    //   const password = form.password

    //   console.log('login url', api.accounts.login())
    //   axios({
    //     method: 'POST',
    //     url: api.accounts.login(),
    //     data: {
    //       username,
    //       password,
    //     }
    //   })
    //   .then((response) => {
    //     // 토큰 response.data.key 에 들어있음
    //     console.log('login action 요청 정상 응답', response.data)

    //     // const payload = {
    //     //   token: response.data.key,
    //     //   username: username,
    //     // }
    //     // 토큰 저장하고
    //     // commit('SAVE_TOKEN', payload)
    //     commit('SAVE_TOKEN', response.data.key)
    //     // 현재 유저 정보 받기
    //     dispatch('getCurrentUser')

    //     // // 로그인 성공 후 홈으로
    //     // router.push({ name: 'home'})
    //     // 로그인 성공 후 이전 페이지로
    //     router.go(-1)

    //     // const redirectPath = store.state.redirectPath || '/'
    //     // router.push(redirectPath)

    //     // context.commit('SET_REDIRECT_PATH', null)
    //   })
    //   .catch((error) => {
    //     console.log(error)
    //   })
    // },
    // async 이용해서 고치고 가입양식 페이지 빈칸으로 만들어놓기!!! 회원가입 완료 페이지로 이동?

    async signUp({ commit, dispatch }, form) {
      try {
        const response = await axios({
          method: 'POST',
          url: api.accounts.signUp(),
          data: {
            ...form
          }
        })

        await commit('SAVE_TOKEN', response.data.key)
        await dispatch('getCurrentUser')

        router.push({ name: 'home' })
      } catch (error) {
        console.log(error)
      }
    },


    // signUp(context, form) {
    //   console.log('signUp action 호출')
    //   console.log(form, 'form')

    //   // const username = form.username
    //   // const password1 = form.password1
    //   // const password2 = form.password2
    //   // const realname = form.realname
    //   // const email = form.email

    //   const request = {
    //     ...form
    //   }
    //   console.log(request, 'request')

    //   // 데이터 넣어서 회원가입 요청 보내야 함
    //   axios({
    //     method: 'POST',
    //     // url: `${context.rootState.BACKEND_URL}accounts/signup/`,
    //     url: api.accounts.signUp(),
    //     data: {
    //       // username,
    //       // password1,
    //       // password2,
    //       // realname,
    //       // email,
    //       ...form
    //     }
    //   })
    //   .then((response) => {
    //     // response.data.token에 토큰 들어있음
    //     console.log(response)
    //     console.log('signUp action axios 요청 정상 응답')

    //     context.commit('SAVE_TOKEN', response.data.key)
    //     context.dispatch('getCurrentUser')
    //     // 일단 home으로 보내놓고 나중에 회원가입완료 페이지 만들면 거기로 옮기기
    //     router.push({ name: 'home'})
    //   })
    //   .catch((error) => {
    //     console.log(error)
    //   })
    // },
    logout({ commit, getters }) {
      axios({
        method: 'POST',
        url: api.accounts.logout(),
        headers: getters.authHeader,
      })
      .then((response) => {
        console.log(response)
        commit('LOGOUT')
        alert('로그아웃 되었습니다.')
      })
      .catch((error) => {
        console.log(error)
      })
    },
    // 현재 유저 확인
    // getCurrentUser(context, token) {
    //   // 요청 보내기
    //   return new Promise((resolve, reject) => {
    //     const request = {
    //       method: 'GET',
    //       url: api.accounts.currentUser(),
    //     }
        
    //     console.log(context)

    //     request['headers'] = { Authorization: `Token ${token}` }
        
    //     console.log('request', request)
    //     // axios({
    //     //   method: 'GET',
    //     //   url: api.accounts.currentUser(),
    //     //   headers: {
    //     //     Authorization: `Token ${context.state.token}`
    //     //   }
    //     // })
    //     axios(request)
    //     .then((response) => {
    //       // response.data.username 에 아이디 들어있음
    //       resolve(response)
    //     })
    //     .catch((error) => {
    //       reject(error)
    //     })
    //   })
    // }
    // 현재 유저 확인
    // getCurrentUser(context) {
    //   axios({
    //     method: 'GET',
    //     url: api.accounts.currentUser(),
    //     headers: context.getters.authHeader
    //   })
    //   .then((response) => {
    //     context.commit('SET_CURRENT_USER', response.data.pk)
    //     return new Promise((resolve, reject) => {
    //       resolve(response)
    //     })
    //   })
    //   .catch((error) => {
    //     console.log(error)
    //     return new Promise((resolve, reject) => {
    //       reject(error)
    //     })
    //   })
    // },
    // getCurrentUser(context) {
    //   return new Promise((resolve, reject) => {
    //     axios({
    //       method: 'GET',
    //       url: api.accounts.currentUser(),
    //       headers: context.getters.authHeader
    //     })
    //       .then((response) => {
    //         context.commit('SET_CURRENT_USER', response.data.pk)
    //         console.log(response, '액션 response')
    //         resolve(response.data)
    //       })
    //       .catch((error) => {
    //         console.log(error)
    //         reject(error)
    //       })
    //   })
    // },
    // getCurrentUser({ getters, commit }) {
    //   return new Promise((resolve, reject) => {
    //     axios({
    //       method: 'GET',
    //       url: api.accounts.currentUser(),
    //       headers: getters.authHeader
    //     })
    //       .then((response) => {
    //         console.log(response, '유저다')
    //         commit('SET_CURRENT_USER', response.data.username)    // username 저장하자
    //         resolve(response.data)
    //       })
    //       .catch((error) => {
    //         console.log(error)
    //         reject(error)
    //       })
    //   })
    // },
    // user 객체로 저장하자
    getCurrentUser({ getters, commit }) {
      return new Promise((resolve, reject) => {
        axios({
          method: 'GET',
          url: api.accounts.currentUser(),
          headers: getters.authHeader
        })
          .then((response) => {
            console.log(response, '유저다')
            commit('SET_CURRENT_USER', response.data)
            resolve(response.data)
          })
          .catch((error) => {
            console.log(error)
            reject(error)
          })
      })
    },
    
  },
}