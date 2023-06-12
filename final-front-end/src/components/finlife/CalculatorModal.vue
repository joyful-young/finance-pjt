<template>
  <v-container>
    <v-row>
      <v-col cols="0" sm="1" lg="2"></v-col>
      <v-col>
        <v-card class="calculator">
          <v-toolbar >이자계산기 모달</v-toolbar>
          <v-card-text>
            <div class="calculator-display">{{ calculation }}</div>
          </v-card-text>
          <v-card-actions>
            <div class="calculator-buttons">
              <div class="number-row" v-for="(row, index) in numbers" :key="index">
                <v-btn v-for="number in row" :key="number" @click="appendToCalculation(number)">{{ number }}</v-btn>
              </div>
            </div>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="0" sm="1" lg="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'CalculatorModal',
  data() {
    return {
      calculation: '',
      numbers: [[7, 8, 9], [4, 5, 6], [1, 2, 3], [0]]
    }
  },
  methods: {
    appendToCalculation(number) {
      this.calculation += number;
    }
  },
}
</script>

<style scoped>
/* .calculator {
}

.calculator-display {
}

.calculator-buttons {
} */
</style>