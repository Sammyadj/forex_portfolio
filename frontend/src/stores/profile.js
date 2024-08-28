import { defineStore } from 'pinia';
import { reactive } from 'vue';
import { makeApiCall } from '@/stores/authHelpers';
// import axios from 'axios';
export const useProfileStore = defineStore('profile', {
  state: () => {
    return reactive({
      profile: null
    });
  },
  actions: {
    async fetchProfile() {
      try {
        const profileData = await makeApiCall('/api/accounts/current_profile/');
        console.log('Profile data:', profileData);
        this.profile = profileData; // Assign the returned profile data directly
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    }
  },
  getters: {
    profileId(state) {
      return state.profile ? state.profile.id : null;
    }
  }
});