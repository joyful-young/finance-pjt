import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'


import HomeView from '../views/HomeView.vue'

import NotFound404 from '../views/NotFound404.vue'

import DepositView from '../views/finlife/DepositView.vue'
import DepositDetailView from '../views/finlife/DepositDetailView.vue'
import InstallmentView from '../views/finlife/InstallmentView.vue'
import InstallmentDetailView from '../views/finlife/InstallmentDetailView.vue'
// import RecommendView from '../views/finlife/RecommendView.vue'
import RecommendView2 from '../views/finlife/RecommendView2.vue'
// import ExchangeRateView from '../views/finlife/ExchangeRateView.vue'
import BankMapView from '../views/finlife/BankMapView.vue'

import ArticlesView from '../views/community/ArticlesView.vue'
import ArticleCreateView from '../views/community/ArticleCreateView.vue'
import ArticleDetailView from '../views/community/ArticleDetailView.vue'
import ArticleUpdateView from '../views/community/ArticleUpdateView.vue'

import LoginView from '../views/accounts/LoginView.vue'
import SignupView from '../views/accounts/SignupView.vue'
import ProfileView from '../views/accounts/ProfileView.vue'

import HwanyulView from '../views/hwanyul/HwanyulView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/404-not-found',
    name: 'NotFound404',
    component: NotFound404
  },
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // },
  {
    path: '/deposit',
    name: 'deposit',
    component: DepositView,
  },
  {
    path: '/deposit/:finPrdtCd',
    name: 'DepositDetailView',
    component: DepositDetailView
  },
  {
    path: '/installment',
    name: 'installment',
    component: InstallmentView
  },
  {
    path: '/installment/:finPrdtCd',
    name: 'InstallmentDetailView',
    component: InstallmentDetailView
  },
  {
    path: '/recommmend',
    name:'RecommendView',
    component: RecommendView2,
  },
  {
    path: '/exchange-rate',
    name: 'HwanyulView',
    component: HwanyulView
  },
  {
    path: '/bank',
    name: 'bank',
    component: BankMapView
  },
  {
    path: '/articles',
    name: 'articles',
    component: ArticlesView,
  },
  {
    path: '/articles/:articleId',
    name: 'ArticleDetailView',
    component: ArticleDetailView
  },
  // 게시글 수정 페이지 - 로그인 필요
  {
    path: '/articles/:articleId/update',
    name: 'ArticleUpdateView',
    component: ArticleUpdateView,
    // meta: {
    //   requiresAuth: true
    // }
  },
  // 게시글 생성 페이지 - 로그인 필요
  {
    // path: '/create-article',
    path: '/articles/new/create',
    name: 'ArticleCreateView',
    component: ArticleCreateView,
    // meta: {
    //   requiresAuth: true
    // }
  },

  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
  },
  // 프로필 페이지 - 로그인 필요
  {
    path: '/profile/:username',
    name: 'profile',
    component: ProfileView,
    // meta: {
    //   requiresAuth: true
    // }
  },

  {
    path: '*',
    redirect: '/404-not-found'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  // 로그인 여부
  const isLoggedIn = store.getters.isLoggedIn
  console.log('로그인?', isLoggedIn)

  // 로그인 필요한 페이지 지정
  // 게시글 수정, 생성 페이지
  const authPages = ['ArticleUpdateView', 'ArticleCreateView', 'ProfileView']

  // 이동할 페이지가 로그인이 필요한 페이지인가?
  const isAuthRequired = authPages.includes(to.name)

  // 로그인 필요한데 로그인 안 되었을 경우
  if (isAuthRequired && !isLoggedIn) {
    alert('로그인이 필요한 페이지입니다.')
    next({
      name: 'login'
    })
  } else {
    next()
  }
})

// // 로그인 후 이전 페이지로 이동
// router.beforeEach((to, from, next) => {
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     // 인증이 필요한 라우트
//     if (!store.getters.isLoggedIn) {
//       // 로그인이 되어있지 않을 경우
//       next({
//         name: 'login'
//       })
//     } else {
//       // 로그인이 되어있을 경우
//       next()
//     }
//   } else {
//     // 인증이 필요하지 않은 라우트
//     next()
//   }
// })

// // 로그인 후 원래 가려던 페이지로 이동하게 하고싶은데 안된다 다음에 다시 보기
// let isInitialNavigation = true    // 초기 페이지 로드 여부 확인 변수

// router.beforeEach((to, from, next) => {
//   console.log('로그인?', store.getters.isLoggedIn)
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     // 인증이 필요한 라우트
//     if (!store.getters.isLoggedIn) {
//       // 로그인되지 않은 경우
//       if (isInitialNavigation) {
//         store.dispatch('setRedirectPath', to.path)
//         console.log('이동할 경로', to.path)
//         isInitialNavigation = false
//       } else {
//         isInitialNavigation = true
//       }
//       next({
//         name: 'login'
//       })
//     } else {
//       // 로그인이 되어있을 경우
//       next()
//     }
//   } else {
//     // 인증이 필요하지 않은 라우트
//     next()
//   }
// })


export default router
