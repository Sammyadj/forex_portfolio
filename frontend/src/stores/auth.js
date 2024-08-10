import { defineStore } from 'pinia';
import axios from 'axios';
import { useProfileStore } from './profile';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('access_token'),
    
  }),
    actions: {
      async login(username, password) {
        try {
          const response = await axios.post('/api/token/', { username, password });
          localStorage.setItem('access_token', response.data.access);
          this.isAuthenticated = true;
    
          // Fetch profile right after login
          await useProfileStore().fetchProfile();
        } catch (error) {
          console.error('Authentication failed:', error.response.data);
          throw new Error('Authentication failed');
        }
      },
      async logout() {
        localStorage.removeItem('access_token');
        this.isAuthenticated = false;
    }
}
});