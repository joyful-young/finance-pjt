<template>
  <v-app>

    <v-app-bar
      app
      dark
      id="nav"
    >
      <v-container fluid>
        <v-tabs
        dark
        >
          <v-tab :to="{ name: 'home' }">
            <v-img
              src="@/assets/image/3percentLogo.png"
              contain
              height="100%"
              width="100%"
            ></v-img></v-tab>
          <v-tab :to="{ name: 'deposit'}">정기 예금</v-tab>
          <v-tab :to="{ name: 'installment'}">적금</v-tab>
          <v-tab :to="{ name: 'HwanyulView'}">환율</v-tab>
          <v-tab :to="{ name: 'bank'}">은행 검색</v-tab>
          <!-- <v-tab href="/bank">은행 검색</v-tab> -->
          <v-tab :to="{ name: 'articles'}">Community</v-tab>
          <v-tab :to="{ name: 'RecommendView'}">추천페이지</v-tab>


          <v-spacer></v-spacer>


          <v-tab v-if="!isLoggedIn" :to="{ name: 'login' }">로그인</v-tab>
          <v-tab v-if="!isLoggedIn" :to="{ name: 'signup' }">회원가입</v-tab>
          <v-tab v-if="isLoggedIn" :to="{ name: 'profile', params: { username: currentUser?.username }}">프로필</v-tab>
          <v-tab>
            <v-btn v-if="isLoggedIn" @click="logout()">로그아웃</v-btn>
          </v-tab>
        </v-tabs>
      </v-container>

    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
    <FootBar/>
    <!-- v-main 위에 넣었던데 여기가 맞지 않으려나 -->
  </v-app>
  <!-- 어떻게 쓰는지 모르겠으니까 일단 주석 처리함 -->
      <!-- contain 이미지 종횡비 유지하면서 컨테이너에 맞게 크기 조정 -->
      <!-- target="_blank" 버튼 클릭시 링크가 새 브라우저 탭이나 창에서 열리도록 지정 -->
  <!-- <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app> -->



  <!-- <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/deposit">정기 예금</router-link> |
      <router-link to="/installment">적금</router-link> |
      <router-link to="/exchange-rate">환율</router-link> |
      <router-link to="/bank">은행 검색</router-link> |
      <router-link to="/articles">Community</router-link> |
      <router-link to="/login">로그인</router-link> |
      <router-link to="/signup">회원가입</router-link> |
      <button>로그아웃</button>
    </nav>
    <router-view/>
  </div> -->
</template>

<script>
import { mapGetters } from 'vuex'
import FootBar from './FootBar.vue'

export default {
  name: 'App',
  components: {
    FootBar,
  },
  data: () => ({
  }),
  computed: {
    ...mapGetters([ 'currentUser', 'isLoggedIn' ]),
  },
  created() {
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
    }
  }  
};
</script>

<style scoped>
a {
  text-align: align-center;
}
/* 
#nav {
  font-family: 'Black Han Sans';
} */
</style>