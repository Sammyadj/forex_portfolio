import { defineStore } from 'pinia';
import axios from 'axios';
import { useProfileStore } from './profile';
import { useTradeStore } from './tradeStore';
import { usePricingStore } from './pricingStore';
import { useAccountStore } from './accountStore';
// import { usePortfolioStore } from './portfolioStore';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!localStorage.getItem('access_token'),
  }),
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('/api/token/', { username, password });
        this.isAuthenticated = true;
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
    
        // Fetch the user profile
        const profileStore = useProfileStore();
        await profileStore.fetchProfile();
    
        // Initialize WebSockets after login
        // const portfolioStore = usePortfolioStore();
        const tradeStore = useTradeStore();
        const pricingStore = usePricingStore();
        const accountStore = useAccountStore();
        
        // portfolioStore.initializeWebSocket();
        tradeStore.initializeWebSocket();
        pricingStore.initializeWebSocket();
        accountStore.initializeWebSocket();

        // tradeStore.initializeWebSocket().then(() => {
        //   return pricingStore.initializeWebSocket();
        // }).then(() => {
        //   return accountStore.initializeWebSocket();
        // }).catch(error => {
        //   console.error('WebSocket initialization failed:', error);
        // });
    
      } catch (error) {
        console.error('Authentication failed:', error.response.data);
        throw new Error('Authentication failed');
      }
    },
    async logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      // const portfolioStore = usePortfolioStore();
      const tradeStore = useTradeStore();
      const pricingStore = usePricingStore();
      const accountStore = useAccountStore();
      
      // portfolioStore.closeWebSocket();
      tradeStore.closeWebSocket();
      pricingStore.closeWebSocket();
      accountStore.closeWebSocket();
    
      this.isAuthenticated = false;
    }
  }
});
