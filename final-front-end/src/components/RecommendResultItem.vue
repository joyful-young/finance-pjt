<template>
  <v-col cols="4">
    <v-card
      hover="true"
      class="mx-auto my-3"
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
          <v-card-title class="to-detail">
            {{ productName }}
          </v-card-title>
        </v-col>
      </v-row>
    </v-card>
  </v-col>
</template>

<script>

export default {
  name: 'RecommendResultItem',
  data() {
    return {
      
    }
  },
  props: {
    productName: String,
    productBank: String,
  },
  computed: {
    // finPrdtCd() {
    //   return this.product.fin_prdt_cd
    // },
    bankLogo() {
      const bankImgUrlObj = this.$store.state.finlife.bankImgUrl
      // const bank = this.product.kor_co_nm
      const bank = this.productBank
      return bankImgUrlObj[bank] ? bankImgUrlObj[bank] : ''
    },
  },
  methods: {
    // goProductDetail() {
    //   if (this.type === 'deposit') {
    //     this.$router.push({
    //       name: 'DepositDetailView',
    //       params: {
    //         'finPrdtCd': this.finPrdtCd
    //       }
    //     })
    //   } else {
    //     this.$router.push({
    //       name: 'InstallmentDetailView',
    //       params: {
    //         'finPrdtCd': this.finPrdtCd
    //       }
    //     })
    //   }
    // }
  }
}
</script>

<style scoped>

</style>