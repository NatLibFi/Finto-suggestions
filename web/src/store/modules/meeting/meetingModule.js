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
import isAfter from 'date-fns/is_after';
import isEqual from 'date-fns/is_equal';
import parse from 'date-fns/parse';

import { comparerAsc } from '../../../utils/sortingHelper';

export const mapMeetingGetters = getters => mapGetters(namespace, getters);
export const mapMeetingActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: [],
    [storeStateNames.ITEM]: null,
    [storeStateNames.FUTURE_MEETINGS_COUNT]: 0,
    [storeStateNames.PAST_MEETINGS_COUNT]: 0
  },
  getters: {
    [meetingGetters.GET_MEETINGS]: state => state[storeStateNames.ITEMS],
    [meetingGetters.GET_MEETING]: state => state[storeStateNames.ITEM],
    [meetingGetters.GET_FUTURE_MEETINGS_COUNT]: state =>
      state[storeStateNames.FUTURE_MEETINGS_COUNT],
    [meetingGetters.GET_PAST_MEETINGS_COUNT]: state => state[storeStateNames.PAST_MEETINGS_COUNT]
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
    [meetingMutations.SET_FUTURE_MEETINGS_COUNT](state, count) {
      Vue.set(state, storeStateNames.FUTURE_MEETINGS_COUNT, count);
    },
    [meetingMutations.SET_PAST_MEETINGS_COUNT](state, count) {
      Vue.set(state, storeStateNames.PAST_MEETINGS_COUNT, count);
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
    async [meetingActions.GET_FUTURE_AND_PAST_MEETINGS_COUNT]({ commit }) {
      const result = await api.meeting.getMeetings();
      if (result && result.code === 200) {
        let futureMeetings = [];
        let pastMeetings = [];
        const today = Date();
        result.data.forEach(meeting => {
          if (meeting.meeting_date) {
            if (
              isAfter(parse(meeting.meeting_date), today) ||
              isEqual(parse(meeting.meeting_date), today)
            ) {
              futureMeetings.push(meeting);
            } else {
              pastMeetings.push(meeting);
            }
          }
        });
        commit(meetingMutations.SET_FUTURE_MEETINGS_COUNT, futureMeetings.length);
        commit(meetingMutations.SET_PAST_MEETINGS_COUNT, pastMeetings.length);
      }
    }
  }
};
