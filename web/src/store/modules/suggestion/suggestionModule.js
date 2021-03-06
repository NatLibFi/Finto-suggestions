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
    [storeStateNames.COUNT]: 0,
    [storeStateNames.ARCHIVED_SUGGESTIONS_COUNT]: 0,
    [storeStateNames.FILTERS]: [],
    [storeStateNames.ITEM]: null,
    [storeStateNames.FILTERED_ITEMS]: []
  },
  getters: {
    [suggestionGetters.GET_SUGGESTIONS]: state => state[storeStateNames.ITEMS],
    [suggestionGetters.GET_SUGGESTIONS_COUNT]: state => state[storeStateNames.COUNT],
    [suggestionGetters.GET_ARCHIVED_SUGGESTIONS_COUNT]: state =>
      state[storeStateNames.ARCHIVED_SUGGESTIONS_COUNT],
    [suggestionGetters.GET_SUGGESTION]: state => state[storeStateNames.ITEM],
    [suggestionGetters.GET_SEARCH_QUERY]: state => state[storeStateNames.SEARCH_QUERY],
    [suggestionGetters.GET_FILTERS]: state => state[storeStateNames.FILTERS],
    [suggestionGetters.GET_SUGGESTIONS_SELECTED_SORT]: state =>
      state[storeStateNames.SUGGESTIONS_SELECTED_SORT],
    [suggestionGetters.GET_MEETING_SUGGESTIONS_SELECTED_SORT]: state =>
      state[storeStateNames.MEETING_SUGGESTIONS_SELECTED_SORT],
    [suggestionGetters.GET_FILTERED_ITEMS]: state => state[storeStateNames.FILTERED_ITEMS]
  },
  mutations: {
    [suggestionMutations.SET_SUGGESTIONS](state, suggestions) {
      Vue.set(state, storeStateNames.ITEMS, suggestions);
    },
    [suggestionMutations.SET_SUGGESTIONS_COUNT](state, count) {
      Vue.set(state, storeStateNames.COUNT, count);
    },
    [suggestionMutations.SET_ARCHIVED_SUGGESTIONS_COUNT](state, archivedCount) {
      Vue.set(state, storeStateNames.ARCHIVED_SUGGESTIONS_COUNT, archivedCount);
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
    },
    [suggestionMutations.SET_FILTERED_ITEMS](state, filtered_items) {
      Vue.set(state, storeStateNames.FILTERED_ITEMS, filtered_items);
    },
    [suggestionMutations.SET_SELECTED_STORAGE_FILTERS](state, filters) {
      Vue.set(sessionStorage, sessionStorageKeyNames.SELECTED_FILTERS, filters);
    }
  },
  actions: {
    async [suggestionActions.GET_SUGGESTIONS]({ commit }, { offset, sort, filters, searchWord }) {
      const response = await api.suggestion.getSuggestions(offset, sort, filters, searchWord);
      if (response && response.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, response.data);
        return response.items;
      } else {
        return [];
      }
    },
    async [suggestionActions.GET_SUGGESTIONS_COUNT]({ commit }, { filters, searchWord }) {
      const response = await api.suggestion.getSuggestionsCount(filters, searchWord);
      if (response && response.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS_COUNT, response.data.count);
      }
    },
    async [suggestionActions.GET_ARCHIVED_SUGGESTIONS_COUNT]({ commit }, { filters, searchWord }) {
      const response = await api.suggestion.getArchivedSuggestionsCount(filters, searchWord);
      if (response && response.code == 200) {
        commit(suggestionMutations.SET_ARCHIVED_SUGGESTIONS_COUNT, response.data.count);
      }
    },
    async [suggestionActions.GET_SUGGESTIONS_BY_USER_ID]({ commit }, { userId, offset }) {
      const response = await api.suggestion.getSuggestionsByUserId(userId, offset);
      if (response && response.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, response.data);
      } else {
        return [];
      }
    },
    async [suggestionActions.GET_SUGGESTION_BY_ID]({ commit }, suggestionId) {
      const response = await api.suggestion.getSuggestionById(suggestionId);
      if (response && response.code == 200) {
        commit(suggestionMutations.SET_SUGGESTION, response.data);
      }
    },
    async [suggestionActions.ASSIGN_SUGGESTION_TO_USER]({ commit }, { suggestionId, userId }) {
      const response = await api.suggestion.assignUserToSuggestion(suggestionId, userId);
      if (response && response.code == 202) {
        commit(suggestionMutations.SET_SUGGESTION, response.data);
      }
    },
    async [suggestionActions.UNASSIGN_SUGGESTION_FROM_USER]({ commit }, suggestionId) {
      const response = await api.suggestion.unassignUserFromSuggestion(suggestionId);
      if (response && response.code == 202) {
        commit(suggestionMutations.SET_SUGGESTION, response.data);
      }
    },
    async [suggestionActions.ASSIGN_SUGGESTION_TO_MEETING](
      { commit },
      { suggestionId, meetingId }
    ) {
      const response = await api.suggestion.assignSuggestionToMeeting(suggestionId, meetingId);
      if (response && response.code == 202) {
        commit(suggestionMutations.SET_SUGGESTION, response.data);
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
      const response = await api.suggestion.getSuggestionsByMeetingId(meetingId);
      if (response && response.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, response.data);
      }
    },
    [suggestionActions.GET_MEETING_SUGGESTIONS_SELECTED_SORT]({ commit }) {
      const sortKey = sessionStorage[sessionStorageKeyNames.MEETING_SUGGESTIONS_SELECTED_SORT];
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
    async [suggestionActions.SET_SUGGESTION_STATUS]({ dispatch }, params) {
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
    [suggestionActions.GET_SELECTED_FILTERS]({ commit }) {
      const filters = sessionStorage[sessionStorageKeyNames.SELECTED_FILTERS];
      if (filters) {
        commit(suggestionMutations.SET_FILTERS, JSON.parse(filters));
      }
    },
    [suggestionActions.SET_SELECTED_FILTERS]({ commit }, filters) {
      if (filters) {
        commit(suggestionMutations.SET_SELECTED_STORAGE_FILTERS, JSON.stringify(filters));
        commit(suggestionMutations.SET_FILTERS, filters);
      }
    },
    async [suggestionActions.GET_OPEN_SUGGESTIONS]({ commit }, offset) {
      const response = await api.suggestion.getOpenSuggestions(offset);
      if (response && response.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, response.data);
      }
    },
    async [suggestionActions.GET_RESOLVED_SUGGESTIONS]({ commit }, offset) {
      const response = await api.suggestion.getResolvedSuggestions(offset);
      if (response && response.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, response.data);
      }
    },
    async [suggestionActions.RESET_SUGGESTION_LISTING]({ commit }) {
      const response = await api.suggestion.getSuggestions();
      if (response && response.code === 200) {
        commit(suggestionMutations.SET_SUGGESTIONS_SELECTED_STORAGE_SORT, 'CREATED_DESC');
        commit(suggestionMutations.SET_SUGGESTIONS, response.data);
        commit(suggestionMutations.SET_SELECTED_STORAGE_FILTERS, []);
        commit(suggestionMutations.SET_FILTERS, []);
      }
    }
  }
};
