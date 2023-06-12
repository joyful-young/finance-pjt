<template>
  <div>
    <h2>글 작성</h2>
    <form @submit.prevent="createArticle()">
      <div>
        <label for="title">제목: </label>
        <input id="title" type="text" v-model.trim="form.title">
      </div>
      <div>
        <label for="content">내용: </label>
        <textarea id="content" cols="30" rows="10" v-model="form.content"></textarea>
      </div>
      <div>
        <label for="want-anonymous">익명 여부 선택</label>
        <input id="want-anonymous" type="checkbox" v-model="form.anonymous_is_active">
      </div>
      <button>작성하기</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ArticleCreateView',
  data() {
    return {
      form: {
        // 초기값은 ''가 좋을까 null이 좋을까
        title: '',
        content: '',
        // default를 true로 했던데 거기 맞춰서 써야되나
        // isActive: false,
        // 변수 이름을 장고 모델이랑 맞춰야 하는걸까
        // anonymous_is_active: false,
      }
    }
  },
  computed: {
    BACKEND_URL() {
      return this.$store.state.BACKEND_URL
    },
    token() {
      return localStorage.getItem('key') ? localStorage.getItem('key') : false
    }
  },
  methods: {
    createArticle() {
      // 글 작성은 여기서만 쓸테니까 action까지 가지 말고 여기다 하자
      // 아직 글 작성 url이 없네

      const form = this.form

      // 일단 최소한의 유효성 검사
      if (form.title === '') {
        alert('제목을 입력해주세요')
        return
      }

      if (form.content === '') {
        alert('내용을 입력해주세요')
        return
      }

      const CREATE_ARTICLE_URL = `${this.BACKEND_URL}community/`

      // 요청 보내면 백에서 알아서 DB에 저장해줄 것임
      axios({
        method: 'POST',
        url: CREATE_ARTICLE_URL,
        data: {
          ...form,
        },
        headers: {
          Authorization: `Token ${this.token}`
        }
      })
      .then((response) => {
        console.log(response)
        // 사용자경험
        // 생성되면 detail로 가는 게 좋겠는데
        // $router.push?
        
        // 값 초기화 - 근데 detail로 보낼거면 이게 필요한가?
        form.title = ''
        form.content = ''
        // form.isActive = false
        form.annonymous_is_active = false

        // detail로 보내자
        // 근데 그럼 article id 알아야 함
        // response 안에 들어있을까?
        // this.$router.push({
        //   name: ArticleDetailView,
        //   params: { articleId: ~~~ }
        // })

      })
      .catch((error) => {
        console.log(error)
      })
    },
  },
}
</script>

<style>

</style>