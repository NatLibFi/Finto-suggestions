import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  meetingMutations,
  meetingGetters,
  meetingActions
} from './meetingConst';

export const mapMeetingGetters = getters => mapGetters(namespace, getters);
export const mapMeetingActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    items: []
  },
  mutations: {
    [meetingMutations.SET_MEETINGS](state, suggestions) {
      Vue.set(state, storeStateNames.ITEMS, suggestions);
    }
  },
  getters: {
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS]
  },
  actions: {
    async [meetingActions.GET_MEETINGS]({ commit }) {
      const result = await api.suggestions.getSuggestions();
      commit(meetingMutations.SET_MEETINGS, result.data);
    }
  }
};
