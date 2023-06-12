<template>
  <v-container>
    <v-form class="mt-7" @submit.prevent="login()">
      <v-row>
        <v-col cols="10" sm="6" lg="4" class="mx-auto">
          <v-text-field
            v-model="form.username"
            :rules="[rules.required]"
            label="아이디"
            @keyup.enter="login()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="10" sm="6" lg="4"
        class="mx-auto">
          <v-text-field
            v-model="form.password"
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.min]"
            :type="show ? 'text' : 'password'"
            label="비밀번호"
            hint="8자 이상이어야 합니다."
            counter
            @click:append="show = !show"
            @keyup.enter="login()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn @click="login()">Login</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>


  <!-- <div>
    <form @submit.prevent="login()">
      <div>
        <label for="username">아이디</label>
        <input id="username" type="text" v-model="form.username">
      </div>
      <div>
        <label for="password">비밀번호</label>
        <input id="password" type="password" v-model="form.password">
      </div>
      <button>Login</button>
    </form>
  </div> -->
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'LoginComponent',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      show: false,
      rules: {
        required: value => !!value || '필수 입력 항목입니다.',
        min: v => v.length >= 8 || '8자 이상 입력하세요',
      }
    }
  },
  computed: {
    ...mapGetters([ 'currentUser' ]),
    currentUsername() {
      return this.currentUser.username
    },
  },
  methods: {
    // login() {
    //   if (this.form.username === '') {
    //     alert('아이디를 입력하세요')
    //     return
    //   }

    //   if (this.form.password === '') {
    //     alert('비밀번호를 입력하세요')
    //     return
    //   }

    //   this.$store.dispatch('login', this.form)
    //   .then(() => {
    //     alert(`환영합니다. ${this.currentUsername}님!`)
    //   })
    //   .catch((error) => {
    //     console.log(error)
    //   })
    // },
    async login() {
      if (this.form.username === '') {
        alert('아이디를 입력하세요')
        return
      }

      if (this.form.password === '') {
        alert('비밀번호를 입력하세요')
        return
      }
      try {
        const response = await this.$store.dispatch('login', this.form)
        console.log(response)
        alert(`환영합니다. ${this.currentUsername}님!`)
        this.$router.go(-1)

      } catch (error) {
        console.log(error)
      }

    }
  }
}
</script>

<style>

</style>