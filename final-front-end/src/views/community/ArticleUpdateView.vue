<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <h2>글 수정 페이지</h2>
        <ArticleForm v-if="article.title !== ''"
          :article="article"
          action="update"
        />
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import api from '@/api'
import ArticleForm from '@/components/community/ArticleForm.vue'

export default {
  name: 'ArticleUpdateView',
  components: {
    ArticleForm,
  },
  data() {
    return {
      article: {
        title: '',
        content: '',
        category: '일반',
      }
    }
  },
  computed: {
    articleId() {
      return this.$route.params.articleId
    }
  },
  created() {
    this.getOldArticle()
  },
  methods: {
    // 수정 전 게시글 불러오기
    getOldArticle() {
      axios.get(api.community.articleDetail(this.articleId))
      .then((response) => {
        const article = response.data
        this.article.title = article.title
        this.article.content = article.content
        this.article.category = article.category
      })
      .catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style>

</style>