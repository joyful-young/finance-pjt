<template>
  <v-container>
    <v-row>
      <v-col>
        <h3>좋아요 수 Top 5 게시물</h3>
      </v-col>
    </v-row>
    <v-simple-table
    >
      <template v-slot:default  v-if="articles.length !== 0">
        <thead>
          <tr>
            <th class="text-center category-col">
              분류
            </th>
            <th class="text-center title-col">
              제목
            </th>
            <th class="text-center like-col">
              좋아요 수
            </th>
            <th class="text-center comment-col">
              댓글 수
            </th>
          </tr>
        </thead>
        <tbody>
          <ProfileArticleItem
            v-for="article in top5Articles"
            :key="article.id" 
            :article="article"
          />
        </tbody>
      </template>
      <template v-slot:default v-else>
        <thead>
          <tr>
            <th class="text-center category-col">
              분류
            </th>
            <th class="text-center title-col">
              제목
            </th>
            <th class="text-center like-col">
              좋아요 수
            </th>
            <th class="text-center comment-col">
              댓글 수
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="4" class="text-center">
              작성한 글이 없습니다.
            </td>
          </tr>
        </tbody>
      </template>      
    </v-simple-table>
  </v-container>
</template>

<script>
import ProfileArticleItem from '@/components/accounts/ProfileArticleItem.vue'
import { mapGetters } from 'vuex'
import _ from 'lodash'

export default {
  name: 'ProfileArticleList',
  components: {
    ProfileArticleItem,
  },
  data() {
    return {
      selectedCategory: '전체',
    }
  },
  props: {
    articles: Array,
  },
  computed: {
    ...mapGetters(['categoriesAll']),
    sortedArticles() {
      return _.sortBy(this.articles, 'like_count').reverse()
    },
    top5Articles() {
      return this.sortedArticles.slice(0, 5)
    }

    // selectedArticles() {
    //   if (this.selectedCategory === '전체') {
    //     return this.articles
    //   } else {
    //     return this.articles.filter((article) => {
    //       return article.category === this.selectedCategory
    //     })
    //   }
    // },
    // top10Articles() {

    // }
  },
}
</script>

<style scoped>
.category-col {
  width: 15%;
}
.title-col {
  width: 55%;
}
.like-col {
  width: 15%;
}
.comment-col {
  width: 15%;
}
</style>