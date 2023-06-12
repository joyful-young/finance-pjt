<template>
  <v-container fluid>
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <div class="ml-10">
          <h1>정기예금</h1>
        </div>
        <DepositList/>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import DepositList from '@/components/finlife/DepositList.vue'

export default {
  name: 'DepositView',
  components: {
    DepositList,
  },
  created() {
    // 예금 데이터 가져와서 state에 저장하도록 함
    // 일반 조회 메서드. 최고금리순 따로 있어서 안 씀.
    // this.getDeposits()
  },
  methods: {
    // getDeposits() {
    //   this.$store.dispatch('getDeposits')
    // }
  }
}
</script>

<style>

</style>