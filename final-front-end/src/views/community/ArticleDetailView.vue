<template>
  <v-container>
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col v-if="article" cols="12" sm="10" lg="8">
        <!-- [분류] 제목 -->
        <v-row class="mt-3">
          <v-col>
            <h1>[{{ article.category }}] {{ article.title }}</h1>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <!-- 작성자, 작성 및 수정 날짜, 좋아요 버튼 -->
        <v-row class="mt-3">
          <v-col>
            <router-link :to="{ name: 'profile', params: { username: article.write_user.username }}">
            <v-avatar v-if="article.write_user.avatar" size="48">
              <v-img
                :src="article.write_user.avatar"
                alt="작성자 프로필 사진"
              ></v-img>
            </v-avatar>
            <v-avatar v-else>
              <v-icon size="48"
              >mdi-account-circle</v-icon>
            </v-avatar>
            <span
              class="font-weight-bold"
            >{{ article.write_user.username }}</span>
            </router-link>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="auto">
            <v-row class="">
              <v-col cols="12">
                <span class="caption">
                  {{ createdAt }} 작성
                </span>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <span class="caption">
                  {{ updatedAt }} 수정
                </span>
              </v-col>
            </v-row>
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="auto" class="d-flex align-center text-right">
            <v-btn color="primary" text @click="likeArticle()">
              <v-icon left>{{ likeBtn }}</v-icon>
              {{ likeCount }}</v-btn>
          </v-col>
        </v-row>
        <v-divider></v-divider>

        <!-- 게시글 내용 -->
        <v-row class="my-3">
          <v-col cols="12">
            {{ article.content }}
          </v-col>
        </v-row>
        <v-divider></v-divider>

        <!-- 작성자용 기능 -->
        <v-row class="text-center my-3" v-if="article.write_user.id === currentUser.pk">
          <v-col>
            <router-link :to="{ name: 'ArticleUpdateView', params: { articleId: articleId }}">
              <v-btn color="primary" outlined small class="mr-2">
                <v-icon left>mdi-pencil</v-icon>
                수정
              </v-btn>
            </router-link>
            <v-btn color="error" outlined small @click="deleteArticle()">
              <v-icon left>mdi-delete</v-icon>
              삭제
            </v-btn>
          </v-col>
        </v-row>
        <v-divider></v-divider>
      </v-col>


      <v-col v-else cols="12" sm="10" lg="8">
        <p>로딩중...</p>
      </v-col>

      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>



    <!-- 댓글 -->
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <CommentForm
        @add-comment="addComment"
        :comment="{ content: '' }"
        action="create"
        :articleId="articleId"
      />
      <!-- <div v-if="comments">
        <CommentItem
          @delete-comment="deleteComment"
          v-for="comment in comments.slice().reverse()" :key="comment.id"
          :comment="comment"
        />
      </div> -->
    </v-row>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col v-if="comments" cols="12" sm="10" lg="8">
        <CommentItem
          @delete-comment="deleteComment"
          v-for="comment in latestComments" :key="comment.id"
          :comment="comment"
        />
      </v-col>
      <v-col v-else cols="12" sm="10" lg="8">
        <p>댓글을 작성해주세요.</p>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import CommentItem from '../../components/CommentItem.vue'
import CommentForm from '../../components/CommentForm.vue'
import axios from 'axios'
import api from '@/api'
import { mapGetters } from 'vuex'
import _ from 'lodash'

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
      // return this.likeFlag ? '좋아요 취소' : '좋아요'
      return this.likeFlag ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'
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
    // 최신순 되나
    latestComments() {
      return _.sortBy(this.comments, 'created_at').reverse()
    }
  },

  // 컴포넌트 들어가기 전 데이터 준비
  // 게시글 상세 데이터 받아와서 집어넣기
  // beforeRouteEnter(to, from, next) {
  //   const articleId = to.params.articleId;

  //   next(vm => {
  //     // Access the store using vm.$store
  //     vm.$store.dispatch('getArticleDetail', articleId)
  //       .then(response => {
  //         // Handle the response if needed
  //         console.log(response.data)
  //         vm.article = response.data
  //         next();
  //       })
  //       .catch(error => {
  //         // Handle the error appropriately
  //         console.log('Error fetching article details:', error);
  //         // Redirect to an error page or handle the error in any other way
  //         next('/404-not-found');
  //       });
  //   });
  // },


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

    // // 자스로 likeFlag 판단
    // async doesLikeThis() {
    //   try {
    //     await this.getArticleDetail(this.articleId)
    //     await this.getCurrentUser()
    //     console.log('이거 실행되나')
  
    //     if (this.likeUsers.includes(this.currentUser.pk)) {
    //       this.likeFlag = true
    //       console.log('true다')
    //     } else {
    //       this.likeFlag = false
    //       console.log('false다')
    //     }
    //   } catch (error) {
    //     console.log(error)
    //   }
    // },

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



    // 이 아래는 v-if로 만든 수정 form에 필요한 것들

    // updateFlagToggle() {
    //   this.updateFlag = true
    // },
    // updateArticle() {
    //   const title = this.article.title
    //   const content = this.article.content
    //   // const anonymous_is_active = this.article.anonymous_is_active

    //   // 일단 최소한의 유효성 검사
    //   if (title === '') {
    //     alert('제목을 입력해주세요')
    //     return
    //   }

    //   if (content === '') {
    //     alert('내용을 입력해주세요')
    //     return
    //   }      

    //   const form = {
    //     title,
    //     content,
    //     // anonymous_is_active,
    //     category: '예금',
    //   }

    //   axios({
    //     method: 'PUT',
    //     url: `${this.BACKEND_URL}community/detail/${this.articleId}/`,
    //     data: {
    //       ...form,
    //     },
    //     // data: {
    //     //   // id: this.articleId,
    //     //   title: title,
    //     //   content: content,
    //     //   category: '일반',
    //     // },
    //     headers: {
    //       Authorization: `Token ${this.token}`
    //     }
    //   })
    //   .then((response) => {
    //     console.log(response)
    //     // this.updateFlag = false
    //   })
    //   .catch((error) => {
    //     console.log(error)
    //   })
    // },
}

</script>

<style scoped>
.caption {
  color: #888;
}

</style>