import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';
import { namespace, storeStateNames, tagMutations, tagGetters, tagActions } from './tagConst';

export const mapTagGetters = getters => mapGetters(namespace, getters);
export const mapTagActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    items: []
  },
  mutations: {
    [tagMutations.SET_TAGS](state, tags) {
      Vue.set(state, storeStateNames.ITEMS, tags);
    }
  },
  getters: {
    [tagGetters.GET_TAGS]: state => state[storeStateNames.ITEMS]
  },
  actions: {
    async [tagActions.GET_TAGS]({ commit }) {
      const result = await api.tags.getTags();
      commit(tagMutations.SET_TAGS, result.data);
    }
  }
};
