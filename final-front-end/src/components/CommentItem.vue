<template>
  <v-row>
    <v-col v-if="!updateFlag">
      <v-row>
        <v-col cols="2">
          <router-link :to="{ name: 'profile', params: { username: comment.user }}">
            <v-avatar v-if="comment.user.avatar" size="24">
              <v-img
                :src="comment.user.avatar"
                alt="작성자 프로필 사진"
              ></v-img>
            </v-avatar>
            <v-avatar v-else>
              <v-icon size="24"
              >mdi-account-circle</v-icon>
            </v-avatar>
            <span
              class="font-weight-bold"
            >{{ comment.user }}</span>
          </router-link>
        </v-col>
        <v-col cols="5" class="d-flex align-center" style="font-size: 12px">
          수정일: {{ updatedAt }}
        </v-col>
        <v-col cols="2"></v-col>
        <!-- 작성자 본인이면 수정, 삭제 버튼 -->
        <v-col cols="3" v-if="comment.user === currentUser.pk" class="text-end">
          <v-btn color="primary" outlined small @click="goUpdate()" class="mr-2">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>

          <v-btn color="error" outlined small @click="deleteComment()">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="3" v-else></v-col>


        <v-col cols="9">
          <p>{{ newComment.content }}</p>
        </v-col>
        <v-col cols="3" class="text-end">
          <v-btn color="primary" text @click="likeComment()">
            <v-icon left>{{ likeBtn }}</v-icon>{{ likeCount }}</v-btn>
        </v-col>
      </v-row>
    </v-col>


    <v-col v-if="updateFlag">
      <!-- <form @submit.prevent="updateComment()">
        <div>
          <label for="content">댓글</label>
          <textarea id="content" v-model="newComment.content" cols="70" rows="10" type="text" placeholder="댓글을 입력해주세요." required></textarea>
        </div>
        <div>
          <button>수정</button>
        </div>
      </form> -->
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
          <v-btn @click="updateComment()" type="submit" color="info">
            <v-icon>mdi-comment-plus</v-icon>
            수정
          </v-btn>
        </v-col>
      </v-row>
    </v-col>



    <!-- 수정 페이지 -->
    <!-- <div v-else>
      <h2>글 수정하기</h2>
      <form @submit.prevent="updateArticle()">
        <div>
          <label for="title">제목: </label>
          <input id="title" type="text" v-model.trim="article.title">
        </div>
        <div>
          <label for="content">내용: </label>
          <textarea id="content" cols="30" rows="10" v-model="article.content"></textarea>
        </div>
        <div>
          <label for="want-anonymous">익명 여부 선택</label>
          <input id="want-anonymous" type="checkbox" v-model="article.anonymous_is_active">
        </div>
        <button>수정하기</button>
      </form>
    </div> -->
  </v-row>
</template>

<script>
export default {
  name: 'CommentItem',
  data() {
    return {
      newComment: this.comment,
      updateFlag: false,
      likeFlag: false,
      likeCount: null,
    }
  },
  props: {
    comment: Object,
  },
  computed: {
    updatedAt() {
      return this.comment.updated_at.replace('T', ' ').substr(0, 16)
    },
    currentUser() {
      return this.$store.state.accounts.currentUser
    },
    likeBtn() {
      // return this.likeFlag ? '좋아요 취소' : '좋아요'
      return this.likeFlag ? 'mdi-thumb-up' : 'mdi-thumb-up-outline'
    },
  },
  mounted() {
    if (this.comment.comment_like_user.includes(this.currentUser.pk)) {
      this.likeFlag = true
    } else {
      this.likeFlag = false
    }
    this.likeCount = this.comment.comment_like_user.length
  },
  methods: {
    deleteComment() {
      const wantDelete = confirm('댓글을 삭제하시겠습니까?')

      if (wantDelete) {
        this.$store.dispatch('deleteComment', this.comment.id)
        .then((response) => {
          console.log(response, '댓글 삭제 완료')
          this.$emit('delete-comment', this.comment.id)
        })
        .catch((error) => {
          console.log(error)
        })
      } else {
        return
      }
    },
    goUpdate() {
      this.updateFlag = true
    },
    updateComment() {
      this.$store.dispatch('updateComment', this.newComment)
      .then((response) => {
        console.log(response, '댓글 수정 완료')
        this.updateFlag = false
      })
      .catch((error) => {
        console.log(error)
      })
    },
    likeComment() {
      const articleId = this.comment.article
      const commentId = this.comment.id
      const payload = {
        articleId,
        commentId
      }
      this.$store.dispatch('likeComment', payload)
      .then((response) => {
        console.log('좋아요 완료', response)
        if (this.likeFlag) {
          this.likeCount -= 1
        } else {
          this.likeCount += 1
        }
        this.likeFlag = !this.likeFlag
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