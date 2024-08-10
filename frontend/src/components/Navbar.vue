<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="navbar-brand" to="/">Forex Portfolio</router-link>
      <div class="navbar-nav">
        <router-link v-if="isAuthenticated" class="nav-link" to="/dashboard">Dashboard</router-link>
        <router-link v-if="isAuthenticated" class="nav-link" to="/trade">Trade</router-link>
        <button v-if="isAuthenticated" @click="logout" class="nav-item nav-link">Logout</button>
        <router-link v-else class="nav-item nav-link" to="/login">Login</router-link>
      </div>
    </nav>
  </template>
  
<script>
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const isAuthenticated = computed(() => authStore.isAuthenticated);

    const logout = () => {
    authStore.logout();
    router.push('/login');
    };

    return { isAuthenticated, logout };
}
};
</script>

  