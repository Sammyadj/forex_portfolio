<template>
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
</style>

<!-- <script>
import { useProfileStore } from '@/stores/profile';
import { useTradeStore } from '@/stores/tradeStore';
import { useWebSocketStore } from '@/stores/webSocketStore';
import { useAccountStore } from '@/stores/accountStore';
import { computed } from 'vue';

export default {
  setup() {
    const profileStore = useProfileStore();
    const profile = computed(() => profileStore.profile);
    const profileId = profileStore.profile?.id;
    

    return {
      profile,
      profileId,
    };
  },
  mounted() {
    const tradeStore = useTradeStore();
    tradeStore.initializeWebSocket();

    const webSocketStore = useWebSocketStore();
    webSocketStore.initializeWebSocket();

    const accountStore = useAccountStore();
    accountStore.initializeWebSocket();
  },
}
</script> -->


