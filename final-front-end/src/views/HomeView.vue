<template>
  <v-container class="background-container" fluid>

  </v-container>
</template>

<script>

  export default {
    name: 'HomeView',

    components: {
    },
  }
</script>

<style scoped>
.background-container {
  background-image: url('@/assets/image/main.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  height: 100vh; /* Adjust the height if needed */
}

@media (max-width: 768px) {
  .background-container {
    background-size: contain;
    background-position: top;
  }
}

</style>