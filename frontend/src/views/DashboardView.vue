<template>
  <div class="container mt-4">
    <h1>Dashboard</h1>
    <div v-if="profile">
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

    return {
      profile,
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
