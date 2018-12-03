import Vue from 'vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import api from '../../../api';
import {
  namespace,
  storeStateNames,
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
    [storeStateNames.OPEN_COUNT]: 0,
    [storeStateNames.RESOLVED_COUNT]: 0,
    [storeStateNames.FILTERS]: [],
    [storeStateNames.ITEM]: null
  },
  getters: {
    [suggestionGetters.GET_SUGGESTIONS]: state => state[storeStateNames.ITEMS],
    [suggestionGetters.GET_SUGGESTION]: state => state[storeStateNames.ITEM],
    [suggestionGetters.GET_OPEN_SUGGESTIONS_COUNT]: state => state[storeStateNames.OPEN_COUNT],
    [suggestionGetters.GET_RESOLVED_SUGGESTIONS_COUNT]: state =>
      state[storeStateNames.RESOLVED_COUNT],
    [suggestionGetters.GET_SEARCH_QUERY]: state => state[storeStateNames.SEARCH_QUERY],
    [suggestionGetters.GET_FILTERS]: state => state[storeStateNames.FILTERS],
    [suggestionGetters.GET_PAGINATION_SUGGESTIONS]: state => state[storeStateNames.PAGINATED_ITEMS]
  },
  mutations: {
    [suggestionMutations.SET_SUGGESTIONS](state, suggestions) {
      Vue.set(state, storeStateNames.ITEMS, suggestions);
    },
    [suggestionMutations.SET_OPEN_SUGGESTIONS_COUNT](state, count) {
      Vue.set(state, storeStateNames.OPEN_COUNT, count);
    },
    [suggestionMutations.SET_RESOLVED_SUGGESTIONS_COUNT](state, count) {
      Vue.set(state, storeStateNames.RESOLVED_COUNT, count);
    },
    [suggestionMutations.SET_SEARCH_QUERY](state, searchQuery) {
      Vue.set(state, storeStateNames.SEARCH_QUERY, searchQuery);
    },
    [suggestionMutations.SET_FILTERS](state, filters) {
      Vue.set(state, storeStateNames.FILTERS, filters);
    },
    [suggestionMutations.SET_PAGINATION_SUGGESTIONS](state, suggestions) {
      Vue.set(state, storeStateNames.PAGINATED_ITEMS, suggestions);
    },
    [suggestionMutations.SET_SUGGESTION](state, suggestion) {
      Vue.set(state, storeStateNames.ITEM, suggestion);
    }
  },
  actions: {
    async [suggestionActions.GET_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTIONS, result.data);
      }
    },
    async [suggestionActions.GET_OPEN_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getOpenSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_OPEN_SUGGESTIONS_COUNT, result.items);
      }
    },
    async [suggestionActions.GET_RESOLVED_SUGGESTIONS]({ commit }) {
      const result = await api.suggestion.getResolvedSuggestions();
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_RESOLVED_SUGGESTIONS_COUNT, result.items);
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
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTION, result.data);
      }
    },
    async [suggestionActions.UNASSIGN_SUGGESTION_FROM_USER]({ commit }, suggestionId) {
      const result = await api.suggestion.unassignUserFromSuggestion(suggestionId);
      if (result && result.code == 200) {
        commit(suggestionMutations.SET_SUGGESTION, result.data);
      }
    }
  }
};
