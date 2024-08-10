import { defineStore } from 'pinia';
import axios from 'axios';
import { reactive } from 'vue';

export const useProfileStore = defineStore('profile', {
  state: () => {
    return reactive({
      profile: null
    });
  },
  actions: {
    async fetchProfile() {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        console.error('No access token available.');
        return;
      }
      await axios.get('/api/accounts/current_profile/', {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      })
      .then(response => {
        console.log('Profile data:', response.data);
        this.profile = response.data;
      })
      .catch(error => {
        console.error('Failed to fetch profile:', error);
      });
    }
  }
});
