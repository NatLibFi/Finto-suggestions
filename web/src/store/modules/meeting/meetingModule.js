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
    [storeStateNames.MEETINGS_SELECTED_SORT]: null,
    [storeStateNames.UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS]: false
  },
  getters: {
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS],
    [meetingGetters.GET_MEETING]: state => state[storeStateNames.ITEM],
    [meetingGetters.GET_MEETINGS_SELECTED_SORT]: state =>
      state[storeStateNames.MEETINGS_SELECTED_SORT],
    [meetingGetters.GET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS]: state =>
      state[storeStateNames.UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS]
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
    },
    [meetingMutations.SET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS](state, value) {
      Vue.set(state, storeStateNames.UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS, value);
    }
  },
  actions: {
    async [meetingActions.GET_MEETINGS]({ commit }) {
      const response = await api.meeting.getMeetings();
      if (response && response.code === 200) {
        commit(meetingMutations.SET_MEETINGS, response.data);
      }
    },
    async [meetingActions.GET_MEETING]({ commit }, meetingId) {
      const response = await api.meeting.getMeeting(meetingId);
      if (response && response.code === 200) {
        commit(meetingMutations.SET_MEETING, response.data);
      }
    },
    async [meetingActions.ADD_NEW_MEETING]({ dispatch }, params) {
      const response = await api.meeting.addNewMeeting(params);
      if (response && response.code === 201) {
        dispatch(meetingActions.GET_MEETINGS);
      }
    },
    async [meetingActions.UPDATE_MEETING]({ commit }, { meetingId, data }) {
      const response = await api.meeting.updateMeeting(meetingId, data);
      if (response && response.code === 200) {
        commit(meetingMutations.SET_MEETING, response.data);
      }
    },
    async [meetingActions.DELETE_MEETING]({ commit }, meetingId) {
      const response = await api.meeting.deleteMeeting(meetingId);
      if (response && response.code === 204) {
        await commit(meetingMutations.GET_MEETINGS);
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
