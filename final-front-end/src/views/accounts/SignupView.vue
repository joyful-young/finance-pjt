<template>
  <v-container>
    <v-row class="text-center mt-10">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <h1>회원가입</h1>
        <SignupComponent/>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import SignupComponent from '@/components/accounts/SignupComponent.vue'

export default {
  name: 'SignupView',
  components: {
    SignupComponent,
  }
}
</script>

<style>

</style>