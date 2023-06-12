<template>
  <v-container>
    <!-- 옵션이다 -->
    {{ installment.saving_options }}
    <v-row class="align-center text-center">
      <v-col>
        <v-img :src="bankLogo" alt=""
          max-height="100"
          max-width="100"
        ></v-img>
      </v-col>
      <v-col>
        <p>{{ installment.kor_co_nm }}</p>
        <router-link :to="{
          name: 'InstallmentDetailView',
          params: {
            'finPrdtCd': installment.fin_prdt_cd
          }
        }">
          <!-- 금융 상품명. 클릭하면 detail로 연결 -->
          {{ installment.fin_prdt_nm }}
        </router-link>
        <!-- <div v-if="selectedOption === 'maxIntrRate'">
          <p>최고 금리 : {{ maxIntrRate }} %</p>
          <p>기본 금리 : {{ minIntrRate }} %</p>
        </div>
        <div v-else>
          <p>기본 금리 : {{ minIntrRate }} %</p>
          <p>최고 금리 : {{ maxIntrRate }} %</p>
        </div> -->
      </v-col>

      <v-col>
        <v-btn @click="likeInstallment(installment.fin_prdt_cd)">{{ likeBtn }}</v-btn>
        <v-btn @click="joinInstallment(installment.fin_prdt_cd)">{{ joinBtn }}</v-btn>
      </v-col>
    </v-row>

    <hr>
    <!-- 가입 제한 같은 거 표시해주는 게 좋을까 -->
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'InstallmentListItem',
  data() {
    return {
      likeFlag: false,
      joinFlag: false,
    }
  },
  props: {
    installment: Object,
    selectedOption: String,
  },
  computed: {
    ...mapGetters(['currentUser', 'isLoggedIn']),
    bankLogo() {
      const bankImgUrlObj = this.$store.state.finlife.bankImgUrl
      const bank = this.installment.kor_co_nm
      return bankImgUrlObj[bank] ? bankImgUrlObj[bank] : ''
    },
    likeBtn() {
      return this.likeFlag ? '찜 해제' : '찜'
    },
    joinBtn() {
      return this.joinFlag ? '해지' : '가입'
    },
    // 기본 금리
    // minIntrRate() {
    //   return Math.min(...this.installment.options.map((option) => {
    //     return option.intr_rate
    //   }))
    // },
    // // 최고 금리
    // maxIntrRate() {
    //   return Math.max(...this.installment.options.map((option) => {
    //     return option.intr_rate2
    //   }))
    // },
  },
  created() {
    // 로그인한 유저이면 상품 좋아요했는지, 가입했는지 판단
    if (this.isLoggedIn) {
      // 좋아요 했는가?
      if (this.installment.like_saving.includes(this.currentUser.pk)) {
        this.likeFlag = true
      } else {
        this.likeFlag = false
      }
      // 가입했는가?
      if (this.installment.registered_saving.includes(this.currentUser.pk)) {
        this.joinFlag = true
      } else {
        this.joinFlag = false
      }
    } else {    // 로그인 안한 유저이면 둘 다 false
      this.likeFlag = false
      this.joinFlag = false
    }
  },
  methods: {
    // 적금 좋아요
    likeInstallment(finPrdtCd) {
      if (this.isLoggedIn) {
        this.$store.dispatch('likeInstallment', finPrdtCd)
        .then(() => {
          if (this.likeFlag) {
            this.likeFlag = false
          } else {
            this.likeFlag = true
          }
        })
        .catch((error) => {
          console.log(error)
        })
      } else {
        const wantLogin = confirm('로그인이 필요합니다. 로그인하시겠습니까?')
        if (wantLogin) {
          this.$router.push('/login')
        }
      }
    },
    // 적금 가입
    joinInstallment(finPrdtCd) {
      if (this.isLoggedIn) {
        this.$store.dispatch('joinInstallment', finPrdtCd)
        .then(() => {
          if (this.joinFlag) {
            this.joinFlag = false
          } else {
            this.joinFlag = true
          }
        })
        .catch((error) => {
          console.log(error)
        })
      } else {
        const wantLogin = confirm('로그인이 필요합니다. 로그인하시겠습니까?')
        if (wantLogin) {
          this.$router.push('/login')
        }
      }
    },
  }
}
</script>

<style>

</style>