<template>
  <v-container>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <form @submit.prevent="searchBanks">
          <label for="location">Location:</label>
          <input type="text" id="location" v-model="location" required>
          <label for="bank">Bank:</label>
          <input type="text" id="bank" v-model="bank" required>
          <button type="submit">Search</button>
        </form>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col cols="12" sm="10" lg="8">
        <div id="map" style="width: 80%; height: 600px" class="mx-auto"></div>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>

    <!-- 여기부터! -->
    <v-row>
      <v-col cols="12">
        <div class="search-results">
          <div v-if="banks.length > 0">
            <h2>Search Results</h2>
            <ul>
              <li v-for="(bank, index) in banks" :key="bank.id">
                <div class="result-item">
                  <div class="item-number">{{ index + 1 }}</div>
                  <div class="item-details">
                    <h3>{{ bank.name }}</h3>
                    <h5>{{ bank.address }}</h5>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <div v-else>
            <p>No search results found.</p>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
import api from '@/api'

export default {
  name: 'BankMapView',
  data() {
    return {
      location: '',
      bank: '',
      banks: [],
      latitude: 33.450701,
      longitude: 126.570667,
      map: null,
      markers: [],
      infowindow: null
    };
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initializeMap();
    } else {
      this.loadScript();
    }
  },
  computed: {
    ...mapGetters(['currentUser', 'authHeader'])
  },
  methods: {
    loadScript() {
      const script = document.createElement("script");
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_API_KEY}&autoload=false`;
      /* global kakao */
      script.addEventListener("load", () => {
        kakao.maps.load(this.initializeMap);
      });
      document.head.appendChild(script);
    },
    initializeMap() {
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3
      };
      this.map = new kakao.maps.Map(document.getElementById('map'), mapOption);
      this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    },
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
    clearMarkers() {
      for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
      this.markers = [];
    },
    displayInfowindow(marker, title) {
      const content = `<div style="padding: 5px; z-index: 1;">${title}</div>`;
      this.infowindow.setContent(content);
      this.infowindow.open(this.map, marker);
    },
    searchBanks() {
      axios({
        method: 'POST',
        url: api.bankMap.searchBank(),
        headers: this.authHeader,
        data: {
          location: this.location,
          bank: this.bank
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