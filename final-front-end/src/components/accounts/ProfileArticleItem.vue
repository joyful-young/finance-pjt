<template>
  <tr>
    <td class="text-center category-col">
      [{{ article.category }}]
    </td>
    <td class="text-center title-col">
      <router-link :to="{
        name: 'ArticleDetailView',
        params: { 'articleId': article.id }
      }">
        {{ shortTitle }}
      </router-link>
    </td>
    <td class="text-center like-col">
      {{ article.like_count }}
    </td>
    <td class="text-center comment-col">
      {{ article.comment_count }}
    </td>
  </tr>
</template>

<script>
export default {
  name: 'ProfileArticleItem',
  props: {
    article: Object,
  },
  computed: {
    shortTitle() {
      if (this.article.title.length > 30) {
        return this.article.title.substring(0, 30) + '...'
      } else {
        return this.article.title
      }
    },
  }
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