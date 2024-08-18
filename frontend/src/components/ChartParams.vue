<template>
    <div class="chart-params d-flex justify-content-start">
      <div class="btn-group">
        <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
          {{ selectedInstrument }}
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#" @click="updateInstrument('EUR_USD')">EUR/USD</a>
          <a class="dropdown-item" href="#" @click="updateInstrument('GBP_USD')">GBP/USD</a>
          <a class="dropdown-item" href="#" @click="updateInstrument('USD_JPY')">USD/JPY</a>
          <a class="dropdown-item" href="#" @click="updateInstrument('AUD_USD')">AUD/USD</a>
          <a class="dropdown-item" href="#" @click="updateInstrument('GBP_JPY')">GBP/JPY</a>
          <a class="dropdown-item" href="#" @click="updateInstrument('USD_CAD')">USD/CAD</a>
          <a class="dropdown-item" href="#" @click="updateInstrument('GBP_CHF')">GBP/CHF</a>
        </div>
      </div>

      <div class="btn-group mr-3">
        <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
          {{ selectedGranularity }}
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#" @click="updateGranularity('M1')">1 minute</a>
          <a class="dropdown-item" href="#" @click="updateGranularity('H1')">1 hour</a>
          <a class="dropdown-item" href="#" @click="updateGranularity('D')">1 Day</a>
          <a class="dropdown-item" href="#" @click="updateGranularity('W')">1 Week</a>
          <a class="dropdown-item" href="#" @click="updateGranularity('M')">1 Month</a>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedGranularity: 'H1',
        selectedInstrument: 'EUR_USD',
      };
    },
    methods: {
      updateGranularity(granularity) {
        this.selectedGranularity = granularity;
        this.$emit('update:granularity', granularity);
      },
      updateInstrument(instrument) {
        this.selectedInstrument = instrument;
        this.$emit('update:instrument', instrument);
      }
    }
  }
  </script>
  
  <style scoped>
  .btn-group {
    margin-right: 1px;
  }
  .btn {
    border-radius: 3px;
    border: none;
    color: black;
    background-color: whitesmoke;
  }
  .dropdown-menu {
    background-color: whitesmoke;
  }

  .chart-params {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #dee2e6;
    border-radius: 3px;
  }
  </style>
  