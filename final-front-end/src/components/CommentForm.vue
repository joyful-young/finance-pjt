<template>
  <v-col cols="12" sm="10" lg="8">
    <v-row>
      <v-col>
        <h5>댓글</h5>
      </v-col>
    </v-row>
    <v-row>
      <v-row>
        <v-col cols="10" class="pr-0">
          <v-form @submit.prevent>
            <v-textarea
              prepend-inner-icon="mdi-comment-outline"
              v-model.trim="newComment.content"
              :label="placeholderContent"
              filled
              outlined
              rows="1"
              auto-grow
            ></v-textarea>
          </v-form>
        </v-col>
        <v-col cols="2">
          <v-btn @click="submitComment()" type="submit" color="info">
            <v-icon>mdi-comment-plus</v-icon>
            {{ actionBtn }}
          </v-btn>
        </v-col>
      </v-row>
    </v-row>
  </v-col>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'CommentForm',
  props: {
    // 빈 comment 혹은 수정할 comment
    comment: Object,
    // create or update
    action: String,
    // 댓글이 달릴 게시글 pk
    articleId: String,
  },
  data() {
    return {
      newComment: {
        content: this.comment.content,
      },
      actionBtn: (this.action === 'create') ? '등록' : '수정',
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
    placeholderContent() {
      return this.isLoggedIn ? '댓글을 입력해주세요.' : '댓글을 작성하시려면 로그인을 해주세요.'
    },
  },
  methods: {
    submitComment() {
      if (!this.isLoggedIn) {
        alert('로그인이 필요합니다.')
        this.$router.push({ name: 'LoginView'})
        return
      } else {
        if (this.action === 'create') {   // 글 생성

          if (this.newComment.content === '') {
            alert('댓글을 입력해주세요.')
            return
          }

          const payload = {
            // 게시글 아이디랑 댓글 내용
            articleId: this.articleId,
            ...this.newComment,
          }
          this.$store.dispatch('createComment', payload)
          .then((response) => {
            console.log('댓글생성요청응답받았다', response.data)
            this.$emit('add-comment', response.data)
            this.newComment.content = ''    // 입력 필드 초기화
          })
          .catch((error) => {
            console.log(error)
          })
        }
      }
    }
  }
}
</script>

<style>

</style>