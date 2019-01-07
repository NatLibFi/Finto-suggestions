import Vue from 'vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
  sessionStorageKeyNames,
  suggestionMutations,
  suggestionGetters,
  suggestionActions
} from './suggestionConsts';

export const mapSuggestionGetters = getters => mapGetters(namespace, getters);
export const mapSuggestionActions = actions => mapActions(namespace, actions);
export const mapSuggestionMutations = mutations => mapMutations(namespace, mutations);

export default {
  namespaced: true,
  state: {
    [storeStateNames.ITEMS]: [],
    [storeStateNames.FILTERS]: [],
    [storeStateNames.ITEM]: null,
    [storeStateNames.SELECTED_SORT]: null
  },
  getters: {
    [suggestionGetters.GET_SUGGESTIONS]: state => state[storeStateNames.ITEMS],
    [suggestionGetters.GET_SUGGESTION]: state => state[storeStateNames.ITEM],
    [suggestionGetters.GET_SEARCH_QUERY]: state => state[storeStateNames.SEARCH_QUERY],
    [suggestionGetters.GET_FILTERS]: state => state[storeStateNames.FILTERS],
    [suggestionGetters.GET_SELECTED_SORT]: state => state[storeStateNames.SELECTED_SORT]
  },
  mutations: {
    [suggestionMutations.SET_SUGGESTIONS](state, suggestions) {
      Vue.set(state, storeStateNames.ITEMS, suggestions);
    },
    [suggestionMutations.SET_SEARCH_QUERY](state, searchQuery) {
      Vue.set(state, storeStateNames.SEARCH_QUERY, searchQuery);
    },
    [suggestionMutations.SET_FILTERS](state, filters) {
      Vue.set(state, storeStateNames.FILTERS, filters);
    },
    [suggestionMutations.SET_SUGGESTION](state, suggestion) {
      Vue.set(state, storeStateNames.ITEM, suggestion);
    },
    [suggestionMutations.SET_SELECTED_SORT](state, sortKey) {
      Vue.set(state, storeStateNames.SELECTED_SORT, sortKey);
    },
    [suggestionMutations.SET_SELECTED_STORAGE_SORT](state, sortKey) {
      Vue.set(sessionStorage, sessionStorageKeyNames.SUGGESTION_LIST_SELECTED_SORT, sortKey);
    }
  },
  actions: {
    async [suggestionActions.GET_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    },
    async [suggestionActions.GET_SORTED_SUGGESTIONS]({ commit }, sortValue) {
      const result = await api.suggestion.getSortedSuggestions(sortValue);
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    },
    async [suggestionActions.GET_SUGGESTION_BY_ID]({ commit }, suggestionId) {
      const result = await api.suggestion.getSuggestionById(suggestionId);
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTION, result.data);
      }
    },
    async [suggestionActions.ASSIGN_SUGGESTION_TO_USER]({ commit }, { suggestionId, userId }) {
      const result = await api.suggestion.assignUserToSuggestion(suggestionId, userId);
      if (result && result.code == 202) {
        commit(suggestionMutations.SET_SUGGESTION, result.data);
      }
    },
    async [suggestionActions.UNASSIGN_SUGGESTION_FROM_USER]({ commit }, suggestionId) {
      const result = await api.suggestion.unassignUserFromSuggestion(suggestionId);
      if (result && result.code == 202) {
        commit(suggestionMutations.SET_SUGGESTION, result.data);
      }
    },
    [suggestionActions.GET_SELECTED_SORT_KEY]({ commit }) {
      const sortKey = sessionStorage[sessionStorageKeyNames.SUGGESTION_LIST_SELECTED_SORT];
      if (sortKey) {
        commit(suggestionMutations.SET_SELECTED_SORT, sortKey);
      }
    },
    [suggestionActions.SET_SELECTED_SORT_KEY]({ commit }, sortKey) {
      if (sortKey) {
        commit(suggestionMutations.SET_SELECTED_SORT, sortKey);
        commit(suggestionMutations.SET_SELECTED_STORAGE_SORT, sortKey);
      }
    },
    async [suggestionActions.GET_SUGGESTIONS_BY_MEETING_ID]({ commit }, meetingId) {
      const result = await api.suggestion.getSuggestionByMeetingId(meetingId);
      if (result && result.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    },
    async [suggestionActions.GET_SORTED_SUGGESTIONS_BY_MEETING_ID]({ commit }, values) {
      const result = await api.suggestion.getSortedSuggestionByMeetingId(
        values.meetingId,
        values.sortValue
      );
      if (result && result.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    }
  }
};
