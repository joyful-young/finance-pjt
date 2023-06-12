<template>
  <v-sheet
    color="#E3F2FD"
    elevation="2"
    rounded
    class="pa-5"
  >
    <p>저축 금리 유형: {{ option.intr_rate_type_nm }}</p>
    <p>저축 금리: {{ intrRate }} %</p>
    <p v-if="intrRate !== intrRate2">
      최고 우대금리: {{ intrRate2 }} %
    </p>
  </v-sheet>
</template>

<script>
export default {
  name: 'DepositOption',
  props: {
    option: Object,
  },
  computed: {
    intrRate() {
      return this.option.intr_rate.toFixed(2)
    },
    intrRate2() {
      return this.option.intr_rate2.toFixed(2)
    },
  }
}
</script>

<style>

</style>