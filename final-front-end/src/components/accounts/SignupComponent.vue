<template>
  <v-container>
    <v-form
      class="mt-7"
      @submit.prevent="signUp()"
    >
      <!-- 아이디 -->
      <v-row class="justify-center">
        <v-col cols="10" sm="6" lg="4">
          <v-row class="justify-between">
            <v-col cols="9">
              <v-text-field
                v-model.trim="form.username"
                :rules="[rules.required]"
                label="아이디"
                @change="needCheck()"
              ></v-text-field>
            </v-col>
            <v-col class="d-flex align-center justify-end">
              <v-btn
                icon
                v-show="isChecked"
              >
                <v-icon>mdi-check-circle</v-icon>
              </v-btn>
              <v-btn
                icon
                v-show="!isChecked"
                @click="checkDuplicate()"
              >
                <v-icon>mdi-check-circle-outline</v-icon>
              </v-btn>
            </v-col>

          </v-row>
        </v-col>
      </v-row>
      <!-- 비밀번호 -->
      <v-row class="justify-center">
        <v-col cols="10" sm="6" lg="4">
          <v-text-field
            v-model.trim="form.password1"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.password]"
            :type="show1 ? 'text' : 'password'"
            label="비밀번호"
            hint="숫자와 문자를 각각 하나 이상 포함해서 8자 이상 작성하세요"
            @click:append="show1 = !show1"
            @change="checkPasswordValidity()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="10" sm="6" lg="4">
          <v-text-field
            v-model.trim="form.password2"
            :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.checkpassword]"
            :type="show2 ? 'text' : 'password'"
            label="비밀번호확인"
            hint="숫자와 문자를 각각 하나 이상 포함해서 8자 이상 작성하세요"
            @click:append="show2 = !show2"
            @change="checkPasswordSame()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="10" sm="6" lg="4">
          <v-text-field
            v-model.trim="form.realname"
            :rules="[rules.required]"
            label="이름"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="10" sm="6" lg="4">
          <v-text-field
            v-model.trim="form.email"
            :rules="[rules.required, rules.email]"
            label="이메일"
            type="email"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="justify-center">
        <v-col cols="10" sm="6" lg="4">
          <v-btn @click="signUp()">SignUp</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
  <!-- <div>
    <form @submit.prevent>


      <div>
        <label for="password2">비밀번호 확인</label><br>
        <input id="password2" 
        @blur="checkPasswordSame()"
        @change="checkPasswordSame()" type="password" placeholder="비밀번호" v-model="form.password2">
        <p v-show="!isPasswordSame">
          비밀번호가 일치하지 않습니다.
        </p>
      </div>


    </form>
  </div> -->
</template>

<script>
import axios from 'axios'
import api from '@/api'

export default {
  name: 'SignupComponent',
  data() {
    return {
      form: {
        username: '',
        password1: '',
        password2: '',
        realname: '',
        email: '',
      },
      isPasswordValid: true,
      isPasswordSame: true,
      isChecked: false, // 아이디 중복체크 했나,
      show1: false,
      show2: false,
      rules: {
        required: value => !!value || '필수 입력 항목입니다.',
        email: v => !!(v || '').match(/@/) || '올바른 이메일 형식으로 입력해주세요.',
        password: v => !!(v || '').match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$/) || '비밀번호는 숫자와 문자를 각각 1개 이상 포함하고 8글자 이상이어야 합니다.',
        checkpassword: v => v === this.form.password1 || '비밀번호를 확인해주세요.'
      }
    }
  },
  methods: {
    // 아이디가 바뀌면 중복체크 필요
    needCheck() {
      this.isChecked = false
    },
    checkDuplicate() {
      if (this.form.username === '') {
        alert('아이디를 입력해주세요.')
        return
      }
      axios.get(api.accounts.checkDuplicate(this.form.username))
      .then((response) => {
        if (response.data.msg === 'NO') {
          alert('중복된 아이디입니다.')
        } else {
          alert('사용가능한 아이디입니다.')
          this.isChecked = true
        }
      })
      .catch((error) => {
        console.log(error)
      })
    },
    checkPasswordValidity() {
      // 비밀번호 형식 맞는지 검사
      // 숫자와 문자를 1개 이상 포함하고 8글자 이상, 특수문자는 옵션
      const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$/;
      this.isPasswordValid = passwordPattern.test(this.form.password1)
    },
    checkPasswordSame() {
      // password1과 일치하는지 검사
      if (this.form.password1 !== this.form.password2) {
        this.isPasswordSame = false
      } else {
        this.isPasswordSame = true
      }
    },
    signUp() {
      if (!this.isChecked) {
        alert('아이디 중복확인을 해주세요.')
        return
      }
      // 먼저 유효성 검사 - 입력 되었는가?

      // 아이디 입력 확인
      if (this.form.username === '') {
        alert('아이디를 입력하세요!')
        return
      }
      // 비밀번호 입력 확인
      if (this.form.password1 === '') {
        alert('비밀번호를 입력하세요!')
        return
      }
      // 비밀번호 일치 확인
      if (!this.isPasswordSame || !this.isPasswordValid) {
        alert('비밀번호를 확인해주세요!')
        return
      }
      if (this.form.password1 !== this.form.password2) {
        alert('비밀번호를 확인해주세요!')
        return
      }
      // 이름 입력 확인
      if (this.form.realname === '') {
        alert('이름을 입력해주세요!')
        return
      }
      // 이메일 입력 확인
      if (this.form.email === '') {
        alert('이메일을 입력해주세요!')
        return
      }

      this.$store.dispatch('signUp', this.form)
    }
  }
}
</script>

<style>

</style>