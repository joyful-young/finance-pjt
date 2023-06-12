<template>
  <v-container>
    <v-row class="text-center mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <h2>새로운 게시글</h2>
        <ArticleForm
          :article="article"
          action="create"
        />
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import ArticleForm from '@/components/community/ArticleForm.vue'

export default {
  name: 'ArticleCreateView',
  data() {
    return {
      article: {
        title: '',
        content: '',
        category: '일반',
      }
    }
  },
  components: {
    ArticleForm,
  }
}
</script>

<style>

</style>