<template>
  <v-card
    hover="true"
    class="mx-auto"
    max-width="344"
  >
    <v-row>
      <v-col>
        <v-img class="mx-auto"
          :src="bankLogo"
          max-height="60"
          max-width="60"
        ></v-img>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col class="d-flex justify-center">
        <v-card-title class="to-detail" @click="goProductDetail()">
          {{ product.fin_prdt_nm }}
        </v-card-title>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="6">
        <v-card-subtitle class="text-center py-0 my-0">
          <v-btn
            icon
            elevation="1"
            class="mb-2"
            color="yellow lighten-1"
            v-if="likeFlag"
            @click="likeProduct()"
          >
            <v-icon>mdi-star</v-icon>
          </v-btn>
          <v-btn
            icon
            elevation="1"
            class="mb-2"
            v-if="!likeFlag"
            @click="likeProduct()"
          >
            <v-icon>mdi-star-outline</v-icon>
          </v-btn>
        </v-card-subtitle>
      </v-col>
      <v-col cols="6">
        <v-card-subtitle class="text-center py-0 my-0">
          <v-btn
            icon
            color="indigo"
            elevation="1"
            class="mb-2"
            v-if="joinFlag"
            @click="joinProduct()"
          >
            <v-icon>mdi-bank-check</v-icon>
          </v-btn>
          <v-btn
            icon
            elevation="1"
            class="mb-2"
            v-if="!joinFlag"
            @click="joinProduct()"
          >
            <v-icon>mdi-bank-plus</v-icon>
          </v-btn>
        </v-card-subtitle>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'LikeProductItem',
  data() {
    return {
      likeFlag: true,
      joinFlag: true,
    }
  },
  props: {
    product: Object,
    type: String,
  },
  computed: {
    ...mapGetters([ 'maxSortedDeposits', 'maxSortedInstallments' ]),
    finPrdtCd() {
      return this.product.fin_prdt_cd
    },
    bankLogo() {
      const bankImgUrlObj = this.$store.state.finlife.bankImgUrl
      const bank = this.product.kor_co_nm
      return bankImgUrlObj[bank] ? bankImgUrlObj[bank] : ''
    },
    likeCount() {
      if (this.type === 'deposit') {
        return this.product.like_deposit_count
      } else {
        return this.product.like_saving_count
      }
    },
    joinCount() {
      if (this.type === 'deposit') {
        return this.product.register_deposit_count
      } else {
        return this.product.registered_saving_count
      }
    },
  },
  methods: {
    likeProduct() {
      if (this.type === 'deposit') {
        this.$store.dispatch('likeDeposit', this.finPrdtCd)
        .then(() => {
          this.likeFlag = !this.likeFlag
        })
        .catch((error) => {
          console.log(error)
        })
      } else {
        this.$store.dispatch('likeInstallment', this.finPrdtCd)
        .then(() => {
          this.likeFlag = !this.likeFlag
        })
        .catch((error) => {
          console.log(error)
        })
      }
    },
    joinProduct() {
      if (this.type === 'deposit') {
        this.$store.dispatch('joinDeposit', this.finPrdtCd)
        .then(() => {
          this.joinFlag = !this.joinFlag
        })
        .catch((error) => {
          console.log(error)
        })
      } else {
        this.$store.dispatch('joinInstallment', this.finPrdtCd)
        .then(() => {
          this.joinFlag = !this.joinFlag
        })
        .catch((error) => {
          console.log(error)
        })
      }
    },
    goProductDetail() {
      if (this.type === 'deposit') {
        this.$router.push({
          name: 'DepositDetailView',
          params: {
            'finPrdtCd': this.finPrdtCd
          }
        })
      } else {
        this.$router.push({
          name: 'InstallmentDetailView',
          params: {
            'finPrdtCd': this.finPrdtCd
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.to-detail {
  cursor: pointer;
}
</style>