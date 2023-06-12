import axios from 'axios'
import api from '@/api'

export default {
  state: {
    bankImgUrl: {
      // "KDB산업은행": "https://cdn.banksalad.com/graphic/color/logo/circle/kdb.png?w=48&q=75",
      "한국산업은행": "https://cdn.banksalad.com/graphic/color/logo/circle/kdb.png?w=48&q=75",
      // "SC제일은행": "https://cdn.banksalad.com/graphic/color/logo/circle/sc.png?w=48&q=75",
      "한국스탠다드차타드은행": "https://cdn.banksalad.com/graphic/color/logo/circle/sc.png?w=48&q=75",
      "경남은행": "https://cdn.banksalad.com/graphic/color/logo/circle/bnk-kyongnam.png?w=48&q=75",
      "광주은행": "https://cdn.banksalad.com/graphic/color/logo/circle/knj.png?w=48&q=75",
      "국민은행": "https://cdn.banksalad.com/graphic/color/logo/circle/kb.png?w=48&q=75",
      // "기업은행": "https://cdn.banksalad.com/graphic/color/logo/circle/ibk.png?w=48&q=75",
      "중소기업은행": "https://cdn.banksalad.com/graphic/color/logo/circle/ibk.png?w=48&q=75",
      // "농협은행": "https://cdn.banksalad.com/graphic/color/logo/circle/nh.png?w=48&q=75",
      "농협은행주식회사": "https://cdn.banksalad.com/graphic/color/logo/circle/nh.png?w=48&q=75",
      "대구은행": "https://cdn.banksalad.com/graphic/color/logo/circle/dgb.png?w=48&q=75",
      "부산은행": "https://cdn.banksalad.com/graphic/color/logo/circle/bnk.png?w=48&q=75",
      "수협은행": "https://cdn.banksalad.com/graphic/color/logo/circle/suhyup.png?w=48&q=75",
      "신한은행": "https://cdn.banksalad.com/graphic/color/logo/circle/shinhan.png?w=48&q=75",
      "씨티은행": "https://cdn.banksalad.com/graphic/color/logo/circle/citi.png?w=48&q=75",
      "우리은행": "https://cdn.banksalad.com/graphic/color/logo/circle/woori.png?w=48&q=75",
      "우체국": "https://cdn.banksalad.com/graphic/color/logo/circle/post.png?w=48&q=75",
      "전북은행": "https://cdn.banksalad.com/graphic/color/logo/circle/knj.png?w=48&q=75",
      "제주은행": "https://cdn.banksalad.com/graphic/color/logo/circle/shinhan.png?w=48&q=75",
      // "카카오뱅크": "https://cdn.banksalad.com/graphic/color/logo/circle/kakaobank.png?w=48&q=75",
      "주식회사 카카오뱅크": "https://cdn.banksalad.com/graphic/color/logo/circle/kakaobank.png?w=48&q=75",
      // "케이뱅크": "https://cdn.banksalad.com/graphic/color/logo/circle/kbank.png?w=48&q=75",
      "주식회사 케이뱅크": "https://cdn.banksalad.com/graphic/color/logo/circle/kbank.png?w=48&q=75",
      // "토스뱅크": "https://cdn.banksalad.com/graphic/color/logo/circle/toss.png?w=48&q=75",
      "토스뱅크 주식회사": "https://cdn.banksalad.com/graphic/color/logo/circle/toss.png?w=48&q=75",
      "하나은행": "https://cdn.banksalad.com/graphic/color/logo/circle/keb.png?w=48&q=75"
    },    
    deposits: [],
    maxSortedDeposits: [],
    sortedDeposits: [],
    depositDetail: {},
    installments: [],
    maxSortedInstallments: [],
    sortedInstallments: [],
    installmentDetail: {},
  },
  getters: {
    maxSortedDeposits(state) {
      return state.maxSortedDeposits
    },
    sortedDeposits(state) {
      return state.sortedDeposits
    },
    maxSortedInstallments(state) {
      return state.maxSortedInstallments
    },
    sortedInstallments(state) {
      return state.sortedInstallments
    }
  },
  mutations: {
    // 예금 데이터 저장
    SET_DEPOSITS(state, deposits) {
      state.deposits = deposits
      console.log(deposits, '예금 저장')
    },
    // 최고금리순 예금 데이터 저장
    SET_SORTED_BY_MAX_DEPOSITS(state, deposits) {
      state.maxSortedDeposits = deposits
      console.log(deposits, '맞는지 확인')
    },
    // 기본금리순 예금 데이터 저장
    SET_SORTED_DEPOSITS(state, deposits) {
      state.sortedDeposits = deposits
      console.log(deposits, '저장')
    },
    // 예금 상세 데이터 저장
    SET_DEPOSIT_DETAIL(state, deposit) {
      state.depositDetail = deposit
      console.log(deposit, 'detail 예금 저장')
    },
    // 적금 데이터 저장
    SET_INSTALLMENTS(state, installments) {
      state.installments = installments
    },
    // 최고금리순 적금 데이터 저장
    SET_SORTED_BY_MAX_INSTALLMENTS(state, installments) {
      state.maxSortedInstallments = installments
    },
    // 기본금리순 적금 데이터 저장
    SET_SORTED_INSTALLMENTS(state, installments) {
      state.sortedInstallments = installments
    },
    // 적금 상세 데이터 저장
    SET_INSTALLMENT_DETAIL(state, installment) {
      state.installmentDetail = installment
      console.log(installment, 'detail 적금 저장')
    }
  },
  actions: {
    // 전체 예금 목록 조회
    getDeposits(context) {
      axios.get(api.deposits.depositsList())
      .then((response) => {
        console.log(response)
        context.commit('SET_DEPOSITS', response.data)
      })
      .catch((error) => {
        console.log('getDeposits action 에러', error)
      })
    },
    // 최고금리순 예금 목록 조회
    async getDepositsPromise(context) {
      try {
        const response = axios({
          method: 'GET',
          url: api.deposits.maxDepositList(),
        })
        console.log(response, '액션 응답')
        context.commit('SET_SORTED_BY_MAX_DEPOSITS', response.data)
        return response
      } catch (error) {
        console.log(error)
        return error
      }
    },
    getSortedByMaxDeposits(context) {
      axios.get(api.deposits.maxSortedDepositList())
      .then((response) => {
        console.log(response, '최고금리순')
        context.commit('SET_SORTED_BY_MAX_DEPOSITS', response.data)
      })
      .catch((error) => {
        console.log(error)
      })
    },
    getSortedDeposits(context) {
      axios.get(api.deposits.sortedDepositList())
      .then((response) => {
        console.log('기본금리순', response)
        context.commit('SET_SORTED_DEPOSITS', response.data)
      })
      .catch((error) => {
        console.log(error)
      })
    },
    getDepositDetail(context, finPrdtCd) {
      const request = {
        method: 'GET',
        url: api.deposits.depositDetail(finPrdtCd),
      }

      if (context.getters.isLoggedIn) {
        request['headers'] = context.getters.authHeader
      }

      return new Promise((resolve, reject) => {
        axios(request)
          .then((response) => {
            context.commit('SET_DEPOSIT_DETAIL', response.data)
            resolve(response.data)
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
    // 예금 좋아요
    async likeDeposit({ getters }, finPrdtCd) {
      try {
        const response = await axios({
          method: 'POST',
          url: api.deposits.depositLike(finPrdtCd),
          headers: getters.authHeader
        })
        return response
      } catch (error) {
        console.log(error)
        return error
      }
    },
    // 예금 가입 / 해지
    async joinDeposit({ getters }, finPrdtCd) {
      try {
        const response = await axios({
          method: 'POST',
          url: api.deposits.depositJoin(finPrdtCd),
          headers: getters.authHeader
        })
        return response
      } catch (error) {
        return error
      }
    },
    // 전체 적금 목록 조회
    getInstallments(context) {
      axios.get(api.installments.installmentsList())
      .then((response) => {
        console.log(response)
        context.commit('SET_INSTALLMENTS', response.data)
      })
      .catch((error) => {
        console.log('getInstallments action 에러', error)
      })
    },
    // 적금 최고금리순 조회
    getSortedByMaxInstallments(context) {
      axios.get(api.installments.maxSortedInstallmentList())
      .then((response) => {
        console.log(response, '액션 응답')
        context.commit('SET_SORTED_BY_MAX_INSTALLMENTS', response.data)
      })
      .catch((error) => {
        console.log(error)
      })
    },
    // 적금 기본금리순 조회
    getSortedInstallments(context) {
      axios.get(api.installments.sortedInstallmentList())
      .then((response) => {
        console.log('기본금리순', response)
        context.commit('SET_SORTED_INSTALLMENTS', response.data)
      })
      .catch((error) => {
        console.log(error)
      })
    },
    // 적금 상세 조회
    getInstallmentDetail(context, finPrdtCd) {
      const request = {
        method: 'GET',
        url: api.installments.installmentDetail(finPrdtCd),
      }

      if (context.getters.isLoggedIn) {
        request['headers'] = context.getters.authHeader
      }

      return new Promise((resolve, reject) => {
        axios(request)
          .then((response) => {
            context.commit('SET_INSTALLMENT_DETAIL', response.data)
            resolve(response.data)
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
    // getInstallmentDetail(context, finPrdtCd) {
    //   axios.get(api.installments.installmentDetail(finPrdtCd))
    //   .then((response) => {
    //     console.log(response)
    //     // response.data에 정보 잘 들어있는지 확인할 것!
    //     context.commit('SET_INSTALLMENT_DETAIL', response.data)
    //   })
    //   .catch((error) => {
    //     console.log('getInstallmentDetail action 에러', error)
    //   })
    // },
    // 적금 좋아요
    async likeInstallment({ getters }, finPrdtCd) {
      try {
        const response = await axios({
          method: 'POST',
          url: api.installments.installmentLike(finPrdtCd),
          headers: getters.authHeader
        })
        return response
      } catch (error) {
        console.log(error)
        return error
      }
    },
    // 적금 가입 / 해지
    async joinInstallment({ getters }, finPrdtCd) {
      try {
        const response = await axios({
          method: 'POST',
          url: api.installments.installmentJoin(finPrdtCd),
          headers: getters.authHeader
        })
        return response
      } catch (error) {
        return error
      }
    },
  },
}