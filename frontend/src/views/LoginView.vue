<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h1 class="card-title text-center">Login</h1>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="username">Username</label>
                <input v-model="username" type="text" class="form-control" id="username" placeholder="Enter username" required>
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input v-model="password" type="password" class="form-control" id="password" placeholder="Password" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Log In</button>
              <p>Don't have an account? <router-link :to="{ name: 'register' }">Create an account</router-link></p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const authStore = useAuthStore();
    const router = useRouter();

    const login = async () => {
      try {
        await authStore.login(username.value, password.value);
        router.push({ name: 'dashboard' });
      } catch (error) {
        console.error('Login error:', error.message);
      }
    };

    return { username, password, login };
  }
}
</script>