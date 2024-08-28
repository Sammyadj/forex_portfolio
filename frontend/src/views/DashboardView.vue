<template>
  <div class="dashboard">
    <h3>Dashboard</h3>
  </div>
  <div>
    <BotController />
  </div>
  <div>
    <RecentTradesTable />
  </div>
  <div>
    <PnLChart />
  </div>
</template>

<script>
import BotController from '@/components/BotController.vue';
import RecentTradesTable from '@/components/RecentTradesTable.vue';
import PnLChart from '@/components/PnLChart.vue';
// import PortfolioOverview from '@/components/PortfolioOverview.vue';
// import { usePortfolioStore } from '@/stores/portfolioStore';


export default {
  name: 'Dashboard',
  components: {
    BotController,
    // PortfolioOverview,
    RecentTradesTable,
    PnLChart,
  },
  setup() {


    return {
      // portfolioData,
    };
  },
  // mounted() {
  //   const portfolioStore = usePortfolioStore();
  //   portfolioStore.initializeWebSocket();
  // }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
</style>
