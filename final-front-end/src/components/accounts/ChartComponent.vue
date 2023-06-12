<template>
  <v-container>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <!-- 최고금리, 기본금리 그래프 -->
        <canvas ref="chartCanvas"></canvas>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import Chart from 'chart.js';
import axios from 'axios'
import api from '@/api'
import { mapGetters } from 'vuex'

export default {
  mounted() {
    this.fetchChartData();
  },
  computed: {
    ...mapGetters([ 'authHeader', 'currentUser' ]),
    username() {
      return this.$route.params.username
    }
  },
  methods: {
    fetchChartData() {
      axios({
        method: 'GET',
        url: api.accounts.chart(this.username),
        headers: this.authHeader,
      })
        .then(response => {
          const chartData = response.data;
          console.log(chartData)

          const chartCanvas = this.$refs.chartCanvas;
          const ctx = chartCanvas.getContext('2d');

          // Create the chart using Chart.js
          new Chart(ctx, {
            type: 'bar', // Set the chart type (e.g., bar, line, pie)
            data: {
              labels: chartData.labels, // Array of chart labels
              datasets: [
                // data에 오는 건 최고금리, data2는 기본금리
                // 색상 https://carriedata.tistory.com/entry/Chartjs%EB%A1%9C-%EA%B7%B8%EB%9E%98%ED%94%84-%EB%A7%8C%EB%93%A4%EA%B8%B0 참고
                // https://www.flatuicolorpicker.com/
                {
                  label: '최고금리', // Dataset label
                  data: chartData.data, // Array of chart values
                  backgroundColor: 'rgba(75, 192, 192, 0.7)', // Background color for the bars
                  // backgroundColor: 'rgba(255, 99, 132, 0.5)'
                },
                {
                  label: '기본금리', // Dataset label
                  data: chartData.data2, // Array of chart values
                  backgroundColor: 'rgba(54, 162, 235, 0.6)'
                },
              ],
            },
            options: {
              title: {
                display: true,
                text: '가입 상품의 최고 금리 & 기본 금리',
                fontSize: 20,
                fontColor: 'rgba(46, 49, 49, 1)',
              },
              responsive: true,
              scales: {
                xAxes: [{
                  // 눈금 구성
                  ticks: {
                    fontColor: 'rgba(4, 59, 92, 1);'
                  }
                }],
                yAxes: [{
                  ticks: {
                    beginAtZero: true,
                  }
                }],
                y: {
                  max: 10,
                  reverse: true,    // 상향 성장
                }
              },
              animation: {
                duration: 3000, // 애니메이션 지속 시간(ms)
                easing: 'easeInOutQuart' // Animation easing function
              }
            },
          })
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
/* Add CSS styling for the chart if needed */
</style>
