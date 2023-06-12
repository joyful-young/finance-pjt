<template>
  <v-container>
    <v-row class="text-center mt-10">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <h1>로그인</h1>
        <LoginComponent/>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
    <v-row class="text-center">
      <v-col>
        <p>회원이 아니신가요? <router-link :to="{ name: 'signup' }">회원가입</router-link></p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LoginComponent from '@/components/accounts/LoginComponent.vue'

export default {
  name: 'LoginView',
  components: {
    LoginComponent,
  }
}
</script>

<style>

</style>