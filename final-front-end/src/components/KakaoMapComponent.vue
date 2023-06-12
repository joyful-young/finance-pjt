<template>
 
  <div id="map" style="width: 500px; height: 400px;">
   <button @click="initializeMap"
   
   >버튼버튼</button>
   
   

    너는 찍히나요

  </div>

  
</template>

<script>


export default {
    data() {
        return {

            map:null
        }

    },
  created() {
    // Load Kakao Maps API asynchronously
    const script = document.createElement("script");
    this.initializeMap()

    script.onload = () => this.initializeMap();
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_API_KEY}`;
    document.head.appendChild(script);

  },
  methods: {
    initializeMap() {
      const container = document.getElementById("map");
      const options = {
        center: new window.kakao.maps.LatLng(33.450701, 126.570667),
        level: 3
      };

      const map = new window.kakao.maps.Map(container, options);
      console.log(map);
    }
  }
};
</script>
