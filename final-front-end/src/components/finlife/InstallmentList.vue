<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="3">
        <v-btn-toggle v-model="selectedOption" 
          color="primary accent-3"
        >
          <v-btn value="maxIntrRate">
            최고금리순
          </v-btn>
          <v-btn value="intrRate">
            기본금리순
          </v-btn>
        </v-btn-toggle>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <v-row v-if="selectedOption === 'maxIntrRate' && maxSortedInstallments.length !== 0">
      <v-col>
        <InstallmentListItem
          v-for="installment in maxSortedInstallments"
          :key="installment.fin_prdt_cd"
          :selectedOption="selectedOption"
          :installment="installment"
        />
      </v-col>
    </v-row>
    <v-row v-else-if="selectedOption === 'intrRate' && sortedInstallments.length !== 0">
      <v-col>
        <InstallmentListItem
          v-for="installment in sortedInstallments" :key="installment.fin_prdt_cd"
          :selectedOption="selectedOption"
          :installment="installment"
        />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col>
        <v-text-field
          color="primary"
          loading
          disabled
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import InstallmentListItem from './InstallmentListItem.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'InstallmentList',
  data() {
    return {
      // 유저 정렬 기준 선택. 기본값 최고금리순
      selectedOption: 'maxIntrRate',
    }
  },
  components: {
    InstallmentListItem,
  },
  computed: {
    // 최고금리순, 기본금리순
    ...mapGetters(['maxSortedInstallments', 'sortedInstallments']),
    // 적금 일반
    installments() {    
      return this.$store.state.finlife.installments
    },
  },
  created() {
    if (this.maxSortedInstallments.length === 0) {
      this.getSortedByMaxInstallments()
    }
    if (this.sortedInstallments.length === 0) {
      this.getSortedInstallments()
    }  
  },
  methods: {
    // 적금 최고금리순 조회, 저장
    getSortedByMaxInstallments() {
      this.$store.dispatch('getSortedByMaxInstallments')
    },
    // 적금 기본금리순 조회, 저장
    getSortedInstallments() {
      this.$store.dispatch('getSortedInstallments')
    },
  }

}
</script>

<style scoped>
input[type="radio"] {
  /* 라디오박스 동그라미 표시 안 나오게 */
  appearance: none;
  /* 웹킷 기반 브라우저에 적용되는 속성 */
  -webkit-appearance: none;
  /* 파이어폭스에 적용되는 속성 */
  -moz-appearance: none;
}

/* 선택된 값 표시되도록 */
input[type="radio"]:checked + label {
  background-color: gray;
}
</style>