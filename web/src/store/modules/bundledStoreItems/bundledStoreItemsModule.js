import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import api from '../../../api';


export default {
  namespaced: true,
  state: {
    storeStateItems: []
  },
  getters: {
    getInitialData: state => state[storeStateItems.ITEMS]
  },
  mutations: {
    setInitialData(state, initialData) {
      Vue.set(state, storeStateItems.ITEMS, initialData);
    }
  },
  actions: {
    async addInitialData({ dispatch }, { data, suggestionId }) {
      const response = await api.suggestion.addInitialData()(data, suggestionId);
      if (response && response.code === 201) {
        dispatch(mutations.setInitialData(data));
      }
    },
  }
};
