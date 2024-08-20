<template>
  <div class="container mt-1">
    <div v-if="Object.keys(priceInfo).length" class="card-container flex-column d-flex justify-content-start">
      <div class="card">
          <div class="card-body text-center">
            Instruments
          </div>
      </div>
      <div v-for="(info, instrument) in priceInfo" :key="instrument" class="card mb-1 ">
        
        <div class="list-group-item text-center">
          <div class="card-header">{{ instrument }}</div>
            <div class="card-body">
              <p class="card-text"><strong>Bid:</strong> {{ info.bid }}</p>
              <p class="card-text"><strong>Ask:</strong> {{ info.ask }}</p>
            </div>
          </div>
        </div>
    </div>
    <p v-else class="text-muted">No price data available.</p>
  </div>
</template>

<script>
import { usePricingStore } from '@/stores/pricingStore';

export default {
  setup() {
    const { prices } = usePricingStore();

    return {
      priceInfo: prices
    };
  }
};
</script>

<style scoped>
.card-header {
  background-color: #f7f7f7;
  color: #333;
  font-weight: bold;
  border: none;
}
.card {
  width: 100%;
  border: solid 1px #dee2e6;
}
.container {
  max-width: 100%;
  height: 700px;
  /* border: 2px solid #9dceff;
  background-color: #110909b7; */
  overflow-y: auto;
}

.card-container {
  max-width: 100%;
  height: 100%;
  /* overflow-y: auto; */
  /* border: 1px solid #f34aff; */
}
.text-center {
  text-align: center;
}
</style>


