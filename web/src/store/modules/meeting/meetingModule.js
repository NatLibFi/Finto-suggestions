import Vue from 'vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  sessionStorageKeyNames,
  meetingMutations,
  meetingGetters,
  meetingActions
} from './meetingConsts';

import { comparerAsc } from '../../../utils/sortingHelper';

export const mapMeetingGetters = getters => mapGetters(namespace, getters);
export const mapMeetingActions = actions => mapActions(namespace, actions);
export const mapMeetingMutations = mutations => mapMutations(namespace, mutations);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: [],
    [storeStateNames.ITEM]: null,
    [storeStateNames.MEETINGS_SELECTED_SORT]: null
  },
  getters: {
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS],
    [meetingGetters.GET_MEETING]: state => state[storeStateNames.ITEM],
    [meetingGetters.GET_MEETINGS_SELECTED_SORT]: state =>
      state[storeStateNames.MEETINGS_SELECTED_SORT]
  },
  mutations: {
    [meetingMutations.SET_MEETINGS](state, meetings) {
      if (meetings && meetings.length > 0) {
        meetings.sort(comparerAsc('meeting_date'));
      }
      Vue.set(state, storeStateNames.ITEMS, meetings);
    },
    [meetingMutations.SET_MEETING](state, meeting) {
      Vue.set(state, storeStateNames.ITEM, meeting);
    },
    [meetingMutations.SET_MEETINGS_SELECTED_SORT](state, sortKey) {
      Vue.set(state, storeStateNames.MEETINGS_SELECTED_SORT, sortKey);
    },
    [meetingMutations.SET_MEETINGS_SELECTED_STORE_SORT](state, sortKey) {
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
    async [meetingActions.ADD_NEW_MEETING]({ dispatch }, params) {
      const result = await api.meeting.addNewMeeting(params);
      if (result && result.code === 201) {
        dispatch(meetingActions.GET_MEETINGS);
      }
    },
    async [meetingActions.UPDATE_MEETING]({ commit }, { meetingId, data }) {
      const result = await api.meeting.updateMeeting(meetingId, data);
      if (result && result.code === 200) {
        commit(meetingMutations.SET_MEETING, result.data);
      }
    },
    async [meetingActions.DELETE_MEETING]({ commit }, meetingId) {
      const result = await api.meeting.deleteMeeting(meetingId);
      if (result && result.code === 204) {
        commit(meetingMutations.GET_MEETINGS);
      }
    },
    [meetingActions.GET_MEETINGS_SELECTED_SORT]({ commit }) {
      const sortKey = sessionStorage[sessionStorageKeyNames.MEETING_LIST_SELECTED_SORT];
      if (sortKey) {
        commit(meetingMutations.SET_MEETINGS_SELECTED_SORT, sortKey);
      }
    },
    [meetingActions.SET_MEETINGS_SELECTED_SORT]({ commit }, sortKey) {
      if (sortKey) {
        commit(meetingMutations.SET_MEETINGS_SELECTED_SORT, sortKey);
        commit(meetingMutations.SET_MEETINGS_SELECTED_STORE_SORT, sortKey);
      }
    }
  }
};
