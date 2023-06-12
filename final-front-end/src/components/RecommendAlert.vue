<template>
  <v-container>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <v-alert
          v-model="alert"
          border="left"
          close-text="Close Alert"
          color="#64B5F6 accent-4"
          dark
          dismissible
        >
          {{ msg }}
        </v-alert>
        <div class="text-center">
          <v-btn
            v-if="!alert"
            color="#64B5F6 accent-4"
            dark
            @click="goTo"
          >
            {{ btnContent }}
          </v-btn>
          <!-- <v-btn>
            <router-link :to="{ name: 'profile', params: { username: currentUser?.username }}">

            </router-link>
          </v-btn> -->
        </div>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'RecommendAlert',
  props: {
    msg: String,
    type: String,
  },
  computed: {
    ...mapGetters(['currentUser']),
    btnContent() {
      if (this.type === 'profile') {
        return '프로필로 이동'
      } else {
        return '커뮤니티로 이동'
      }
    }
  },
  data() {
    return {
      alert: true,
    }
  },
  methods: {
    goTo() {
      if (this.type === 'profile') {
        this.$router.push({
          name: 'profile',
          params: {
            username: this.currentUser.username
          }
        })
      } else {
        this.$router.push({
          name: 'articles',
        })
      }
    }
  }
}
</script>

<style>

</style>