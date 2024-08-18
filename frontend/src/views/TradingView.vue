<template>
  <div class="trading-view">
    <div class="row">
      <!-- Left Column for Price Stream -->
      <div class="col-md-2 border-end">
        <PriceStream />
      </div>

      <!-- Right Column for Charts, Trade Form, Account, and Trades -->
      <div class="col-md-10 d-flex flex-column" >
        <!-- Chart Parameters Section -->
        <div class="mb-1 ">
          <ChartParams @update:granularity="handleGranularityUpdate" @update:instrument="handleInstrumentUpdate" />
        </div>

        <!-- Chart and Trade Buttons Section -->
        <div class="row h-100">
          <div class="col-lg-10 col-md-8 col-12">
            <CandlestickChart :instrument="instrument" :granularity="granularity" />
          </div>
          <div class="col-lg-2 col-md-4 col-12">
            <TradeForm :instrument="instrument" />
          </div>
        </div>

        <!-- Account and Trades Info Section -->
        <div class="row ">
          <div class="col-md-6 mb-3">
            <AccountInfo />
          </div>
          <div class="col-md-6 mb-3">
            <TradesInfo />
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { usePricingStore } from '@/stores/pricingStore';
// import { useTradeStore } from '@/stores/tradeStore';
import PriceStream from '@/components/PriceStream.vue';
import CandlestickChart from '@/components/CandlestickChart.vue';
import ChartParams from '@/components/ChartParams.vue';
import TradeForm from '@/components/TradeForm.vue';
import AccountInfo from '@/components/AccountInfo.vue';
import TradesInfo from '@/components/TradesInfo.vue';

export default {
  components: {
    ChartParams,
    CandlestickChart,
    PriceStream,
    TradeForm,
    AccountInfo,
    TradesInfo
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
  },
  mounted() {
    const webSocketStore = usePricingStore();
    webSocketStore.initializeWebSocket(); 

  }
}
</script>

<style scoped>
.trading-view,
/* .row, */
.col-md-10
{
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* max-height: 100vh; */
  /* border: 3px solid #ddd; */
}

.trading-view {
  border: 3px solid #ddd;
}


/* Further adjustments */
/* .chart-and-trade-buttons {
  flex-grow: 1;
} */

/* .account-and-trades-info {
  height: 200px;
} */

</style>




<!-- <style scoped>
/* This will ensure that the entire trading view takes up the full height of the viewport */
.trading-view {
  height: 100vh; /* Ensures the full viewport height is used */
  display: flex;
  flex-direction: column; /* Organizes children vertically */
}

/* Flex settings for the main columns */
.price-stream-container,
.chart-and-trade-container {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Flex grow settings to allocate space dynamically based on content size */
/* .chart-params,
.chart-and-trade-buttons {
  flex-grow: 0;
} */

.chart-params {
  flex-grow: 0; /* Adjust to allow this section to grow and take up more or less space */
}

.chart-and-trade-buttons {
  flex-grow: 1; /* Adjust to take up the majority of the space for detailed viewing */
}

.account-and-trades-info {
  flex-grow: 0;
  display: flex;
}




/* Specific flex settings for Account and Trades information to ensure they take up equal space */
.AccountInfo, .TradesInfo {
  flex: 1; /* Each takes up equal space within their container */
  display: flex; /* Enables flexbox properties within AccountInfo and TradesInfo */
  flex-direction: column; /* Stacks children vertically */
  justify-content: center; /* Centers children vertically */
}

/* Ensuring the cards within AccountInfo and TradesInfo take up full available space */
.card {
  height: 100%; /* Makes each card fill the parent container's height */
  display: flex;
  flex-direction: column;
  justify-content: space-around; /* Distributes space around items */
}

/* Styles for maintaining responsive and aesthetically pleasing margins and paddings */
.mb-3 {
  margin-bottom: 1rem !important; /* Adds consistent bottom margin */
}

/* Media query to handle layouts on smaller screens */
@media (max-width: 768px) {
  .price-stream-container,
  .chart-and-trade-container {
    flex-direction: row;
  }

  .AccountInfo, .TradesInfo {
    min-height: 150px; /* Adjusts the minimum height for smaller screens */
  }
}

</style> -->

<!-- <style scoped>
.trading-view {
  background-color: #f4f4f4; /* Light grey background */
}

h2 {
  font-size: 1.5rem; /* Adjust header font size */
}

.mb-3 {
  margin-bottom: 1rem !important; /* Consistent margin */
}

.border-end {
  border-right: 1px solid #ddd !important; /* Add a separator on large screens */
}

.bg-light {
  background-color: #f8f9fa !important; /* Bootstrap's light background */
}

h-100 {
  height: 100vh !important; /* Full height */
}
</style> -->




<!-- <style scoped>
.trading-view {
  display: flex;
  background-color: #f4f4f4; /* Light grey background */
  /* height: 100vh; */
}

.price-stream-container {
  flex: 1; /* Flex grow as needed */
  border-right: 2px solid #ddd; /* Separator */
}

.chart-and-trade-container {
  flex: 3; /* Larger flex basis for the right container */
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.chart-params, .chart-and-trade-buttons, .account-and-trades-info {
  margin-bottom: 20px; /* Spacing between sections */
}

.chart-and-trade-buttons {
  display: flex;
}

.CandlestickChart {
  flex: 3; /* Larger area for the chart */
}

.TradeForm {
  flex: 1; /* Smaller area for the trade form */
}

.account-and-trades-info {
  display: flex;
  justify-content: space-between;
}

.AccountInfo, .TradesInfo {
  flex: 1; /* Equal distribution */
}
</style> -->
