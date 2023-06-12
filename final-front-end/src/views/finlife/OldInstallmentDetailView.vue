<template>
  <div>
    <h3>Installment Detail View</h3>
    <div v-if="installment">
      {{ installment }}
      <h5>{{ installment.fin_prdt_nm }}</h5>
      <p>{{ installment.etc_note }}</p>
      <p>가입 대상 : {{ installment.join_member }}</p>
      <p>가입 방법 : {{ installment.join_way }}</p>
      <p>우대 조건 : {{ installment.spcl_cnd }}</p>
    </div>
    <div v-else>
      <p>로딩중...</p>
    </div>
  </div>
</template>

<script>
import api from '@/api'
import axios from 'axios'
import { mapGetters } from 'vuex'


export default {
  name: 'InstallmentDetailView',
  data() {
    return {
      installment: null,
    }
  },
  computed: {
    ...mapGetters([ 'isLoggedIn', 'currentUser' ]),
    finPrdtCd() {
      return this.$route.params.finPrdtCd
    },
  },
  // 서버 상세조회 api 필요
  created() {
    this.getInstallmentDetail(this.finPrdtCd)
  },
  methods: {
    getInstallmentDetail(finPrdtCd) {

      axios.get(api.installments.installmentDetail(finPrdtCd))
      .then((response) => {
        console.log(response)
        this.installment = response.data
      })
      .catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style>

</style>