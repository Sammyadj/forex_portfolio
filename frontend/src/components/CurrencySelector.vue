<template>
    <select v-model="selected">
      <option disabled value="">Select a currency</option>
      <!-- currencies would be dynamic based on available options -->
      <option value="USD/EUR">USD/EUR</option>
      <option value="USD/JPY">USD/JPY</option>
    </select>
  </template>
  
  <script>
  export default {
    props: ['value'],
    computed: {
      selected: {
        get() { return this.value; },
        set(value) { this.$emit('update:modelValue', value); }
      }
    }
  }
  </script>
  <!-- <script>
  import axios from 'axios';
  
  export default {
    name: "TradingInstruments",
    data() {
      return {
        instruments: [],
      };
    },
    mounted() {
      this.fetchInstruments();
    },
    methods: {
      fetchInstruments() {
        axios.get('/api/trading/instruments/')
            .then(response => {
              this.instruments = response.data;
            })
            .catch(error => {
              console.error('There was an error fetching the instruments:', error);
            });
      }
    }
  }
  </script> -->