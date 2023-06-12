<template>
  <v-container>
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <v-row>
          <v-col>
            <h2>{{ profile?.username }}의 Profile</h2>
            <p>팔로워: {{ followers }}</p>
            <p>팔로잉: {{ followings }}</p>
            <v-btn v-if="currentUsername !== username" @click="followUser()">{{ followBtn }}</v-btn>
            <v-btn v-if="currentUsername === username" @click="goUpdate()">프로필 수정</v-btn>
          </v-col>
        </v-row>

        <div v-if="!updateFlag">
          <div v-if="profile">
            <!-- 기본 정보 -->
            <v-row>
              <v-col>
                <p>Name: {{ profile.realname }}</p>
                <p>Email: {{ profile.email }}</p>
                <p>region: {{ profile.region }}</p>
                <p>sex: {{ profile.sex }}</p>
                <p>age: {{ profile.age }}</p>
                <p>income: {{ profile.income }}</p>
                <p>ready_money: {{ profile.ready_money }}</p>
                <!-- <p>like_comments: {{ profile.like_comments }}</p>
                <p>like_articles: {{ profile.like_articles }}</p> -->
              </v-col>
            </v-row>
            <!-- 게시글 좋아요 순 -->
            <v-row>
              <v-col>
                <ProfileArticleList
                  :articles="profile.articles"
                />
              </v-col>
            </v-row>
            <!-- 찜한 상품 -->
            <v-row>
              <v-col>
                <h3>찜한 상품</h3>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4" v-for="deposit in likeDeposits" :key="deposit.id">
                <LikeProductItem
                  :product="deposit"
                  type="deposit"
                />
              </v-col>
              <v-col cols="4" v-for="installment in likeInstallments" :key="installment.id">
                <LikeProductItem
                  :product="installment"
                  type="installment"
                />
              </v-col>
            </v-row>
            <!-- 가입 상품 -->
            <v-row>
              <v-col>
                <h3>가입한 상품</h3>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4" v-for="deposit in joinDeposits" :key="deposit.id">
                <JoinProductItem
                  :product="deposit"
                  type="deposit"
                />
              </v-col>
              <v-col cols="4" v-for="installment in joinInstallments" :key="installment.id">
                <JoinProductItem
                  :product="installment"
                  type="installment"
                />
              </v-col>                        
            </v-row>
          </div>
        </div>
        <!-- 여기서부턴 수정 시 나오는 부분 -->
        <div v-if="updateFlag">
          <form @submit.prevent>
            <div>
              <label for="name">name</label>
              <input id="name" type="text" v-model="profile.realname" required>
            </div>
            <div>
              <label for="email">email</label>
              <input id="email" type="email" v-model="profile.email" required>
            </div>

            <div>
              <label for="region">Region</label>
              <select id="region" v-model="profile.region">
                <option v-for="region in regionChoices" :key="region.value" :value="region.value">
                  {{ region.label }}
                </option>
              </select>
            </div>
            <div>
              <label for="sex">Sex</label>
              <select id="sex" v-model="profile.sex">
                <option v-for="gender in genderChoices" :key="gender.value" :value="gender.value">
                  {{ gender.label }}
                </option>
              </select>
            </div>



            <div>
              <label for="age">age</label>
              <input id="age" type="number" min="0" v-model="profile.age">
            </div>
            <div>
              <label for="income">income</label>
              <input id="income" type="number" min="0" v-model="profile.income">
            </div>
            <div>
              <label for="ready-money">ready-money</label>
              <input id="ready-money" type="number" min="0" v-model="profile.ready_money">
            </div>
            <div>
              좋아요 게시글, 예금 리스트, 적금 리스트는 다른 방식으로 출력해야 함
            </div>
            <div>
              가입한 상품 리스트는 다른 방식으로 출력
            </div>
            <button @click="updateProfile">수정</button>
          </form>
        </div>
        <!-- 수정 부분 끝 -->

        <!-- <v-row>
          <v-col>
            <div v-if="!updateFlag">
              <div v-if="profile">
                <p>Name: {{ profile.realname }}</p>
                <p>Email: {{ profile.email }}</p>
                <p>region: {{ profile.region }}</p>
                <p>sex: {{ profile.sex }}</p>
                <p>age: {{ profile.age }}</p>
                <p>income: {{ profile.income }}</p>
                <p>ready_money: {{ profile.ready_money }}</p>
                <p>like_comments: {{ profile.like_comments }}</p>
                <p>like_articles: {{ profile.like_articles }}</p>
              </div>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div v-if="!updateFlag">
              <div v-if="profile">
                <p>찜한 상품</p>
                <div v-for="deposit in likeDeposits" :key="deposit.id">
                  <LikeProductItem
                    :product="deposit"
                    type="deposit"
                  />
                </div>
                <div v-for="installment in likeInstallments" :key="installment.id">
                  <LikeProductItem
                    :product="installment"
                    type="installment"
                  />
                </div>

                <p>가입 중인 상품</p>
                <div v-for="deposit in joinDeposits" :key="deposit.id">
                  <JoinProductItem
                    :product="deposit"
                    type="deposit"
                  />
                </div>
                <div v-for="installment in joinInstallments" :key="installment.fin_prdt_nm">
                  <JoinProductItem
                    :product="installment"
                    type="installment"
                  />
                </div>                
              </div>
              <div v-if="currentUsername === username">
                <button @click="goUpdate()">프로필 수정</button>
              </div>
            </div>
            <div v-if="updateFlag">
              <form @submit.prevent>
                <div>
                  <label for="name">name</label>
                  <input id="name" type="text" v-model="profile.realname" required>
                </div>
                <div>
                  <label for="email">email</label>
                  <input id="email" type="email" v-model="profile.email" required>
                </div>

                <div>
                  <label for="region">Region</label>
                  <select id="region" v-model="profile.region">
                    <option v-for="region in regionChoices" :key="region.value" :value="region.value">
                      {{ region.label }}
                    </option>
                  </select>
                </div>
                <div>
                  <label for="sex">Sex</label>
                  <select id="sex" v-model="profile.sex">
                    <option v-for="gender in genderChoices" :key="gender.value" :value="gender.value">
                      {{ gender.label }}
                    </option>
                  </select>
                </div>



                <div>
                  <label for="age">age</label>
                  <input id="age" type="number" min="0" v-model="profile.age">
                </div>
                <div>
                  <label for="income">income</label>
                  <input id="income" type="number" min="0" v-model="profile.income">
                </div>
                <div>
                  <label for="ready-money">ready-money</label>
                  <input id="ready-money" type="number" min="0" v-model="profile.ready_money">
                </div>
                <div>
                  좋아요 게시글, 예금 리스트, 적금 리스트는 다른 방식으로 출력해야 함
                </div>
                <div>
                  가입한 상품 리스트는 다른 방식으로 출력
                </div>
                <button @click="updateProfile">수정</button>
              </form>
            </div> -->
          <!-- </v-col>
        </v-row> -->
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
    <v-row>
      <v-col>
        <ChartComponent/>
      </v-col>
    </v-row>
  </v-container>


