// api url 모음
const BACKEND_URL = 'http://127.0.0.1:8000/'
// const BACKEND_URL = 'http://70.12.102.97:8000/'      // ssafy
// const BACKEND_URL = 'http://172.30.43.87:8000/'
// const BACKEND_URL = 'http://172.30.42.155:8000/'
// const BACKEND_URL = 'http://175.196.236.214:8000/'
// const BACKEND_URL = 'http://192.168.55.176:8000/'
// const BACKEND_URL = 'http://110.14.180.239:8000/'
// const BACKEND_URL = 'http://59.14.27.248:8000/'

const DRF = 'dj-rest-auth/'
// const ADMIN = 'admin/'
const ACCOUNTS = 'accounts/'
const DEPOSITS = 'finlife/'
const INSTALLMENTS = 'saving/'
const COMMUNITY = 'community/'
const EXCHANEG_RATE = 'hwanyul/'
const BANK_MAP = 'search_bank/'
const BECOME_SUPER_RICH = 'becomesuperrich/'

export default {
  // admin 관리자 관련
  // 유저 관련
  accounts: {
    checkDuplicate(username) {
      return BACKEND_URL + ACCOUNTS + `unique_check/${username}/`
    },
    signUp() {
      return BACKEND_URL + ACCOUNTS + 'signup/'
    },
    login() {
      return BACKEND_URL + ACCOUNTS + DRF + 'login/'
    },
    // 로그아웃
    logout() {
      return BACKEND_URL + ACCOUNTS + DRF + 'logout/'
    },
    // 현재 유저 확인
    currentUser() {
      return BACKEND_URL + ACCOUNTS + DRF + 'user/'
    },
    // 프로필 정보 요청
    profileData(userPK) {
      return BACKEND_URL + ACCOUNTS + `profile_view/${userPK}/`
    },
    // 프로필 수정
    profileUpdate(username) {
      return BACKEND_URL + ACCOUNTS + `edit_profile/${username}/`
    },
    // 유저 팔로우
    userFollow(username) {
      return BACKEND_URL + ACCOUNTS + `follow/${username}/`
    },
    // 차트 조회
    chart(username) {
      return BACKEND_URL + ACCOUNTS + `chart-data/${username}`
    },
    // 추천 알고리즘 위한 말머리별 카운트
    categoryCount() {
      return BACKEND_URL + ACCOUNTS + 'increase_count/'
      // return BACKEND_URL + ACCOUNTS + 'increase_count'
    }
  },
  // 예금 관련
  deposits: {
    // 전체 예금 조회
    depositsList() {
      return BACKEND_URL + DEPOSITS + 'deposit-products/'
    },
    // 최고 금리 순
    maxSortedDepositList() {
      return BACKEND_URL + DEPOSITS + 'max_intr_deposit_products/'
    },
    // 기본 금리 순
    sortedDepositList() {
      return BACKEND_URL + DEPOSITS + 'kibon_intr_deposit_products/'
    },
    // 예금 상세 조회
    depositDetail(finPrdtCd) {
      return BACKEND_URL + DEPOSITS + `detail_deposit_product/${finPrdtCd}/`
      // return BACKEND_URL + DEPOSITS + `deposit-product-options/${finPrdtCd}/`
    },
    // 예금 좋아요
    depositLike(finPrdtCd) {
      return BACKEND_URL + DEPOSITS + `like_deposit_product/${finPrdtCd}/`
    },
    // 예금 가입 / 해지
    depositJoin(finPrdtCd) {
      return BACKEND_URL + DEPOSITS + `register_deposit_product/${finPrdtCd}/`
    }
  },
  // 적금 관련
  installments: {
    // 전체 적금 조회
    installmentsList() {
      return BACKEND_URL + INSTALLMENTS + 'saving-products/'
    },
    // 최고 금리 순
    maxSortedInstallmentList() {
      return BACKEND_URL + INSTALLMENTS + 'max_intr_saving_products/'
    },
    // 기본 금리 순
    sortedInstallmentList() {
      return BACKEND_URL + INSTALLMENTS + 'kibon_intr_saving_products/'
    },
    // 적금 상세 조회
    installmentDetail(finPrdtCd) {
      return BACKEND_URL + INSTALLMENTS + `saving-product-options/${finPrdtCd}/`
    },
    // 적금 좋아요
    installmentLike(finPrdtCd) {
      return BACKEND_URL + INSTALLMENTS + `like_saving_product/${finPrdtCd}/`
    },
    // 적금 가입 / 해지
    installmentJoin(finPrdtCd) {
      return BACKEND_URL + INSTALLMENTS + `register_saving_product/${finPrdtCd}/`
    }
  },
  // 커뮤니티 관련
  community: {
    // 전체 글 조회, 생성
    articlesList() {
      return BACKEND_URL + COMMUNITY
    },
    // 상세 글 조회, 수정, 삭제
    articleDetail(articleId) {
      return BACKEND_URL + COMMUNITY + `detail/${articleId}/`
    },
    // 게시글 좋아요/좋아요취소
    articleLike(articleId) {
      return BACKEND_URL + COMMUNITY + `like/${articleId}/`
    },
    // 댓글 생성
    commentCreate(articleId) {
      return BACKEND_URL + COMMUNITY + `comment_create/${articleId}/`
    },
    // 댓글 상세 조회, 수정, 삭제
    commentDetail(commentId) {
      return BACKEND_URL + COMMUNITY + `comment_detail/${commentId}/`
    },
    // 댓글 좋아요/좋아요 취소
    commentLike(payload) {
      const articleId = payload.articleId
      const commentId = payload.commentId
      return BACKEND_URL + COMMUNITY + `like_comments/${articleId}/${commentId}/`
    }
  },
  // 환율 url
  exchangeRate: {
    exchangeRate(country, amount, conversionType) {
      return BACKEND_URL + EXCHANEG_RATE + `?country=${country}&amount=${amount}&conversionType=${conversionType}`
    }
  },
  // 지도 관련
  bankMap: {
    searchBank() {
      return BACKEND_URL + BANK_MAP
    }
  },
  // 추천 알고리즘 관련
  becomesuperrich: {
    portfoliorecommend() {
      return BACKEND_URL + BECOME_SUPER_RICH + 'f_s_e/'
    },
    hybrid_recommendation() {
      return BACKEND_URL + BECOME_SUPER_RICH + 'hybrid_recommendation/'
    },
  }
}