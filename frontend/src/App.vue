<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
// import { usePricingStore } from '@/stores/pricingStore';
// import { useTradeStore } from '@/stores/tradeStore';

export default {
  components: {
    Navbar,
  },
//   mounted() {

// // const portfolioStore = usePortfolioStore();
// const tradeStore = useTradeStore();
// const pricingStore = usePricingStore();
// // const accountStore = useAccountStore();


// // portfolioStore.initializeWebSocket();
// tradeStore.initializeWebSocket();
// pricingStore.initializeWebSocket();
// // accountStore.initializeWebSocket();

// }
};
</script>