</template>

<script>
import axios from 'axios'
import api from '@/api'
import { mapGetters } from 'vuex'
import ChartComponent from '@/components/accounts/ChartComponent.vue'
import LikeProductItem from '@/components/accounts/LikeProductItem.vue'
import JoinProductItem from '@/components/accounts/JoinProductItem.vue'
import ProfileArticleList from '@/components/accounts/ProfileArticleList.vue'

export default {
  name: 'ProfileView',
  components: {
    ChartComponent,
    LikeProductItem,
    JoinProductItem,
    ProfileArticleList,
  },
  data() {
    return {
      profile: null,
      updateFlag: false,
      regionChoices: [
        { label: '서울', value: '서울' },
        { label: '경기', value: '경기' },
        { label: '인천', value: '인천' },
        { label: '부산', value: '부산' }
      ],
      genderChoices: [
        { label: '남성', value: '남성' },
        { label: '여성', value: '여성' }
      ],
      followFlag: false,  // 현재 유저가 팔로잉중인가
      followers: null,    // 팔로워 수
      followings: null,   // 팔로잉 수
    };
  },
  computed: {
    ...mapGetters(['currentUser', 'authHeader']),
    currentUsername() {
      return this.currentUser.username
    },
    username() {
      return this.$route.params.username
    },
    followBtn() {
      return this.followFlag ? '팔로우 취소' : '팔로우'
    },
    likeDeposits() {
      return this.profile.like_deposit_list
    },
    likeInstallments() {
      return this.profile.like_saving_list
    },
    joinDeposits() {
      return this.profile.registered_deposit_list
    },
    joinInstallments() {
      return this.profile.registered_saving_list
    }
  },
  created() {
    this.fetchProfileData(this.$route.params.username);
  },
  beforeRouteUpdate(to, from, next) {
    console.log(to.params.username)
    this.fetchProfileData(to.params.username)
    next()
  },
  methods: {
    async fetchProfileData(username) {
      try {
        const response = await axios({
          method: 'GET',
          url: api.accounts.profileData(username),
          headers: this.authHeader
        })
        console.log(response);
        const profile = response.data
        this.profile = profile
        // 현재 유저의 프로필 유저 팔로우 여부
        this.followFlag = profile.is_following
        // 프로필 유저 팔로워 수
        this.followers = profile.follower_count
        // 프로필 유저 팔로잉 수
        this.followings = profile.following_count
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    // 프론트에서 팔로워 유저 목록받아 현재 유저의 프로필 유저 팔로우여부 판단
    // async fetchProfileData(username) {
    //   try {
    //     const response = await axios({
    //       method: 'GET',
    //       url: api.accounts.profileData(username),
    //       headers: this.$store.getters.authHeader
    //     })
    //     console.log(response);
    //     this.profile = response.data;
    //     // 현재 유저의 프로필 유저 팔로우 여부
    //     this.followFlag = this.profile.is_following
    //   } catch (error) {
    //     console.error('Error fetching profile:', error);
    //   }
    // },
    goUpdate() {
      this.updateFlag = true
    },
    async updateProfile() {
      // Implement the logic for editing the profile here
      try {
        console.log('업뎃')
        const response = await axios({
          method: 'PUT',
          url: api.accounts.profileUpdate(this.username),
          data: {
            ...this.profile,
          },
          headers: this.$store.getters.authHeader,
        })
        console.log(response)
        this.updateFlag = false
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    async followUser() {
      // 본인 팔로우는 버튼에서 거름
      try{
        const response = await axios({
          method: 'POST',
          url: api.accounts.userFollow(this.username),
          headers: this.$store.getters.authHeader,
        })
        console.log(response)

        if (this.followFlag) {
          this.followers -= 1
        } else {
          this.followers += 1
        }

        this.followFlag = !this.followFlag
      } catch (error) {
        console.error('Error following user:', error);
      }
    }
  }
};
</script>