<template>
  <tr>
    <td class="id-col">
      {{ article.id }}
    </td>
    <td class="category-col">
      [{{ article.category }}]
    </td>
    <td class="title-col text-left">
      <router-link :to="{
        name: 'ArticleDetailView',
        params: { 'articleId': article.id }
      }">
        {{ shortTitle }}
      </router-link>
    </td>
    <td class="writer-col">
      <router-link :to="{ name: 'profile', params: { username: article.write_user }}">
        <span>{{ shortWriter }}</span>
      </router-link>
    </td>
    <td class="like-col align-center">
      <v-row>
        <v-col class="pb-0">
          좋아요<br>
          {{ article.like_count }}
        </v-col>
      </v-row>
      <v-row>
        <v-col class="pt-0">
          댓글 수<br>
          {{ article.comment_count }}
        </v-col>
      </v-row>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'ArticleItem',
  props: {
    article: Object,
  },
  computed: {
    shortTitle() {
      if (this.article.title.length > 50) {
        return this.article.title.substring(0, 50) + '...'
      } else {
        return this.article.title
      }
    },
    shortWriter() {
      if (this.article.write_user.length > 10) {
        return this.article.write_user.substring(0, 10) + '...'
      } else {
        return this.article.write_user
      }
    }
  }
}
</script>

<style scoped>
.id-col {
  width: 10%
}
.category-col {
  width: 15%;
}
.title-col {
  width: 45%;
}
.writer-col {
  width: 15%;
}
.like-col {
  width: 15%;
}
/* 제목 제외 가운데 정렬 */
td {
  text-align: center;
}
</style>