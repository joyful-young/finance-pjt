<template>
  <v-container>
    <!-- 게시글 상세 내용 -->
    <v-row class="mt-3">
      <v-col cols="12">
        <h1 class="display-1 mb-2">[{{ article.category }}] {{ article.title }}</h1>
      </v-col>
    </v-row>
    <v-divider></v-divider>

    <!-- 작성자, 작성 및 수정 날짜, 좋아요 버튼 -->
    <v-row class="mt-3">
      <v-col cols="12" md="6" lg="3">
        <router-link :to="{ name: 'profile', params: { username: article.write_user.username }}">
          <v-avatar size="48">
            <img :src="article.write_user.avatar" alt="작성자 프로필 사진">
          </v-avatar>
          <span class="subtitle-1 font-weight-bold">{{ article.write_user.username }}</span>
        </router-link>
      </v-col>
      <v-col cols="12" md="6" lg="3">
        <v-row class="mt-2">
          <v-col cols="12">
            <span class="caption">{{ createdAt }} 작성</span>
          </v-col>
          <v-col cols="12">
            <span class="caption">{{ updatedAt }} 수정</span>
          </v-col>
        </v-row>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" md="6" lg="3">
        <v-btn color="primary" text @click="likeArticle">
          <v-icon left>{{ likeIcon }}</v-icon>
          {{ likeCount }} {{ likeText }}
        </v-btn>
      </v-col>
    </v-row>
    <v-divider></v-divider>

    <!-- 게시글 내용 -->
    <v-row class="mt-3">
      <v-col cols="12">
        <div class="body-text" v-html="article.content"></div>
      </v-col>
    </v-row>
    <v-divider></v-divider>

    <!-- 작성자용 기능 -->
    <v-row class="mt-3" v-if="article.write_user.id === currentUser.pk">
      <v-col cols="12">
        <router-link :to="{ name: 'ArticleUpdateView', params: { articleId: articleId }}">
          <v-btn color="primary" outlined class="mr-2">
            <v-icon left>mdi-pencil</v-icon>
            수정하기
          </v-btn>
        </router-link>
        <v-btn color="error" outlined @click="deleteArticle">
          <v-icon left>mdi-delete</v-icon>
          삭제하기
        </v-btn>
      </v-col>
    </v-row>

    <!-- 댓글 -->
    <v-row class="mt-5">
      <v-col cols="12">
        <h2 class="headline">댓글</h2>
        <CommentForm
          @add-comment="addComment"
          :comment="{ content: '' }"
          action="create"
          :articleId="articleId"
        />
        <template v-if="comments.length">
          <CommentItem
            @delete-comment="deleteComment"
            v-for="comment in comments.slice().reverse()" :key="comment.id"
            :comment="comment"
          />
        </template>
        <template v-else>
          <p>댓글을 작성해주세요.</p>
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CommentItem from '../../components/CommentItem.vue'
import CommentForm from '../../components/CommentForm.vue'
import axios from 'axios'
import api from '@/api'
import { mapGetters } from 'vuex'

