<template>
  <v-row>
    <v-col>
      <v-row>
        <v-col>
          <v-select
            :items="categoriesAll"
            label="분류별 보기"
            dense
            solo
            hint="분류를 선택해주세요."
            v-model="selectedCategory"
          ></v-select>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="auto">
          <v-btn @click="download()">
            <v-icon
              color="primary"
            >mdi-file-excel</v-icon>
            엑셀로 다운받기
          </v-btn>
        </v-col>
      </v-row>
      <v-simple-table
      >
        <template v-slot:default  v-if="selectedArticles.length !== 0">
          <thead>
            <tr class="primary">
              <th class="white--text text-center id-col">
                글번호
              </th>
              <th class="white--text text-center category-col">
                분류
              </th>
              <th class="white--text text-center title-col">
                제목
              </th>
              <th class="white--text text-center writer-col">
                작성자
              </th>
              <th class="text-center like-col">            
              </th>
            </tr>
          </thead>
          <tbody>
            <ArticleItem
              v-for="article in selectedArticles"
              :key="article.id" 
              :article="article"
            />
          </tbody>
        </template>
        <template v-slot:default v-else>
          <thead>
            <tr>
              <th class="text-center id-col">
                글번호
              </th>
              <th class="text-center category-col">
                분류
              </th>
              <th class="text-center title-col">
                제목
              </th>
              <th class="text-center writer-col">
                작성자
              </th>
              <th class="text-center like-col">            
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colspan="5" class="text-center">
                게시글을 작성해주세요.
              </td>
            </tr>
          </tbody>
        </template>      
      </v-simple-table>
    </v-col>
  </v-row>
</template>

<script>
// import axios from 'axios'
import ArticleItem from '@/components/community/ArticleItem.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'ArticleListView',
  components: {
    ArticleItem,
  },
  data() {
    return {
      selectedCategory: '전체',
    }
  },
  computed: {
    ...mapGetters(['articles', 'categoriesAll']),

    // 분류별 필터 적용
    selectedArticles() {
      if (this.selectedCategory === '전체') {
        return this.articles
      } else {
        return this.articles.filter((article) => {
          return article.category === this.selectedCategory
        })
      }
    }
  },
  created() {
    // 게시글 정보 가져와서 state에 저장
    this.getArticles()
  },
  methods: {
    getArticles() {
      this.$store.dispatch('getArticles')
    },
    download(fileName, sheetName, sheetHtml) {
      var html = '';
      html += '<html xmlns:x="urn:schemas-microsoft-com:office:excel">';
      html += '    <head>';
      html += '        <meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8">';
      html += '        <xml>';
      html += '            <x:ExcelWorkbook>';
      html += '                <x:ExcelWorksheets>';
      html += '                    <x:ExcelWorksheet>'
      html += '                        <x:Name>' + sheetName + '</x:Name>';   // 시트이름
      html += '                        <x:WorksheetOptions><x:Panes></x:Panes></x:WorksheetOptions>';
      html += '                    </x:ExcelWorksheet>';
      html += '                </x:ExcelWorksheets>';
      html += '            </x:ExcelWorkbook>';
      html += '        </xml>';
      html += '    </head>';
      html += '    <body>';
      
      // ----------------- 시트 내용 부분 -----------------
      html += sheetHtml;
      // ----------------- //시트 내용 부분 -----------------
      
      html += '    </body>';
      html += '</html>';
      
      // 데이터 타입
      var data_type = 'data:application/vnd.ms-excel';
      console.log(data_type)
      var ua = window.navigator.userAgent;
      var blob = new Blob([html], {type: "application/csv;charset=utf-8;"});
      
      if ((ua.indexOf("MSIE ") > 0 || !!navigator.userAgent.match(/Trident.*rv:11\./)) && window.navigator.msSaveBlob) {
        // ie이고 msSaveBlob 기능을 지원하는 경우
        navigator.msSaveBlob(blob, fileName);
      } else {
        // ie가 아닌 경우 (바로 다운이 되지 않기 때문에 클릭 버튼을 만들어 클릭을 임의로 수행하도록 처리)
        var anchor = window.document.createElement('a');
        anchor.href = window.URL.createObjectURL(blob);
        anchor.download = fileName;
        document.body.appendChild(anchor);
        anchor.click();
        
        // 클릭(다운) 후 요소 제거
        document.body.removeChild(anchor);
      }
    },
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
</style>