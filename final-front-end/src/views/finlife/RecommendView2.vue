<template>
  <div class="background-container">
    <v-container fluid>
      <v-row align="center" justify="center">
        <v-col cols="12">
          <template v-if="isLoading">
            <v-progress-linear indeterminate color="primary"></v-progress-linear>
          </template>
          <RecommendAlert v-else-if="jongryu === 0"
            :msg="msg"
            type="profile"
          >
          </RecommendAlert>
          <RecommendAlert v-else-if="jongryu === 1"
            :msg="msg"
            type="community"
          >
          </RecommendAlert>
          <template v-else-if="!(differenceField === '')">
            <v-card class="transparent-card">
              <v-card-title class="title"> 상위 3%의 포트폴리오와 가장 큰 차이는</v-card-title>

              <RecommendResult
              :differenceField="differenceField"
              />
              <!-- <v-card-text class="field">{{ getRecommendationText() }}</v-card-text> -->
              
            </v-card>
          </template>
        </v-col>
      </v-row>
    </v-container>
  </div>
  
</template>

<script>
import axios from 'axios';
import api from '@/api';
import { mapGetters } from 'vuex';
import RecommendAlert from '@/components/RecommendAlert.vue'
import RecommendResult from '@/components/RecommendResult.vue'

export default {
  data() {
    return {
      differenceField: '',
      msg: '',
      jongryu: '',
      isLoading: false,
    };
  },
  components: {
    RecommendAlert,
    RecommendResult
  },
  computed: {
    ...mapGetters(['currentUser', 'authHeader']),
  },
  created() {
    this.fetchRecommendation();
  },
  methods: {
    async fetchRecommendation() {
      this.isLoading = true;
      try {
        const response = await axios({
          method: 'GET',
          url: api.becomesuperrich.portfoliorecommend(),
          headers: this.authHeader,
        });
        this.differenceField = response.data.field;
        console.log(response);
        this.msg = response.data.msg;
        this.jongryu = response.data.jongryu;
        this.isLoading = false;
      } catch (error) {
        console.error('Error fetching recommendation:', error);
        this.isLoading = false;
      }
    },
    getRecommendationText() {
      if (this.differenceField =='loan_amount') {
        return '대출입니다. \n 대출은 자산 증식을 위한 전략적인 선택입니다.'
      }
      else if (this.differenceField == 'cash_equivalents_amount') {
        const wantRecommend = confirm('추천받으시겠습니까?')
        if (wantRecommend) {
          return 'axios 요청 보내기'
        }
        return '캐시'
      }
      else if (this.differenceField == 'bond_amount') {
        return '채권'

      }
      else if ( this.differenceField == 'stock_amount'){
        return '주식'
      }
    },
  },
};
</script>

<style>
.transparent-card {
  background-color: transparent !important;
  box-shadow: none !important;
}


.background-container {
  background-image: url('@/assets/image/AI.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  height: 100vh; /* Adjust the height if needed */
}

.title {
  font-size: 40px;
  font-weight: bold;
  text-align: center;
  margin-top: 100px;
  margin-bottom: 10px;
}

.field {
  font-size: 40px;
  text-align: center;
}

@keyframes appear {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}



</style>
