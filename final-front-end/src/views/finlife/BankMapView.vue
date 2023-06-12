<template>
  <v-container fluid>
    <v-row class="mt-3">
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <h1>
          <v-icon
            x-large
          >mdi-bank-circle-outline</v-icon>
          주변 은행 검색
        </h1>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <v-form @submit.prevent>
          <SelectOption
            @search="searchBanks"
          />
        </v-form>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <!-- 카카오맵 들어갈 곳 -->
        <div id="map" style="width: 100%; height: 500px" class="mx-auto"></div>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>

    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <div class="search-results">
          <v-container v-if="banks.length !== 0">
            <h2>검색 결과</h2>
            <v-list>
              <v-list-item v-for="(bank, index) in banks" :key="bank.id">
                <v-row class="result-item">
                  <v-col cols="2">
                    <div class="item-number">{{ index + 1 }}</div>
                  </v-col>
                  <v-col cols="10">
                    <div class="item-details">
                      <h3>{{ bank.name }}</h3>
                      <h5>{{ bank.address }}</h5>
                    </div>
                  </v-col>
                </v-row>
              </v-list-item>
            </v-list>
          </v-container>
          <div v-if="showResults && banks.length === 0">
            <p>검색 결과가 없습니다.</p>
          </div>
        </div>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>


<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
import api from '@/api'
import SelectOption from '@/components/finlife/SelectOption.vue'

export default {
  name: 'BankMapView',
  data() {
    return {
      // location: '',
      // bank: '',
      banks: [],
      latitude: 33.450701,
      longitude: 126.570667,
      map: null,
      markers: [],
      infowindow: null,
      showResults: false,
    };
  },
  components: {
    SelectOption,
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initializeMap();
    } else {
      this.loadScript();
    }
  },
  computed: {
    ...mapGetters(['currentUser', 'authHeader']),
    bankListLength() {
      return this.banks.length
    }
  },
  watch: {
    bankListLength() {
      this.showResults = true
    }
  },
  methods: {
    // 스크립트 로드
    loadScript() {
      const script = document.createElement("script");
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_API_KEY}&autoload=false`;
      /* global kakao */
      script.addEventListener("load", () => {
        kakao.maps.load(this.initializeMap);
      });
      document.head.appendChild(script);
    },
    // 지도 초기화
    initializeMap() {
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3
      };
      this.map = new kakao.maps.Map(document.getElementById('map'), mapOption);
      this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    },
    // 마커 로드
    loadMarker(banks) {
      this.clearMarkers();

      for (let i = 0; i < banks.length; i++) {
        const { latitude, longitude, name } = banks[i];

        const markerPosition = new kakao.maps.LatLng(latitude, longitude);
        const marker = new kakao.maps.Marker({
          position: markerPosition
        });

        kakao.maps.event.addListener(marker, 'mouseover', () => {
          this.displayInfowindow(marker, name);
        });

        kakao.maps.event.addListener(marker, 'mouseout', () => {
          this.infowindow.close();
        });

        marker.setMap(this.map);
        this.markers.push(marker);
      }
    },
    // 마커 삭제
    clearMarkers() {
      for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
      this.markers = [];
    },
    // 인포윈도우 표시
    displayInfowindow(marker, title) {
      const content = `<div style="padding: 5px; z-index: 1;">${title}</div>`;
      this.infowindow.setContent(content);
      this.infowindow.open(this.map, marker);
    },
    // 은행 검색
    searchBanks(payload) {
      const { location, bank } = payload
      if (location === '') {
        alert('지역을 선택해주세요.')
        return
      }

      if (bank === '') {
        alert('은행을 선택해주세요.')
        return
      }
      axios({
        method: 'POST',
        url: api.bankMap.searchBank(),
        headers: this.authHeader,
        data: {
          location,
          bank,
        }
      })
        .then(response => {
          this.banks = response.data;
          if (this.banks.length > 0) {
            const { latitude, longitude } = this.banks[0];
            this.latitude = latitude;
            this.longitude = longitude;
            this.loadMap(this.latitude, this.longitude);
            this.loadMarker(this.banks);
          } else {
            alert('검색 결과가 없습니다.');
          }
        })
        .catch(error => {
          console.error(error);
          alert('검색 중 오류가 발생했습니다.');
        });
    },
    // searchBanks() {
    //   if (this.location === '') {
    //     alert('지역을 선택해주세요')
    //     return
    //   }
    //   if (this.bank === '') {
    //     alert('은행을 선택해주세요')
    //     return
    //   }
    //   axios({
    //     method: 'POST',
    //     url: api.bankMap.searchBank(),
    //     headers: this.authHeader,
    //     data: {
    //       location: this.location,
    //       bank: this.bank
    //     }
    //   })
    //     .then(response => {
    //       this.banks = response.data;
    //       if (this.banks.length > 0) {
    //         const { latitude, longitude } = this.banks[0];
    //         this.latitude = latitude;
    //         this.longitude = longitude;
    //         this.loadMap(this.latitude, this.longitude);
    //         this.loadMarker(this.banks);
    //       } else {
    //         alert('검색 결과가 없습니다.');
    //       }
    //     })
    //     .catch(error => {
    //       console.error(error);
    //       alert('검색 중 오류가 발생했습니다.');
    //     });
    // },
    // 지도 로드
    loadMap(latitude, longitude) {
      const container = document.getElementById("map");
      const options = {
        center: new kakao.maps.LatLng(Number(latitude), Number(longitude)),
        level: 3
      };
      this.map = new kakao.maps.Map(container, options);
      this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    }
  }
};
</script>

<style>
.search-results {
  margin-top: 20px;
}

.search-results h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.search-results ul {
  list-style-type: none;
  padding: 0;
}

.search-results li {
  margin-bottom: 10px;
}

.result-item {
  display: flex;
}

.item-number {
  font-weight: bold;
  font-size: 16px;
  margin-right: 10px;
}

.item-details {
  flex: 1;
}

.item-details h3 {
  font-size: 18px;
  margin-bottom: 5px;
}

.item-details h5 {
  font-size: 14px;
  color: #666;
}
</style>