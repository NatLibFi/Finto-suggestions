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
    [storeStateNames.SUGGESTIONS_SELECTED_SORT]: null,
    [storeStateNames.MEETING_SUGGESTIONS_SELECTED_SORT]: null
  },
  getters: {
    [suggestionGetters.GET_SUGGESTIONS]: state => state[storeStateNames.ITEMS],
    [suggestionGetters.GET_SUGGESTION]: state => state[storeStateNames.ITEM],
    [suggestionGetters.GET_SEARCH_QUERY]: state => state[storeStateNames.SEARCH_QUERY],
    [suggestionGetters.GET_FILTERS]: state => state[storeStateNames.FILTERS],
    [suggestionGetters.GET_SUGGESTIONS_SELECTED_SORT]: state =>
      state[storeStateNames.SUGGESTIONS_SELECTED_SORT],
    [suggestionGetters.GET_MEETING_SUGGESTIONS_SELECTED_SORT]: state =>
      state[storeStateNames.MEETING_SUGGESTIONS_SELECTED_SORT]
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
    [suggestionMutations.SET_SUGGESTIONS_SELECTED_SORT](state, sortKey) {
      Vue.set(state, storeStateNames.SUGGESTIONS_SELECTED_SORT, sortKey);
    },
    [suggestionMutations.SET_SUGGESTIONS_SELECTED_STORAGE_SORT](state, sortKey) {
      Vue.set(sessionStorage, sessionStorageKeyNames.SUGGESTIONS_SELECTED_SORT, sortKey);
    },
    [suggestionMutations.SET_MEETING_SUGGESTIONS_SELECTED_SORT](state, sortKey) {
      Vue.set(state, storeStateNames.MEETING_SUGGESTIONS_SELECTED_SORT, sortKey);
    },
    [suggestionMutations.SET_MEETING_SUGGESTIONS_SELECTED_STORAGE_SORT](state, sortKey) {
      Vue.set(sessionStorage, sessionStorageKeyNames.MEETING_SUGGESTIONS_SELECTED_SORT, sortKey);
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
    [suggestionActions.GET_SUGGESTIONS_SELECTED_SORT]({ commit }) {
      const sortKey = sessionStorage[sessionStorageKeyNames.SUGGESTIONS_SELECTED_SORT];
      if (sortKey) {
        commit(suggestionMutations.SET_SUGGESTIONS_SELECTED_SORT, sortKey);
      }
    },
    [suggestionActions.SET_SUGGESTIONS_SELECTED_SORT]({ commit }, sortKey) {
      if (sortKey) {
        commit(suggestionMutations.SET_SUGGESTIONS_SELECTED_SORT, sortKey);
        commit(suggestionMutations.SET_SUGGESTIONS_SELECTED_STORAGE_SORT, sortKey);
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
    },
    [suggestionActions.GET_MEETING_SUGGESTIONS_SELECTED_SORT]({ commit }) {
      const sortKey = sessionStorage[sessionStorage.MEETING_SUGGESTIONS_SELECTED_SORT];
      if (sortKey) {
        commit(suggestionMutations.SET_MEETING_SUGGESTIONS_SELECTED_SORT, sortKey);
      }
    },
    [suggestionActions.SET_MEETING_SUGGESTIONS_SELECTED_SORT]({ commit }, sortKey) {
      if (sortKey) {
        commit(suggestionMutations.SET_MEETING_SUGGESTIONS_SELECTED_SORT, sortKey);
        commit(suggestionMutations.SET_MEETING_SUGGESTIONS_SELECTED_STORAGE_SORT, sortKey);
      }
    },
    async [suggestionActions.SET_SUGGESTION_ACCEPTED]({ dispatch }, params) {
      try {
        const response = await api.suggestion.updateSuggestionStatus(
          params.suggestionId,
          params.status,
          params.userId
        );
        if (response && response.code == 202) {
          dispatch(suggestionActions.GET_SUGGESTION_BY_ID, params.suggestionId);
        }
      } catch (error) {
        console.log(`Could not set suggestion state to accepted ${params.suggestionId} , ${error}`);
      }
    },
    async [suggestionActions.SET_SUGGESTION_REJECTED]({ dispatch }, params) {
      try {
        const response = await api.suggestion.updateSuggestionStatus(
          params.suggestionId,
          params.status
        );
        if (response && response.code == 202) {
          dispatch(suggestionActions.GET_SUGGESTION_BY_ID, params.suggestionId);
        }
      } catch (error) {
        console.log(`Could not set suggestion state to rejected ${params.suggestionId}, ${error}`);
      }
    },
    async [suggestionActions.SET_SUGGESTION_RETAINED]({ dispatch }, params) {
      try {
        const response = await api.suggestion.updateSuggestionStatus(
          params.suggestionId,
          params.status
        );
        if (response && response.code == 202) {
          dispatch(suggestionActions.GET_SUGGESTION_BY_ID, params.suggestionId);
        }
      } catch (error) {
        console.log(`Could not set suggestion state to rejected ${params.suggestionId}, ${error}`);
      }
    },
    async [suggestionActions.GET_SUGGESTIONS_BY_SEARCH_WORD]({ commit }, searchWord) {
      const result = await api.suggestion.getSuggestionsBySearchWord(searchWord);
      if (result && result.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    }
  }
};
