<template>
  <v-container>
    <v-row class="text-center mt-3">
      <v-col>
        <v-row align="center">
          <v-col cols="auto">
            <v-img
              src="@/assets/image/exchange.png"
              max-height="30"
              contain
              class="mr-1 d-inline-block"
              style="max-width: 45px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
            ></v-img>
            <h2 class="d-inline-block">Calculation of exchange rates</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-select
              v-model="conversionType"
              :items="conversionTypes"
              item-text="label"
              item-value="value"

              label="Conversion Type"
              solo
              @change="clearConversion"
            ></v-select>
          </v-col>
          <v-col>
            <v-select
              v-model="selectedCountry"
              :items="countries"
              item-text="name"
              item-value="code"
              label="Target Country"
              solo
              :disabled="!conversionType"
              @change="convertCurrency"
            ></v-select>
          </v-col>
          <v-col>
            <v-text-field
              type="number"
              v-model="amount"
              :label="conversionType === 'krw-to-foreign' ? '외화' : '한화'"
              :disabled="!selectedCountry"
              @keyup.enter="convertCurrency"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-btn @click="convertCurrency">환율 계산</v-btn>
          </v-col>
        </v-row>
        <p v-if="convertedAmount">Converted Amount: {{ result }}</p>
        <p v-if="error">{{ error }}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import _ from 'lodash'

import api from '@/api';
export default {
  data() {
    return {
      conversionType: '',
      selectedCountry: '',
      amount: '',
      convertedAmount: null,
      error: null,
      countries: [
        {name: "아랍에미리트 디르함", code: "AED"} ,
        {name: "오스트리아 실링", code: "ATS"} ,
        {name: "호주 달러", code: "AUD"} ,
        {name: "벨기에 프랑", code: "BEF"} ,
        {name: "바레인 디나르", code: "BHD"} ,
        {name: "캐나다 달러", code: "CAD"} ,
        {name: "스위스 프랑", code: "CHF"} ,
        {name: "위안화", code: "CNH"} ,
        {name: "독일 마르크", code: "DEM"} ,
        {name: "덴마아크 크로네", code: "DKK"} ,
        {name: "스페인 페세타", code: "ESP(100)"} ,
        {name: "유로", code: "EUR"} ,
        {name: "핀란드 마르카", code: "FIM"} ,
        {name: "프랑스 프랑", code: "FRF"} ,
        {name: "영국 파운드", code: "GBP"} ,
        {name: "홍콩 달러", code: "HKD"} ,
        {name: "인도네시아 루피아", code: "IDR(100)"} ,
        {name: "이태리 리라", code: "ITL(100)"} ,
        {name: "일본 옌", code: "JPY(100)"} ,
        {name: "한국 원", code: "KRW"} ,
        {name: "쿠웨이트 디나르", code: "KWD"} ,
        {name: "말레이지아 링기트", code: "MYR"} ,
        {name: "네델란드 길더", code: "NLG"} ,
        {name: "노르웨이 크로네", code: "NOK"} ,
        {name: "뉴질랜드 달러", code: "NZD"} ,
        {name: "사우디 리얄", code: "SAR"} ,
        {name: "스웨덴 크로나", code: "SEK"} ,
        {name: "싱가포르 달러", code: "SGD"} ,
        {name: "태국 바트", code: "THB"} ,
        {name: "미국 달러", code: "USD"} ,
        {name: "씨에프에이 프랑(비씨에이오)", code: "XOF"} ,
        // Add more countries and currency codes as needed
      ],
      conversionTypes: [
        { label: '살 때', value: 'foreign-to-krw' },
        { label: '팔 때', value: 'krw-to-foreign' }
      ]
    };
  },
  computed: {
    result() {
      return _.round(this.convertedAmount, 4);
    }
  },
  methods: {
    clearConversion() {
      this.selectedCountry = '';
      this.amount = '';
      this.convertedAmount = null;
      this.error = null;
    },
    convertCurrency() {
      if (!this.selectedCountry || !this.amount) {
        this.convertedAmount = null;
        return;
      }

      if (this.conversionType === 'krw-to-foreign') {
        console.log(this.selectedCountry + ' ' + this.amount)
        axios
          .get(api.exchangeRate.exchangeRate(this.selectedCountry, this.amount, this.conversionType))
          .then(response => {
            console.log(response)
            this.convertedAmount = response.data.converted_amount;
            this.error = null;
          })
          .catch(error => {
            console.log(error)
            this.convertedAmount = null;
            this.error = '환율 정보를 받아오는 데 실패했습니다. 나중에 다시 시도해주세요.';
            console.error(error);
          });
      } else if (this.conversionType === 'foreign-to-krw') {
        axios
          .get(api.exchangeRate.exchangeRate(this.selectedCountry, this.amount, this.conversionType))
          .then(response => {
            this.convertedAmount = response.data.converted_amount;
            this.error = null;
          })
          .catch(error => {
            this.convertedAmount = null;
            this.error = '환율 정보를 받아오는 데 실패했습니다. 나중에 다시 시도해주세요.';
            console.error(error);
          });
      }
    }
  }
};
</script>
