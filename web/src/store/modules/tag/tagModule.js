import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';
import { namespace, storeStateNames, tagMutations, tagGetters, tagActions } from './tagConst';

export const mapTagGetters = getters => mapGetters(namespace, getters);
export const mapTagActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: []
  },
  getters: {
    [tagGetters.GET_TAGS]: state => state[storeStateNames.ITEMS]
  },
  mutations: {
    [tagMutations.SET_TAGS](state, tags) {
      Vue.set(state, storeStateNames.ITEMS, tags);
    }
  },
  actions: {
    async [tagActions.GET_TAGS]({ commit }) {
      const result = await api.tag.getTags();
      commit(tagMutations.SET_TAGS, result.data);
    }
  }
};
