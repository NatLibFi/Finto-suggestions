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
    currentMeetingId: null,
    meetingIdForCurrentMeeting: null,
    [storeStateNames.ITEMS]: [],
    [storeStateNames.TINY_ITEMS]: [],
    [storeStateNames.ITEM]: null,
    [storeStateNames.MEETINGS_SELECTED_SORT]: null,
    [storeStateNames.UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS]: false,
    [storeStateNames.SET_CURRENT_MEETING_ID]: Number
  },
  getters: {
    getMeetingIdForCurrentMeeting: state => state['meetingIdForCurrentMeeting'],
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS],
    [meetingGetters.GET_MEETINGS_BASICS]: state => state[storeStateNames.TINY_ITEMS],
    [meetingGetters.GET_MEETINGS_AS_PITHY]: state => state[storeStateNames.ITEMS],
    [meetingGetters.GET_CURRENT_MEETING_ID]: state => state[storeStateNames.GET_CURRENT_MEETING_ID],
    [meetingGetters.GET_MEETING]: state => state[storeStateNames.ITEM],
    [meetingGetters.GET_MEETINGS_SELECTED_SORT]: state =>
      state[storeStateNames.MEETINGS_SELECTED_SORT],
    [meetingGetters.GET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS]: state =>
      state[storeStateNames.UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS]
  },
  mutations: {
    setCurrentMeetingIdInState (id) {
      Vue.set(this.state, currentMeetingId, id);
    },
    [meetingMutations.SET_MEETINGS](state, meetings) {
      if (meetings && meetings.length > 0) {
        meetings.sort(comparerAsc('meeting_date'));
      }
      Vue.set(state, storeStateNames.ITEMS, meetings);
    },
    [meetingMutations.SET_MEETINGS_BASICS](state, meetingsBasics) {
      Vue.set(state, storeStateNames.TINY_ITEMS, meetingsBasics);
    },
    [meetingMutations.SET_MEETINGS_AS_PITHY](state, meetingsAsPithy) {
      Vue.set(state, storeStateNames.ITEMS, meetingsAsPithy);
    },
    [meetingMutations.SET_MEETING](state, meeting) {
      Vue.set(state, storeStateNames.ITEM, meeting);
    },
    [meetingMutations.SET_CURRENT_MEETING_ID](state, currentMeetingId) {
      Vue.set(state, storeStateNames.SET_CURRENT_MEETING_ID, currentMeetingId)
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
    async [meetingActions.GET_MEETINGS_BASICS]({ commit }) {
      const response = await api.meeting.getMeetingsBasics();
      if (response && response.code === 200) {
        commit(meetingMutations.SET_MEETINGS_BASICS, response.data);
      }
    },
    async [meetingActions.GET_MEETINGS_AS_PITHY]({ commit }) {
      const response = await api.meeting.getMeetings();
      if (response && response.code === 200) {
        commit(meetingMutations.SET_MEETINGS_AS_PITHY, response.data);
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
    },
    [meetingActions.SET_CURRENT_MEETING_ID]({ commit }, meetingId) {
      if (sortKey) {
        commit(meetingMutations.SET_CURRENT_MEETING_ID, meetingId);
      }
    }
  }
};
