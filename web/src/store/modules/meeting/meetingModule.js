import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  sessionStorageKeyNames,
  meetingMutations,
  meetingGetters,
  meetingActions
} from './meetingConst';

import { comparerAsc } from '../../../utils/sortingHelper';

export const mapMeetingGetters = getters => mapGetters(namespace, getters);
export const mapMeetingActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: [],
    [storeStateNames.ITEM]: null,
    [storeStateNames.SELECTED_SORT]: null
  },
  getters: {
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS],
    [meetingGetters.GET_MEETING]: state => state[storeStateNames.ITEM],
    [meetingGetters.GET_SELECTED_SORT]: state => state[storeStateNames.SELECTED_SORT]
  },
  mutations: {
    [meetingMutations.SET_MEETINGS](state, meetings) {
      if (meetings.length > 0) {
        meetings.sort(comparerAsc('meeting_date'));
      }
      Vue.set(state, storeStateNames.ITEMS, meetings);
    },
    [meetingMutations.SET_MEETING](state, meeting) {
      Vue.set(state, storeStateNames.ITEM, meeting);
    },
    [meetingMutations.SET_SELECTED_SORT](state, sortKey) {
      Vue.set(state, storeStateNames.SELECTED_SORT, sortKey);
    },
    [meetingMutations.SET_SELECTED_STORE_SORT](state, sortKey) {
      Vue.set(sessionStorage, sessionStorageKeyNames.MEETING_LIST_SELECTED_SORT, sortKey);
    }
  },
  actions: {
    async [meetingActions.GET_MEETINGS]({ commit }) {
      const result = await api.meeting.getMeetings();
      if (result && result.code === 200) {
        commit(meetingMutations.SET_MEETINGS, result.data);
      }
    },
    async [meetingActions.GET_MEETING]({ commit }, meetingId) {
      const result = await api.meeting.getMeeting(meetingId);
      if (result && result.code === 200) {
        commit(meetingMutations.SET_MEETING, result.data);
      }
    },
    [meetingActions.GET_SELECTED_SORT]({ commit }) {
      const sortKey = sessionStorage[sessionStorageKeyNames.MEETING_LIST_SELECTED_SORT];
      if (sortKey) {
        commit(meetingMutations.SET_SELECTED_SORT, sortKey);
      }
    },
    [meetingActions.SET_SELECTED_SORT]({ commit }, sortKey) {
      if (sortKey) {
        commit(meetingMutations.SET_SELECTED_SORT, sortKey);
        commit(meetingMutations.SET_SELECTED_STORE_SORT, sortKey);
      }
    }
  }
};
