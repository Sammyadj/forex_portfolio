<template>
  <div class="trading-view d-flex">
    <div class="price-stream-container flex-fill">
      <PriceStream />
    </div>
    <div class="chart-container flex-fill">
      <ChartParams @update:granularity="handleGranularityUpdate" @update:instrument="handleInstrumentUpdate"/>
      <CandlestickChart :instrument="instrument" :granularity="granularity"/>
    </div>
    <div class="trade-form-container">
      <TradeForm />
    </div>
  </div>
</template>

<script>
import PriceStream from '@/components/PriceStream.vue';
import CandlestickChart from '@/components/CandlestickChart.vue';
import ChartParams from '@/components/ChartParams.vue';
import TradeForm from '@/components/TradeForm.vue';

export default {
  components: {
    ChartParams,
    CandlestickChart,
    PriceStream,
    TradeForm
  },
  data() {
    return {
      instrument: 'EUR_USD',
      granularity: 'H1'
    };
  },
  methods: {
    handleGranularityUpdate(newGranularity) {
      this.granularity = newGranularity;
    },
    handleInstrumentUpdate(newInstrument) {
      this.instrument = newInstrument;
    }
  }
}
</script>

<style scoped>
.trading-view {
  display: flex;
  justify-content: space-between; /* Adjusts the spacing between components */
}

.price-stream-container,
.chart-container {
  width: 50%; /* Adjusts width */
}

/* .trade-form-container {
  width: 100%;
} */
</style>




<!-- <template>
  <div class="trading-view d-flex">
    <div class="price-stream-container flex-fill">
      <PriceStream />
    </div>
    <div>
      <ChartParams @update:granularity="fetchChartData" @update:instrument="fetchChartData"/>
    </div>  
    <div class="chart-container">
      <CandlestickChart ref="candlestickChart" />
    </div>
    <div class="trade-form-container">
      <TradeForm />
    </div>
  </div>
</template>

<script>
import PriceStream from '@/components/PriceStream.vue';
import CandlestickChart from '@/components/CandlestickChart.vue';
import ChartParams from '@/components/ChartParams.vue';
import TradeForm from '@/components/TradeForm.vue';

export default {
  components: {
    ChartParams,
    CandlestickChart,
    PriceStream,
    TradeForm
  },
  data() {
    return {
      chartData: null
    };
  },
  methods: {
    fetchChartData(granularity, instrument) {
      this.$refs.candlestickChart.fetchChartData(granularity, instrument);
    }
  }
}
</script>

<style scoped>
.trading-view {
  display: flex;
  justify-content: space-between; /* Adjusts the spacing between components */
}

.price-stream-container,
.chart-container {
  width: 50%;
  flex-grow: 1;
}

.trade-form-container {
  width: 100%; /* Sets the trade form to take the full width below the other components */
}
</style>


<template>
  <div>
    <ChartParams @update:granularity="fetchChartData" @update:instrument="fetchChartData"/>
    <CandlestickChart :data="chartData"/>
    <PriceStream/>
    <TradeForm/>
  </div>
</template>

<script>
import ChartParams from '@/components/ChartParams.vue';
import CandlestickChart from '@/components/CandlestickChart.vue';
import PriceStream from '@/components/PriceStream.vue';
import TradeForm from '@/components/TradeForm.vue';

export default {
  components: {
    ChartParams,
    CandlestickChart,
    PriceStream,
    TradeForm
  },
  data() {
    return {
      chartData: null
    };
  },
  methods: {
    fetchChartData(granularity, instrument) {
      // API call to fetch data
      // Update `chartData` accordingly
    }
  }
}
</script> --> -->
