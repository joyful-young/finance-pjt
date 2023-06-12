<template>
  <v-container>
    <v-row v-if="deposit" class="">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <v-row>
          <v-col>
            <v-btn class="mt-1">
              <router-link :to="{ name: 'deposit'}">
                <v-icon left>mdi-arrow-left</v-icon>
                목록 보기
              </router-link>
            </v-btn>
          </v-col>
        </v-row>

        <v-row class="modal-overlay justify-space-between">
          <v-col class="">
            <v-img :src="bankLogo" :alt="deposit.kor_co_nm + ' logo'"
            max-height="100"
            max-width="100"
            class="ma-3"
            ></v-img>

            <h4>{{ deposit.kor_co_nm }}</h4>
            <h2>{{ deposit.fin_prdt_nm }}</h2>
          </v-col>
          <v-spacer></v-spacer>
          <v-col class="d-flex align-end justify-end">
            <v-btn @click="likeDeposit(deposit.fin_prdt_cd)"
            class="ma-1"
            :color="likeFlag ? 'primary' : 'gray'"
            >
              <v-icon left>{{ likeBtn }}</v-icon>
              {{ likeCount }}
            </v-btn>
            <v-btn @click="joinDeposit(deposit.fin_prdt_cd)"
            class="ma-1"
            :color="joinFlag ? 'primary' : 'gray'"
            >
              <v-icon left>{{ joinBtn }}</v-icon>
              {{ joinCount }}  
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p>{{ deposit.etc_note }}</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <ul>
              <li>가입 대상 : {{ deposit.join_member }}</li>
              <br>
              <li>가입 방법 : {{ deposit.join_way }}</li>
              <br>
              <li>우대 조건</li>
              <p>{{ deposit.spcl_cnd }}</p>
            </ul>
          </v-col>
        </v-row>
        <v-row class="text-center">
          <v-col>
            <div v-if="deposit.options.length !== 0">

              <v-btn-toggle v-model="picked"
                class="mb-3"
                color="primary accent-3"
              >
                <v-btn v-for="(option, index) in deposit.options" :key="option.id"
                  :value="index"
                >
                  {{ option.save_trm }}개월
                </v-btn>
              </v-btn-toggle>

              <DepositOption
              :option="deposit.options[picked]"
              />
            </div>
          </v-col>
        </v-row>
        <!-- <v-row class="text-center">
          <v-col>
            <v-dialog
              transition="dialog-bottom-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon left>mdi-calculator</v-icon>
                  이자 계산기
                </v-btn>
              </template>
              <template v-slot:default="dialog">
                <CalculatorModal/>
                <v-btn
                  text
                  @click="dialog.value = false"
                >
                  닫기
                </v-btn>
              </template>
            </v-dialog>
          </v-col>
        </v-row> -->
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>

    <v-row v-else>
      <v-col>
        <v-text-field
          color="primary"
          loading
          disabled
        ></v-text-field>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import DepositOption from '@/components/finlife/DepositOption.vue'
// import CalculatorModal from '@/components/finlife/CalculatorModal.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'DepositDetailView',
  components: {
    // CalculatorModal,
    DepositOption,
  },
  data() {
    return {
      deposit: null,
      isModalOpen: false,
      likeUsers: [],
      joinUsers: [],
      likeFlag: false,
      joinFlag: false,
      likeCount: '',
      joinCount: '',
      picked: null,
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'currentUser']),
    finPrdtCd() {
      return this.$route.params.finPrdtCd
    },
    bankLogo() {
      const bankImgUrlObj = this.$store.state.finlife.bankImgUrl
      const bank = this.deposit.kor_co_nm
      return bankImgUrlObj[bank] ? bankImgUrlObj[bank] : ''
    },
    likeBtn() {
      return this.likeFlag ? 'mdi-star' : 'mdi-star-outline'
    },
    joinBtn() {
      return this.joinFlag ? 'mdi-bank-check' : 'mdi-bank-plus'
    },
  },
  // 서버 상세조회 api 필요
  created() {
    this.getDepositDetail(this.finPrdtCd)
  },
  methods: {
    openModal() {
      this.isModalOpen = true
    },
    closeModal() {
      this.isModalOpen = false
    },
    async getDepositDetail(finPrdtCd) {
      try {
        const response = await this.$store.dispatch('getDepositDetail', finPrdtCd)
        // 컴포넌트 데이터에 저장
        this.deposit = response
        this.likeFlag = response.liked_by_user
        this.joinFlag = response.registered_by_user
        this.likeCount = this.deposit.like_deposit_count
        this.joinCount = this.deposit.register_deposit_count
        this.picked = 0
      } catch(error) {
        console.log(error)
      }
    },
    likeDeposit(finPrdtCd) {
      this.$store.dispatch('likeDeposit', finPrdtCd)
      .then(() => {
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
    },
    joinDeposit(finPrdtCd) {
      this.$store.dispatch('joinDeposit', finPrdtCd)
      .then(() => {
        if (this.joinFlag) {
          this.joinCount -= 1
        } else {
          this.joinCount += 1
        }
        this.joinFlag = !this.joinFlag
      })
      .catch((error) => {
        console.log(error)
      })
    },
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 10000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  position:fixed;
  bottom: 0;
  width: 100%;
  height: 50%;
  background-color: #fff;
  padding: 20px;
  border-radius: 20px;
}

ul > li {
  font-weight: bold;
}
</style>