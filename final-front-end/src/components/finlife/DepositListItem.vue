<template>
  <v-container class="deposit-item">
    <v-row class="align-center">
      <v-col cols="3" md="2" class="d-flex justify-center">
        <v-img :src="bankLogo" alt="Bank Logo" max-height="60" max-width="60"></v-img>
      </v-col>
      <v-col cols="9" md="4" class="text-center">
        <p class="kor-co-nm">{{ deposit.kor_co_nm }}</p>
        <router-link :to="{
          name: 'DepositDetailView',
          params: {
            'finPrdtCd': deposit.fin_prdt_cd
          }
        }">
          <h2 class="fin-prdt-nm">{{ deposit.fin_prdt_nm }}</h2>
        </router-link>
      </v-col>
      <v-col cols="8" md="4" class="text-center">
        <p class="rate-info">최고 금리 {{ maxIntrRate }}% | 기본 금리 {{ minIntrRate }}%</p>
      </v-col>
      <v-col cols="4" md="2" class="text-center">
        <v-row>
          <v-col cols="12">
            <v-btn @click="likeDeposit(deposit.fin_prdt_cd)" 
            :color="likeFlag ? 'primary' : 'gray'"
            class="ma-1">
              <v-icon left>{{ likeBtn }}</v-icon>
              {{ likeCount }}
            </v-btn>
          </v-col>
          <v-col cols="12">
            <v-btn @click="joinDeposit(deposit.fin_prdt_cd)" 
            :color="joinFlag ? 'primary' : 'gray'"
            class="ma-1">
              <v-icon left>{{ joinBtn }}</v-icon>
              {{ joinCount }}
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-divider class="divider"></v-divider>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'DepositListItemGPT',
  data() {
    return {
      likeFlag: false,
      joinFlag: false,
      likeCount: '',
      joinCount: '',
    }
  },
  props: {
    deposit: Object,
    selectedOption: String,
  },
  computed: {
    ...mapGetters(['currentUser', 'isLoggedIn']),
    bankLogo() {
      const bankImgUrlObj = this.$store.state.finlife.bankImgUrl
      const bank = this.deposit.kor_co_nm
      return bankImgUrlObj[bank] ? bankImgUrlObj[bank] : ''
    },
    likeBtn() {
      return this.likeFlag ? 'mdi-star' : 'mdi-star-outline'
    },
    joinBtn() {
      return this.joinFlag ? 'mdi-bank-check' : 'mdi-bank-plus'
    },
    // 기본 금리
    minIntrRate() {
      return Math.min(...this.deposit.options.map((option) => {
        return option.intr_rate
      })).toFixed(2)
    },
    // 최고 금리
    maxIntrRate() {
      return Math.max(...this.deposit.options.map((option) => {
        return option.intr_rate2
      })).toFixed(2)
    },
  },
  created() {
    // 로그인한 유저이면 상품 좋아요했는지, 가입했는지 판단
    if (this.isLoggedIn) {
      // 좋아요 했는가?
      if (this.deposit.like_deposit.includes(this.currentUser.pk)) {
        this.likeFlag = true
      } else {
        this.likeFlag = false
      }
      // 가입했는가?
      if (this.deposit.register_deposit.includes(this.currentUser.pk)) {
        this.joinFlag = true
      } else {
        this.joinFlag = false
      }
    } else {    // 로그인 안한 유저이면 둘 다 false
      this.likeFlag = false
      this.joinFlag = false
    }

    // 좋아요 수, 가입자 수 받아놓기
    this.likeCount = this.deposit.like_deposit_count
    this.joinCount = this.deposit.register_deposit_count
  },
  methods: {
    // 예금 좋아요
    likeDeposit(finPrdtCd) {
      if (this.isLoggedIn) {
        this.$store.dispatch('likeDeposit', finPrdtCd)
        .then(() => {
          if (this.likeFlag) {
            this.likeFlag = false
            this.likeCount -= 1
          } else {
            this.likeFlag = true
            this.likeCount += 1
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
    // 예금 가입
    joinDeposit(finPrdtCd) {
      if (this.isLoggedIn) {
        this.$store.dispatch('joinDeposit', finPrdtCd)
        .then(() => {
          if (this.joinFlag) {
            this.joinFlag = false
            this.joinCount -= 1
          } else {
            this.joinFlag = true
            this.joinCount += 1
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

<style scoped>
.deposit-item {
  padding: 20px;
}

.kor-co-nm {
  margin-top: 0;
  margin-bottom: 5px;
  font-size: 14px;
}

.fin-prdt-nm {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: bold;
}

.rate-info {
  margin-top: 0;
  margin-bottom: 5px;
  /* font-size: 14px; */
  font-size: 16px;
}

.text-center {
  text-align: center;
}

/* .action-button {
  margin-top: 5px;
  margin-bottom: 5px;
} */

.divider {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>