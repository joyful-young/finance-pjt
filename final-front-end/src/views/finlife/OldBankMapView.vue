<template>
  <div>
    <form @submit.prevent="searchBanks">
        <label for="location">Location:</label>
        <input type="text" id="location" v-model="location" required>
        <label for="bank">Bank:</label>
        <input type="text" id="bank" v-model="bank" required>
        <button type="submit">Search</button>
    </form>


      <div id="map" style="width: 500px; height: 400px;">

    </div>       
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios';
import api from '@/api'

export default {
  name: 'BankMapView',
  data() {
    return {
      location: '',
      bank: '',
      banks: [],
      latitude:33.450701,
      longitude:126.570667,
      map:null
    };
  },
     mounted() {
    if (window.kakao && window.kakao.maps) {
      // 카카오 객체가 있고, 카카오 맵그릴 준비가 되어 있다면 맵 실행
      this.initializeMap()
    } else {
      // 없다면 카카오 스크립트 추가 후 맵 실행
      this.loadScript();
    }
  },
  computed: {
  ...mapGetters(['currentUser', 'authHeader'])},
  methods: {
     loadScript() {
      const script = document.createElement("script")
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_API_KEY}&autoload=false`
      /* global kakao */
      script.addEventListener("load", () => {
        kakao.maps.load(this.initializeMap)
      })
      document.head.appendChild(script)
    },
    initializeMap() {
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3
      };
      this.map = new kakao.maps.Map(document.getElementById('map'), mapOption);
    },
    loadMarker(banks) {
    for (let i = 0; i < banks.length; i++) {
      const { latitude, longitude } = banks[i]; // Extract latitude and longitude from the bank object

      const markerPosition = new window.kakao.maps.LatLng(latitude, longitude);

      const marker = new window.kakao.maps.Marker({
        position: markerPosition,
      });

      marker.setMap(this.map);
      }
    },
    loadMap(latitude, longitude) {
      const container = document.getElementById("map"); // 지도를 담을 DOM 영역
      const options = {
        // 지도를 생성할 때 필요한 기본 옵션
        center: new window.kakao.maps.LatLng(Number(latitude), Number(longitude)), // 지도의 중심좌표
        level: 3, // 지도의 레벨(확대, 축소 정도)
      };
      this.map = new window.kakao.maps.Map(container, options); // 지도 생성 및 객체 리턴
    },    
    searchBanks() {
      axios({
          method: 'POST',
          url: api.bankMap.searchBank(),
          headers: this.authHeader,
          data: { 
            "location": this.location,
            "bank": this.bank
          }
      })
      .then(response => {
          console.log(response)
          this.banks = response.data;
          this.latitude = this.banks[0].latitude;
          this.longitude = this.banks[0].longitude
          this.loadMap(this.latitude, this.longitude)
          this.loadMarker(this.banks)
      })
      .catch(error => {
        console.error(error)
        alert('검색 결과가 없습니다.')
      });
    },
  }
};
</script>
