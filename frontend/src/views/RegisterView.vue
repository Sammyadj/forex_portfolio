<template>
  <div class="register-container">
    <h1>Register</h1>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="username" type="text" id="username" class="form-control" placeholder="Username" required />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input v-model="email" type="email" id="email" class="form-control" placeholder="Email" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="password" type="password" id="password" class="form-control" placeholder="Password" required />
      </div>
      <div class="mb-3">
        <label for="password2" class="form-label">Confirm Password</label>
        <input v-model="password2" type="password" id="password2" class="form-control" placeholder="Confirm Password" required />
      </div>
      <div class="mb-3">
        <label for="balance" class="form-label">Initial Deposit (£100 - £10000)</label>
        <input v-model.number="balance" type="number" id="balance" class="form-control" placeholder="Initial Deposit" required min="100" max="10000" />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      balance: 100,
    };
  },
  methods: {
    register() {
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
        password2: this.password2,
        balance: this.balance
      };
      console.log('Registering:', userData);
      axios.post('/api/accounts/register/', userData)
        .then(response => {
          console.log('Registered successfully:', response.data);
          this.$router.push('/login');
        })
        .catch(error => {
          console.error('Failed to register:', error.response.data);
        });
    }
  }
};
</script>
