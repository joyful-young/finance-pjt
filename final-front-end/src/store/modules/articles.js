import axios from 'axios'
import router from '@/router/index.js'
import api from '@/api'

export default {
  state: {
    articles: [],
    articleDetail: {},
    categories: ['일반', '칼럼', '뉴스', '재테크', '주식', '채권', '예금', '적금', '대출'],
  },
  getters: {
    articles(state) {
      return state.articles
    },
    categories(state) {
      return state.categories
    },
    // 전체를 포함한 카테고리명
    categoriesAll(state) {
      return ['전체', ...state.categories]
    },
    articleLikeData(state) {
      return {
        likeUser: state.articleDetail.article_like_user,
        likeCount: state.articleDetail.like_count,
        likeFlag: state.articleDetail.like_flag
      }
    }
  },
  mutations: {
    // 전체 게시글 데이터 저장
    SET_ARTICLES(state, articles) {
      state.articles = articles
    },
    // 게시글 상세 데이터 저장
    SET_ARTICLE_DETAIL(state, article) {
      state.articleDetail = article
      console.log(article, 'detail 저장')
    }
  },
  actions: {
    // 전체 게시글 조회. state 저장
    getArticles(context) {
      axios.get(api.community.articlesList())
      .then((response) => {
        context.commit('SET_ARTICLES', response.data)
      })
      .catch((error) => {
        console.log('getArticles action 에러', error)
      })
    },

    // 게시글 상세 조회. state 저장
    getArticleDetail(context, articleId) {
      const request = {
        method: 'GET',
        url: api.community.articleDetail(articleId),
      }

      if (context.getters.isLoggedIn) {
        request['headers'] = context.getters.authHeader
      }

      return new Promise((resolve, reject) => {
        axios(request)
          .then((response) => {
            context.commit('SET_ARTICLE_DETAIL', response.data)
            resolve(response)
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
    deleteArticle(context, articleId) {
      axios({
        method: 'DELETE',
        url: api.community.articleDetail(articleId),
        headers: context.getters.authHeader
      })
      .then((response) => {
        console.log(response, '삭제 action 처리 완료')
        router.push({ name: 'ArticlesView' })
        // 뒤에 글이 남아있는데 삭제됐다고 나오는 게 별로.
        // 시간 되면 고칠 방법 찾아보기
        alert('삭제되었습니다')
      })
      .catch((error) => {
        console.log(error)
      })
    },
    // 게시글 좋아요/좋아요 취소
    likeArticle(context, articleId) {
      return new Promise((resolve, reject) => {
        axios({
          method: 'POST',
          url: api.community.articleLike(articleId),
          data: {
            article_id: articleId
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
  },
}