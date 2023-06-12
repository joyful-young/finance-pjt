<template>
  <v-card
  >

    <v-card-title>{{ result }}</v-card-title>

    <div v-if="products">

      <v-container>
        <v-row>
          <RecommendResultItem v-for="(product, index) in products" :key="index"
          :productName="products[index][1]"
          :productBank="products[index][3]"
          />
        </v-row>
      </v-container>
    </div>
  </v-card>
</template>

<script>
import api from '@/api'
import axios from 'axios'
import { mapGetters } from 'vuex'
import RecommendResultItem from '@/components/RecommendResultItem.vue'

export default {
  name: 'RecommendResult',
  data() {
    return {
      result: '',
      products: [],
      deposits: [],
      installments: [],
    }
  },
  components: {
    RecommendResultItem,
  },
  props: {
    // loan_amount, bond_amount, stock_amount
    differenceField: String,
  },
  created() {
    if (this.differenceField === 'loan_amount') {
      this.result = '대출입니다. 대출은 자산 증식을 위한 전략적인 선택입니다.'
      return
    } else if (this.differenceField === 'bond_amount') {
      this.result = '채권입니다.'
      return
    } else if (this.differenceField ==='stock_amount') {
      this.result = '주식입니다.'
      return
    } else {
      this.result = '현금성 자산입니다.'
      const wantRecomment = confirm('현금성 자산입니다. 추천받으시겠습니까?')
      if (wantRecomment) {
        this.sendRequest()
      }
    }
  },
  computed: {
    ...mapGetters(['authHeader', 'maxSortedDeposits',]),
    productsNameList() {
      return this.products.map((product) => {
        return product[1]
      })
    },
    productsBankList() {
      return this.products.map((product) => {
        return product[3]
      })
    },
    recommendedProducts() {
      return this.deposits.map((deposit) => {
        return this.productsNameList.includes(deposit.fin_prdt_nm)
      })
    }
  },
  methods: {
    async sendRequest() {
      try {
        const response = await axios({
          method: 'GET',
          url: api.becomesuperrich.hybrid_recommendation(),
          headers: this.authHeader,
        })
        console.log(response)
        this.products = response.data.final_recommendation
        
        const depositResponse = await this.$store.dispatch('getDepositsPromise')

        const deposits = depositResponse
        this.deposits = deposits
        console.log(this.products) // id, fin_prdt_nm, fin_prdt_cd
        console.log(this.deposits, 'deposit')
      } catch (error) {
        console.log(error)
      }
    },
    
  }
}
</script>

<style>

</style>