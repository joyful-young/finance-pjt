<template>
  <v-container fluid>
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <div class="ml-10">
          <h1>적금</h1>
        </div>
        <InstallmentList/>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import InstallmentList from '@/components/finlife/InstallmentList.vue'

export default {
  name: 'InstallmentView',
  components: {
    InstallmentList,
  },
  created() {
    // 적금 데이터 가져와서 state에 저장하도록
    this.getInstallments()
  },
  methods: {
    getInstallments() {
      this.$store.dispatch('getInstallments')
    }
  }
}
</script>

<style>

</style>