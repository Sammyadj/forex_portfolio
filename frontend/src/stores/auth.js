import { defineStore } from 'pinia';
import axios from 'axios';
import { useProfileStore } from './profile';
import { useTradeStore } from './tradeStore';
import { usePricingStore } from './pricingStore';
import { useAccountStore } from './accountStore';

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
    
        // Fetch the user profile
        const profileStore = useProfileStore();
        await profileStore.fetchProfile();
    
        // Initialize WebSockets after login
        const tradeStore = useTradeStore();
        const pricingStore = usePricingStore();
        const accountStore = useAccountStore();
        
        pricingStore.initializeWebSocket();
        tradeStore.initializeWebSocket();
        accountStore.initializeWebSocket();
    
      } catch (error) {
        console.error('Authentication failed:', error.response.data);
        throw new Error('Authentication failed');
      }
    },
    async logout() {
      localStorage.removeItem('access_token');
      const accountStore = useAccountStore();
      const tradeStore = useTradeStore();
      const pricingStore = usePricingStore();
      
      accountStore.closeWebSocket();
      tradeStore.closeWebSocket();
      pricingStore.closeWebSocket();
    
      this.isAuthenticated = false;
    }
  }
});

// export const useAuthStore = defineStore('auth', {
//   state: () => ({
//     isAuthenticated: !!localStorage.getItem('access_token'),
    
//   }),
//     actions: {
//       async login(username, password) {
//         try {
//           const response = await axios.post('/api/token/', { username, password });
//           localStorage.setItem('access_token', response.data.access);
//           this.isAuthenticated = true;
    
//           // Fetch profile right after login
//           await useProfileStore().fetchProfile();
//         } catch (error) {
//           console.error('Authentication failed:', error.response.data);
//           throw new Error('Authentication failed');
//         }
//       },
//       async logout() {
//         localStorage.removeItem('access_token');
//         this.isAuthenticated = false;
//         const accountStore = useAccountStore();
//         accountStore.closeWebSocket();
//     }
// }
// });