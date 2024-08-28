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
        <div class="row h-90">
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
import { useTradeStore } from '@/stores/tradeStore';
// import { usePortfolioStore } from '@/stores/portfolioStore';
import { useAccountStore } from '@/stores/accountStore';
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
      instrument: 'EUR/USD',
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

    // const portfolioStore = usePortfolioStore();
    const tradeStore = useTradeStore();
    const pricingStore = usePricingStore();
    const accountStore = useAccountStore();
    
    // if (tradeStore.socket && pricingStore.socket) {
    //   return;
    // }
    // portfolioStore.initializeWebSocket();
    tradeStore.initializeWebSocket();
    pricingStore.initializeWebSocket();
    accountStore.initializeWebSocket();

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
