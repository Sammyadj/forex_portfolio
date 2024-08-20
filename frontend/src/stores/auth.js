import { defineStore } from 'pinia';
import axios from 'axios';
import { useProfileStore } from './profile';
import { useTradeStore } from './tradeStore';
import { usePricingStore } from './pricingStore';
import { useAccountStore } from './accountStore';
import { usePortfolioStore } from './portfolioStore';

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
        const portfolioStore = usePortfolioStore();
        
        portfolioStore.initializeWebSocket();
        tradeStore.initializeWebSocket();
        accountStore.initializeWebSocket();
        pricingStore.initializeWebSocket();
    
      } catch (error) {
        console.error('Authentication failed:', error.response.data);
        throw new Error('Authentication failed');
      }
    },
    async logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      const accountStore = useAccountStore();
      const tradeStore = useTradeStore();
      const pricingStore = usePricingStore();
      const portfolioStore = usePortfolioStore();
      
      accountStore.closeWebSocket();
      tradeStore.closeWebSocket();
      pricingStore.closeWebSocket();
      portfolioStore.closeWebSocket();
    
      this.isAuthenticated = false;
    }
  }
});
