import Vue from 'vue';
import { mapGetters, mapActions } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  eventGetters,
  eventMutations,
  eventActions
} from './eventConsts';

export const mapEventGetters = getters => mapGetters(namespace, getters);
export const mapEventActions = actions => mapActions(namespace, actions);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: []
  },
  getters: {
    [eventGetters.GET_EVENTS]: state => state[storeStateNames.ITEMS]
  },
  mutations: {
    [eventMutations.SET_EVENTS](state, events) {
      Vue.set(state, storeStateNames.ITEMS, events);
    }
  },
  actions: {
    async [eventActions.ADD_NEW_EVENT]({ dispatch }, params) {
      if (params.event) {
        const response = await api.event.addNewComment(params.event);
        if (response && response.code === 201) {
          dispatch(eventActions.GET_EVENTS_BY_SUGGESTION, params.suggestionId);
        }
      }
    },
    async [eventActions.PATCH_EVENT]({ dispatch }, { eventId, data, suggestionId }) {
      const response = await api.event.patchEvent(eventId, data);
      if (response && response.code === 200) {
        dispatch(eventActions.GET_EVENTS_BY_SUGGESTION, suggestionId);
      }
    },
    async [eventActions.DELETE_EVENT]({ dispatch }, { eventId, suggestionId }) {
      await api.event.deleteEvent(eventId);
      dispatch(eventActions.GET_EVENTS_BY_SUGGESTION, suggestionId);
    },
    async [eventActions.GET_EVENTS_BY_SUGGESTION]({ commit }, suggestionId) {
      const response = await api.event.getEventsBySuggestion(suggestionId);
      if (response && response.code === 200) {
        commit(eventMutations.SET_EVENTS, response.data);
      }
    }
  }
};
