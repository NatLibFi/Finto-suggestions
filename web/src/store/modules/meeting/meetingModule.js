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
    [storeStateNames.ITEMS]: []
  },
  getters: {
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS]
  },
  mutations: {
    [meetingMutations.SET_MEETINGS](state, meetings) {
      Vue.set(state, storeStateNames.ITEMS, meetings);
    }
  },
  actions: {
    async [meetingActions.GET_MEETINGS]({ commit }) {
      const result = await api.meeting.getMeetings();
      if (result && result.code === 200) {
        commit(meetingMutations.SET_MEETINGS, result.data);
      }
    }
  }
};
