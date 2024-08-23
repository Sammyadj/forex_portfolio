<template>
  <div class="dashboard">
    <h3>Dashboard</h3>
  </div>
  <div>
    <BotController />
  </div>
  <!-- <div>
    <PortfolioOverview />
  </div> -->
</template>

<script>
import BotController from '@/components/BotController.vue';
// import PortfolioOverview from '@/components/PortfolioOverview.vue';
// import RecentTradesTable from '@/components/RecentTradesTable.vue';
// import { usePortfolioStore } from '@/stores/portfolioStore';


export default {
  name: 'Dashboard',
  components: {
    BotController,
    // PortfolioOverview,
    // RecentTradesTable,
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

<!-- <template>
  <div class="container mt-4">
    <h1>Dashboard</h1>
    <div v-if="profile">
      <p>Welcome to your dashboard, {{ profileId }}!</p>
      <p>Welcome to your dashboard, {{ profile.username }}!</p>
      <p>Your balance is: £{{ profile.balance }}</p>
    </div>
    <p v-else>Loading...</p>
  </div>
</template>


<script>
import { useProfileStore } from '@/stores/profile';
import { computed } from 'vue';

export default {
  setup() {
    const profileStore = useProfileStore();
    const profile = computed(() => profileStore.profile);
    const profileId = computed(() => profileStore.profile?.id);


    return {
      profile,
      profileId,
    };
  }
}
</script>


<style scoped>
.container {
  margin-top: 20px;
  text-align: center;
}
</style> -->



