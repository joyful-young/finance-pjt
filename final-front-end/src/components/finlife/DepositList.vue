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

    <v-row v-if="selectedOption === 'maxIntrRate' && maxSortedDeposits.length !== 0">
      <v-col>
        <DepositListItem
          v-for="deposit in maxSortedDeposits" :key="deposit.fin_prdt_cd"
          :selectedOption="selectedOption"
          :deposit="deposit"
        />
      </v-col>
    </v-row>
    <v-row v-else-if="selectedOption === 'intrRate' && sortedDeposits.length !== 0">
      <v-col>
        <DepositListItem
          v-for="deposit in sortedDeposits" :key="deposit.fin_prdt_cd"
          :selectedOption="selectedOption"
          :deposit="deposit"
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
import DepositListItem from './DepositListItem.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'DepositList',
  data() {
    return {
      // 유저 정렬 기준 선택. 기본값 최고금리순
      selectedOption: 'maxIntrRate',
    }
  },
  components: {
    DepositListItem,
  },
  computed: {
    // 최고금리순, 기본금리순
    ...mapGetters([ 'maxSortedDeposits', 'sortedDeposits' ]),
    // 예금 일반
    deposits() {    
      return this.$store.state.finlife.deposits
    },
  },
  created() {
    if (this.maxSortedDeposits.length === 0) {
      this.getSortedByMaxDeposits()
    }
    if (this.sortedDeposits.length === 0) {
      this.getSortedDeposits()
    }
  },
  methods: {
    // 예금 최고금리순 조회, 저장
    getSortedByMaxDeposits() {
      this.$store.dispatch('getSortedByMaxDeposits')
    },
    // 예금 기본금리순 조회, 저장
    getSortedDeposits() {
      this.$store.dispatch('getSortedDeposits')
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