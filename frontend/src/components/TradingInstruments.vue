<template>
  <div>
    <h1>Instruments</h1>
    <ul>
      <li v-for="instrument in instruments" :key="instrument.id">
        {{ instrument.name }} - {{ instrument.type }}
      </li>
    </ul>
  </div>
</template>

<script>
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
</script>
