<template>
  <v-container>
    <v-spacer></v-spacer>
    <v-form @submit.prevent="submitArticle()">
      <v-row>
        <v-spacer></v-spacer>
        <v-col>
          <v-select class="align-center"
            :items="categories"
            label="분류"
            dense
            solo
            hint="분류를 선택해주세요."
            v-model="newArticle.category"
            :rules="[rules.required]"
          ></v-select>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="12" lg="8">
          <v-text-field
            solo
            label="제목"
            hint="제목을 입력해주세요."
            v-model="newArticle.title"
            :rules="[rules.required, rules.counter]"
            counter
            maxlength="100"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="12" lg="8">
          <v-textarea
            solo
            label="내용"
            hint="내용을 입력해주세요."
            v-model="newArticle.content"
            :rows="10"
            :rules="[rules.required]"
            auto-grow
          ></v-textarea>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn class="ma-1" @click="goBack()">
            <v-icon left>mdi-arrow-left</v-icon>
            목록 보기
          </v-btn>
          <v-btn class="ma-1" @click="submitArticle()">{{ actionBtn }}</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios'
import api from '@/api'
import { mapGetters } from 'vuex'

export default {
  name: 'ArticleForm',
  props: {
    // 빈 article 혹은 수정할 article
    article: Object,
    // create or update
    action: String,
  },
  computed: {
    ...mapGetters(['authHeader', 'categories']),
    articleId() {
      return this.$route.params.articleId
    },
  },  
  data() {
    return {
      newArticle: {
        title: this.article.title,
        content: this.article.content,
        category: this.article.category,
      },
      actionBtn: (this.action === 'create') ? '등록' : '수정',
      rules: {
          required: value => !!value || '필수 입력 항목입니다.',
          counter: value => value.length <= 100 || '제목은 최대 100자입니다.',
          // email: value => {
          //   const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          //   return pattern.test(value) || 'Invalid e-mail.'
          // },
        },
    }
  },
  methods: {
    // 글 생성 시에는 글 목록으로, 글 수정 시에는 상세 페이지로
    goBack() {
      if (this.action === 'create') {
        this.$router.push({ name: 'articles'})
      } else {
        this.$router.push({ name: 'ArticleDetailView', params: { articleId: this.articleId }})
      }
    },
    // 글 생성 / 수정
    submitArticle() {
      // 유효성 검사
      if (this.newArticle.category === '') {
        alert('분류를 선택해주세요.')
        return
      }

      if (this.newArticle.title === '') {
        alert('제목을 입력해주세요.')
        return
      }

      if (this.newArticle.content === '') {
        alert('내용을 입력해주세요.')
        return
      }

      // 글 생성
      if (this.action === 'create') {
        axios({
          method: 'POST',
          url: api.community.articlesList(),
          data: {
            ...this.newArticle,
          },
          headers: this.authHeader,
        })
        .then((response) => {
          console.log(response)
          
          // 값 초기화
          this.newArticle.title = ''
          this.newArticle.content = ''
          this.newArticle.category = '일반'

          // detail로 보내기
          const newArticleId = response.data.id
          this.$router.push({
            name: 'ArticleDetailView',
            params: { articleId: newArticleId }
          })
        })
        .catch((error) => {
          console.log(error)
        })
      }
      // 글 수정
      else if (this.action === 'update') {
        axios({
          method: 'PUT',
          url: api.community.articleDetail(this.articleId),
          data: {
            ...this.newArticle,
          },
          headers: this.authHeader,
        })
        .then((response) => {
          console.log(response)
          // detail로 보내기
          this.$router.push({
            name: 'ArticleDetailView',
            articleId: this.$route.params.articleId
          })
        })
        .catch((error) => {
          console.log(error)
        })
      }
    },
  }
}
</script>

<style>

</style>