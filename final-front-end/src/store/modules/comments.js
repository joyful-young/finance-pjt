import axios from 'axios'
import api from '@/api'

export default {
  state: {
  },
  getters: {

  },
  mutations: {
  },
  actions: {
    // 댓글 생성
    createComment(context, payload) {
      const articleId = payload.articleId
      const content = payload.content

      return new Promise((resolve, reject) => {
        axios({
          method: 'POST',
          url: api.community.commentCreate(articleId),
          data: {
            article: articleId,
            content,
          },
          headers: context.getters.authHeader
        })
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
      })
    },
    deleteComment(context, commentId) {
      console.log('액션 호출 안 됨?')
      return new Promise((resolve, reject) => {
        axios({
          method: 'DELETE',
          url: api.community.commentDetail(commentId),
          headers: context.getters.authHeader
        })
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
      })
    },
    updateComment(context, comment) {
      console.log('댓글 수정 액션 호출')
      return new Promise((resolve, reject) => {
        axios({
          method: 'PUT',
          url: api.community.commentDetail(comment.id),
          data: {
            ...comment
          },
          headers: context.getters.authHeader
        })
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
      })
    },
    async likeComment(context, payload) {
      console.log('댓글 좋아요 액션 호출')
      try {
        const response = await axios({
          method: 'POST',
          url: api.community.commentLike(payload),
          headers: context.getters.authHeader
        })
        console.log('좋아요 응답', response)
        return response
      } catch (error) {
        console.log(error)
        return error
      }
    }
  }
}