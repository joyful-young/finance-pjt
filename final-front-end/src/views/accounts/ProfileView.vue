<template>
  <v-container>
    <!-- 위 수정 -->
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <v-row v-if="userdata">
          <v-col>
            <v-card  variant="tonal">
              <v-card-title class="indigo white--text text-h5">
                {{ userdata?.username }}의 프로필
              </v-card-title>
            
              <v-card-text>
                <!-- <v-avatar
                  v-if="profile.avatar"
                  size="88"
                >
                  <v-img
                    :src="getRandomAvatarUrl()" class="mb-6"
                  ></v-img>
                </v-avatar> -->
                <h3 class="text-h5 font-weight-bold my-2 ml-2">
                  {{ userdata.username }}
                </h3>
                <div class="blue--text my-2 ml-2">
                  {{ userdata.email }}
                </div>
                <div class="blue--text font-weight-bold ml-2">
                  {{ userdata.region }}
                </div>
              </v-card-text>
              <v-card-subtitle class="text-center">
                <v-row>
                  <v-col>
                    <p>게시글</p>
                    <p>{{ userdata.articles.length }}</p>
                  </v-col>
                  <v-col>
                    <p>팔로워</p>
                    <p>{{ followers }}</p>
                  </v-col>
                  <v-col>
                    <p>팔로잉</p>
                    <p>{{ followings }}</p>
                  </v-col>
                </v-row>
              </v-card-subtitle>

              <v-row class="text-center">
                <v-col>
                  <v-btn v-if="currentUsername !== username" @click="followUser()">
                    <v-icon left>{{ followIcon }}</v-icon>{{ followBtn }}</v-btn>
                  <v-btn v-if="currentUsername === username && !updateFlag" @click="goUpdate()"
                  color="indigo lighten-1 white--text"
                  >프로필 수정</v-btn>
                </v-col>
              </v-row>
            </v-card>
            <v-divider></v-divider>
          </v-col>
        </v-row>

        <div v-if="userdata">

          <v-row v-if="!updateFlag">
            <v-col>
              <v-card>
                <v-row>
                  <v-col
                    class="text-right mb-1"
                    tag="strong"
                    cols="6"
                  >
                    이름 : 
                  </v-col>
                  <v-col
                    cols="6"
                  >
                    {{ userdata.realname }}
                  </v-col>
                  <v-col
                    class="text-right mb-1"
                    tag="strong"
                    cols="6"                
                  >
                    성별 : 
                  </v-col>
                  <v-col
                    cols="6"
                  >
                    {{ userdata.sex }}
                  </v-col>
                  <v-col
                    class="text-right mb-1"
                    tag="strong"
                    cols="6"
                  >
                    나이 : 
                  </v-col>
                  <v-col
                    cols="6"
                  >
                    {{ userdata.age }}
                  </v-col>
                  <v-col v-if="currentUsername === username"
                    class="text-right mb-1"
                    tag="strong"
                    cols="6"
                  >
                    수입 : 
                  </v-col>
                  <v-col v-if="currentUsername === username"
                    cols="6"
                  >
                    {{ userdata.income }} 만원
                  </v-col>
                  <v-col v-if="currentUsername === username"
                    class="text-right mb-1"
                    tag="strong"
                    cols="6"
                  >
                    가용 자산 : 
                  </v-col>
                  <v-col v-if="currentUsername === username"
                    cols="6"
                  >
                    {{ userdata.ready_money }} 만원
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </div>


        <div v-if="!updateFlag">
          <div v-if="profile">
            <!-- 기본 정보 -->
            <!-- 게시글 좋아요 순 -->
            <v-row>
              <v-col>
                <ProfileArticleList
                  :articles="userdata.articles"
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

        
        <v-row>
          <v-col>
            <v-card v-if="updateFlag">
              <v-form @submit.prevent>
                <div>
                  <v-label for="name">이름 : </v-label>
                  <v-text-field id="name" type="text" v-model="userdata.realname" required></v-text-field>
                </div>
                <div>
                  <v-label for="email">이메일 : </v-label>
                  <v-text-field id="email" type="email" v-model="userdata.email" required></v-text-field>
                </div>

                <div>
                  <v-label for="region">지역 : </v-label>
                  <v-select id="region" v-model="profile.region" :items="items" label="지역"></v-select>
                </div>

                <div>
                  <v-label for="sex">성별 : </v-label>
                  <v-select id="sex" v-model="profile.sex" :items="genderChoices" label="성별"></v-select>
                </div>

                <div>
                  <v-label for="age">나이 : </v-label>
                  <v-text-field id="age" type="number" min="0" v-model="userdata.age"></v-text-field>
                </div>
                <div>
                  <v-label for="income">수입 (만원) : </v-label>
                  <v-text-field id="income" type="number" min="0" v-model="userdata.income"></v-text-field>
                </div>
                <div>
                  <v-label for="ready-money">가용 자산 (만원) : </v-label>
                  <v-text-field id="ready-money" type="number" min="0" v-model="userdata.ready_money"></v-text-field>
                </div>

                <div>
                  <v-label for="stock_amount">주식 (만원) : </v-label>
                  <v-text-field id="stock_amount" type="number" min="0" v-model="profile.stock_amount"></v-text-field>
                </div>
                <div>
                  <v-label for="bond_amount">채권 (만원) : </v-label>
                  <v-text-field id="bond_amount" type="number" min="0" v-model="profile.bond_amount"></v-text-field>
                </div>
                <div>
                  <v-label for="loan_amount">대출 (만원) : </v-label>
                  <v-text-field id="loan_amount" type="number" min="0" v-model="profile.loan_amount"></v-text-field>
                </div>
                <div>
                  <v-label for="cash_equivalents_amount">현금성 자산 (만원) : </v-label>
                  <v-text-field id="cash_equivalents_amount" type="number" min="0" v-model="profile.cash_equivalents_amount"></v-text-field>
                </div>
                <v-row class="text-center">
                  <v-col>
                    <v-btn @click="updateProfile" color="indigo lighten-1 white--text">수정</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
        <!-- 수정 부분 끝 -->
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
      userdata: null,       // 유저 정보. 여기 프로필 객체 포함되어 있음
      profile: null,        // 프로필 수정을 위한 유저 프로필 객체 따로 받기
      updateFlag: false,    // 수정할건
      items: [
        "서울",
        "부산",
        "대구",
        "인천",
        "광주",
        "대전",
        "울산",
        "경기",
        "강원",
        "충청",
        "전라",
        "경상",
        "제주",
        "세종"
      ],
      genderChoices: [
        "남성",
        "여성"
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
    followIcon() {
      return this.followFlag ? 'mdi-account-check' : 'mdi-account-plus'
    },
    likeDeposits() {
      return this.userdata.like_deposit_list
    },
    likeInstallments() {
      return this.userdata.like_saving_list
    },
    joinDeposits() {
      return this.userdata.registered_deposit_list
    },
    joinInstallments() {
      return this.userdata.registered_saving_list
    },
    property_amount() {
      return this.profile.stock_amount + this.profile.bond_amount + this.profile.loan_amount + this.profile.cash_equivalents_amount
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
     getRandomAvatarUrl() {
      // Generate a random number to use in the avatar URL

      // Return the URL with the random number
      return `https://avataaars.io/`;
     },
    async fetchProfileData(username) {
      try {
        const response = await axios({
          method: 'GET',
          url: api.accounts.profileData(username),
          headers: this.authHeader
        })
        console.log(response)
        // response.data에 유저 데이터
        const userdata = response.data
        this.userdata = userdata
        // userdata 객체 안에 profile 객체
        const profile = response.data.profile
        this.profile = profile
        // 현재 유저의 프로필 유저 팔로우 여부
        this.followFlag = userdata.is_following
        // 프로필 유저 팔로워 수
        this.followers = userdata.follower_count
        // 프로필 유저 팔로잉 수
        this.followings = userdata.following_count

      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    goUpdate() {
      this.updateFlag = true
    },
    async updateProfile() {
      try {
        const response = await axios({
          method: 'PUT',
          url: api.accounts.profileUpdate(this.username),
          data: {
            ...this.profile,
            property_amount: this.property_amount,
          },
          headers: this.authHeader,
        })
        console.log(response)
        this.updateFlag = false
      } catch (error) {
        console.log(error)
        console.error('Error updating profile:', error);
      }
    },
    async followUser() {
      // 본인 팔로우는 버튼에서 거름
      try{
        const response = await axios({
          method: 'POST',
          url: api.accounts.userFollow(this.username),
          headers: this.authHeader,
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