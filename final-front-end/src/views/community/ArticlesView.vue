<template>
  <v-container fluid>
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <v-row>
          <v-col>
            <h1>커뮤니티</h1>
          </v-col>
        </v-row>
        <v-row v-if="isLoggedIn">
          <v-col></v-col>
          <v-col cols="auto" class="text-right">
            <v-btn
              elevation="8"
            >
              <v-icon
                color="primary"
              >mdi-pencil-plus</v-icon>
              <router-link :to="{ name: 'ArticleCreateView' }">글 작성</router-link>
            </v-btn>
          </v-col>
        </v-row>
        <ArticleList/>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import ArticleList from '@/components/community/ArticleList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'ArticlesView',
  components: {
    ArticleList,
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
  }
}
</script>

<style>
a {
  color: inherit;
  text-decoration: none;
}
</style>