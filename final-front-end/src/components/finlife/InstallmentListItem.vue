<template>
  <v-container class="installment-item">
    <v-row class="align-center">
      <v-col cols="3" md="2" class="d-flex justify-center">
        <v-img :src="bankLogo" alt="Bank Logo" max-height="60" max-width="60"></v-img>
      </v-col>
      <v-col cols="9" md="4" class="text-center">
        <p class="kor-co-nm">{{ installment.kor_co_nm }}</p>
        <router-link :to="{
          name: 'InstallmentDetailView',
          params: {
            'finPrdtCd': installment.fin_prdt_cd
          }
        }">
          <h2 class="fin-prdt-nm">{{ installment.fin_prdt_nm }}</h2>
        </router-link>
      </v-col>
      <v-col cols="8" md="4" class="text-center">
        <p class="rate-info">최고 금리 {{ maxIntrRate }}% | 기본 금리 {{ minIntrRate }}%</p>
      </v-col>
      <v-col cols="4" md="2" class="text-center">
        <v-row>
          <v-col cols="12">
            <v-btn @click="likeInstallment(installment.fin_prdt_cd)" 
            :color="likeFlag ? 'primary' : 'gray'"
            class="ma-1">
              <v-icon left>{{ likeBtn }}</v-icon>
              {{ likeCount }}
            </v-btn>
          </v-col>
          <v-col cols="12">
            <v-btn @click="joinInstallment(installment.fin_prdt_cd)" 
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
  name: 'InstallmentListItem',
  data() {
    return {
      likeFlag: false,
      joinFlag: false,
      likeCount: '',
      joinCount: '',
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
      return this.likeFlag ? 'mdi-star' : 'mdi-star-outline'
    },
    joinBtn() {
      return this.joinFlag ? 'mdi-bank-check' : 'mdi-bank-plus'
    },
    // 기본 금리
    minIntrRate() {
      return Math.min(...this.installment.saving_options.map((option) => {
        return option.intr_rate
      })).toFixed(2)
    },
    // 최고 금리
    maxIntrRate() {
      return Math.max(...this.installment.saving_options.map((option) => {
        return option.intr_rate2
      })).toFixed(2)
    },
  },
  created() {
    if (this.isLoggedIn) {
      if (this.installment.like_saving.includes(this.currentUser.pk)) {
        this.likeFlag = true
      } else {
        this.likeFlag = false
      }

      if (this.installment.registered_saving.includes(this.currentUser.pk)) {
        this.joinFlag = true
      } else {
        this.joinFlag = false
      }
    } else {
      this.likeFlag = false
      this.joinFlag = false
    }
    this.likeCount = this.installment.like_saving_count
    this.joinCount = this.installment.registered_saving_count
  },
  methods: {
    likeInstallment(finPrdtCd) {
      if (this.isLoggedIn) {
        this.$store.dispatch('likeInstallment', finPrdtCd)
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
    joinInstallment(finPrdtCd) {
      if (this.isLoggedIn) {
        this.$store.dispatch('joinInstallment', finPrdtCd)
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
  },
}
</script>

<style scoped>
.installment-item {
  margin-bottom: 20px;
}

.kor-co-nm {
  font-size: 14px;
  margin-top: 6px;
}

.fin-prdt-nm {
  font-size: 18px;
  margin: 10px 0;
}

.rate-info {
  font-size: 14px;
  margin-top: 6px;
}

.divider {
  margin-top: 20px;
}
</style>