export default {
  name: 'ArticleDetailView',
  components: {
    CommentItem,
    CommentForm,
  },
  data() {
    return {
      article: null,
      likeCount: null,
      likeFlag: false,
      likeUsers: [],
      comments: [],
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'currentUser', 'authHeader']),
    // isLoggedIn() {
    //   return this.$store.getters.isLoggedIn
    // },
    likeBtn() {
      return this.likeFlag ? '좋아요 취소' : '좋아요'
    },
    // currentUser() {
    //   return this.$store.state.accounts.currentUser
    // },
    articleId() {
      return String(this.$route.params.articleId)
    },
    createdAt() {
      return this.article.created_at.replace('T', ' ').substr(0, 16)
    },
    updatedAt() {
      return this.article.updated_at.replace('T',' ').substr(0, 16)
    },
  },
  created() {
    // // 자스로 likeFlag 판단할 때
    // // 로그인한 유저라면
    // if (this.isLoggedIn) {
    //   this.doesLikeThis()
    //   console.log('created')
    // } else {      // 아니면 그냥 게시글 가져오면 됨
    //   this.getArticleDetail(this.articleId)
    // }

    // 백에서 likeFlag 가져오기
    this.getArticleDetail(this.articleId)
    if (this.isLoggedIn) {
      this.getCurrentUser()
    }

  },
  mounted() {
  },
  methods: {
    // 현재 유저 정보 가져오기
    getCurrentUser() {
      return new Promise((resolve, reject) => {
        this.$store.dispatch('getCurrentUser')
        .then((response) => {
          console.log(response, '바로 유저 객체임')
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
      })
    },
    
    // 게시글 상세 정보 받아와서 data의 article에 넣고 유저의 좋아요 여부, 좋아요 수도 같이 data에 저장해놓기
    getArticleDetail(articleId) {
      return new Promise((resolve, reject) => {
        this.$store.dispatch('getArticleDetail', articleId)
        .then((response) => {
          // 게시글 상세 조회 시 추천 알고리즘 데이터 수집을 위한 요청 보내기
          console.log(response.data, 'category 있나')

          if (this.isLoggedIn) {
            axios({
              method: 'POST',
              url: api.accounts.categoryCount(),
              data: {
                category: response.data.category,
              },
              headers: this.authHeader
              // headers: {
              //   'X-header': response.data.category,
              // }
            })
              .then((response) => {
                console.log(response, '알고리즘 데이터 수집')
              })
              .catch((error) => {
                console.log(error, '알고리즘 데이터 수집 에러')
              })
          }

          console.log(response.data, 'article 객체다')
          const article = response.data
          this.article = article
          this.likeCount = article.like_count
          this.likeUsers = article.article_like_user
          this.likeFlag = article.like_flag
          this.comments = article.comments
          resolve(article)
        })
        .catch((error) => {
          reject(error)
        })
      })
    },

    // 게시글 삭제
    deleteArticle() {
      this.$store.dispatch('deleteArticle', this.articleId)
    },

    // 게시글 좋아요 / 좋아요 취소
    likeArticle() {
      if (!this.isLoggedIn) {     // 로그인 안했으면 로그인 화면으로
        alert('로그인이 필요합니다.')
        this.$router.push({ name: 'LoginView'})
        return
      } else {
        this.$store.dispatch('likeArticle', this.articleId)
        .then((response) => {
          console.log(response)
          if (this.likeFlag) {    // 좋아요한 상태
            this.likeCount -= 1
          } else {                // 좋아요 아닌 상태
            this.likeCount += 1
          }
          this.likeFlag = !this.likeFlag
        })
        .catch((error) => {
          console.log(error)
        })
      }
    },
    addComment(newComment) {
      console.log('부모 컴포넌트에서 이벤트')
      this.comments.push(newComment)
    },
    deleteComment(commentId) {
      console.log('부모 컴포넌트에서 이벤트', commentId)
      console.log(this.comments)
      this.comments = this.comments.filter((comment) => {
        return comment.id !== commentId
      })
      console.log(this.comments)
    }
  },
}

</script>

<style scoped>
.display-1 {
  font-size: 48px;
  font-weight: bold;
}

.subtitle-1 {
  font-size: 18px;
  font-weight: bold;
}

.caption {
  font-size: 12px;
  color: #888;
}

.body-text {
  font-size: 16px;
  line-height: 1.6;
}

.headline {
  font-size: 24px;
  font-weight: bold;
}

.mt-2 {
  margin-top: 8px;
}

.mt-3 {
  margin-top: 16px;
}

.mt-5 {
  margin-top: 40px;
}

.v-avatar {
  display: inline-block;
  width: 48px;
  height: 48px;
  overflow: hidden;
  border-radius: 50%;
}

.v-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

</style>